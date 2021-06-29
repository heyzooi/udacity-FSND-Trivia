from array import array
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
import sys
import re
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    def check_request_json():
        content_type = request.headers.get('Content-Type')
        if content_type is None:
            abort(400, 'content_type header is missing')

        match = re.match(
            r'^(application\/json)(?:\; charset=(.*))?$',
            content_type
        )
        if match is None or match.group(1) != 'application/json':
            abort(400, 'content_type header is not application/json')

        if match.group(2) is not None and match.group(2) != 'utf-8':
            abort(400, 'content_type header charset is not utf-8')

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, OPTION'
        )
        return response

    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def categories():
        categories = Category.query.all()
        return jsonify({
            'categories': {c.id: c.type for c in categories}
        })

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
    pages. Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def questions(category_id=None, searchTerm=None):
        page = request.args.get('page', 1, type=int)
        questions = Question.query
        if category_id is not None:
            questions = questions.filter_by(category_id=category_id)
        if searchTerm is not None:
            questions = questions.filter(
                Question.question.ilike(f'%{searchTerm}%')
            )
        questions = questions.order_by(
            Question.question.desc()
        ).paginate(
            page=page,
            per_page=QUESTIONS_PER_PAGE
        )
        categories = Category.query.order_by(Category.id).all()
        return jsonify({
            'questions': [q.format() for q in questions.items],
            'total_questions': questions.total,
            'current_category': category_id,
            'categories': {c.id: c.type for c in categories},
        })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed. This removal will persist in the database and when you refresh
    the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify(question.format())

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        check_request_json()

        data = json.loads(request.data)

        question = data.get('question')
        if question is None:
            abort(400, 'question is missing')

        answer = data.get('answer')
        if answer is None:
            abort(400, 'answer is missing')

        category_id = data.get('category_id')
        if category_id is None:
            abort(400, 'category_id is missing')

        difficulty = data.get('difficulty')
        if difficulty is None:
            abort(400, 'difficulty is missing')

        question = Question(
            question=question,
            answer=answer,
            category_id=category_id,
            difficulty=difficulty,
        )
        try:
            question.insert()
            return jsonify({
                'id': question.id
            }), 201
        except Exception as error:
            print(sys.exc_info())
            abort(422, str(error))

    '''
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def searchQuestions():
        check_request_json()
        searchTerm = json.loads(request.data)['searchTerm']
        return questions(searchTerm=searchTerm)

    '''
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def questions4Category(category_id):
        return questions(category_id)

    '''
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        check_request_json()
        req_data = json.loads(request.data)

        previous_questions = req_data.get('previous_questions')
        if previous_questions is None:
            abort(400, 'previous_questions is missing')
        if type(previous_questions) is not list and \
                type(previous_questions) is not array:
            abort(400, 'previous_questions is not an list or array')

        category_id = req_data.get('quiz_category_id')
        if category_id is not None and type(category_id) is not int:
            abort(400, 'quiz_category_id is not an integer')

        questions = Question.query
        if category_id is not None:
            questions = questions.filter_by(category_id=category_id)
        questions = questions.filter(
            Question.id.notin_(previous_questions)
        )
        count = questions.count()
        n = random.randint(1, count)
        question = questions.offset(n - 1).limit(1).first()
        if question is not None:
            return jsonify({
                'question': question.format()
            })
        else:
            return jsonify({})

    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': error.description,
            'message': 'bad request',
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': str(error),
            'message': 'not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': str(error),
            'message': 'unprocessable entity',
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': str(error),
            'message': 'internal server error',
        }), 500

    return app
