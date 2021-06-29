import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from uuid import uuid4


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        host = 'localhost'
        port = 5432
        self.database_path = f"postgres://{host}:{port}/{self.database_name}"
        setup_db(self.app, self.database_path)
        self.questions_to_delete = []

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        for question_to_delete in self.questions_to_delete:
            question_to_delete.delete()
        self.questions_to_delete.clear()

    """
    DONE
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def testCORS(self):
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.headers.get('Access-Control-Allow-Headers'),
            'Content-Type'
        )
        self.assertEqual(
            res.headers.get('Access-Control-Allow-Methods'),
            'GET, POST, DELETE, OPTION'
        )
        self.assertEqual(res.headers.get('Access-Control-Allow-Origin'), '*')

    def testQuestionsPagination(self):
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

    def testQuestionsPaginationPage1(self):
        res = self.client().get('/questions?page=1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

    def testQuestionsPaginationPage2(self):
        res = self.client().get('/questions?page=2')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['total_questions'], 19)

    def testGetCategories(self):
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['categories']['1'], 'Science')

    def testDeleteQuestion(self):
        question = Question(
            question="What's the meaning of life?",
            answer='42',
            category_id=5,
            difficulty=1,
        )
        question.insert()
        self.questions_to_delete = [question]
        res = self.client().delete(f'/questions/{question.id}')

        self.assertEqual(res.status_code, 200)
        self.questions_to_delete.clear()
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(data['question'], "What's the meaning of life?")
        self.assertEqual(data['answer'], '42')
        self.assertEqual(data['category'], 5)
        self.assertEqual(data['difficulty'], 1)

    def testAddQuestion(self):
        res = self.client().post('/questions', json={
            'question': "What's the meaning of life?",
            'answer': '42',
            'category_id': 5,
            'difficulty': 1,
        })

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertIsNotNone(data['id'])
        self.assertEqual(type(data['id']), int)
        self.questions_to_delete = [Question.query.get(data['id'])]

    def testSearchQuestion(self):
        uuid = uuid4().hex
        question = Question(
            question=f"My random uuid is {uuid}! Don't tell anyone please!",
            answer=uuid4().hex,
            category_id=5,
            difficulty=1,
        )
        question.insert()
        self.questions_to_delete = [question]

        res = self.client().post('/questions/search', json={
            'searchTerm': uuid,
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(
            data['questions'][0]['question'],
            f"My random uuid is {uuid}! Don't tell anyone please!"
        )

    def testQuestions4Category(self):
        res = self.client().get(f'/categories/1/questions')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 3)
        for question in data['questions']:
            self.assertEqual(question['category'], 1)

    def testQuizzesQuestionDoesNotRepeat(self):
        res = self.client().post('/quizzes', json={
            'quiz_category_id': None,
            'previous_questions': [
                2,
                4,
                5,
                6,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
            ],
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertIsNotNone(data.get('question'))
        self.assertEqual(data['question']['id'], 23)

    def testQuizzesQuestionByCategory(self):
        res = self.client().post('/quizzes', json={
            'quiz_category_id': 6,
            'previous_questions': [11],
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertIsNotNone(data.get('question'))
        self.assertEqual(data['question']['id'], 10)

    def test400BadRequest(self):
        res = self.client().post('/quizzes', json={})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'), 'previous_questions is missing')
        self.assertEqual(data.get('message'), 'bad request')

    def test404NotFound(self):
        res = self.client().get('/this_route_does_not_exists')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(
            data.get('error'),
            '404 Not Found: The requested URL was not found on the server. If '
            'you entered the URL manually please check your spelling and try '
            'again.'
        )
        self.assertEqual(data.get('message'), 'not found')

    def test422UnprocessableEntity(self):
        res = self.client().post('/questions', json={
            'question': "What's the meaning of life?",
            'answer': '42',
            'category_id': 5,
            'difficulty': 'easy',
        })

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.headers['Content-Type'], 'application/json')
        data = json.loads(res.data)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('message'), 'unprocessable entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
