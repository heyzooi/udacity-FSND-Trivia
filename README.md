# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

- [x] 1. Use Flask-CORS to enable cross-domain requests and set response headers. 


- [x] 2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


- [x] 3. Create an endpoint to handle GET requests for all available categories. 


- [x] 4. Create an endpoint to DELETE question using a question ID. 


- [x] 5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


- [x] 6. Create a POST endpoint to get questions based on category. 


- [x] 7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


- [x] 8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


- [x] 9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## REST API

***

### Retrieve All Categories

#### Example

##### Request
```
GET /categories
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

***

### Retrieve Questions (paginated, pages of 10 items)

#### Query Parameters

| Parameter | Type | Default Value |
| --- | --- | --- |
| page | int | 1 |

#### Example

##### Request
```
GET /questions?page=1
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "total_questions": 19
}
```

***

### Add Question

#### Body Parameters

| Parameter | Type |
| --- | --- |
| question | string |
| answer | string |
| difficulty | int |
| category_id | int |

#### Example

##### Request
```
POST /questions
Content-Type: application/json; charset=utf-8

{
  "question": "What's the meaning of life?",
  "answer": "42",
  "difficulty": 1,
  "category_id": 5
}
```

##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json

{
  "id": 34
}
```

***

### Delete Question

Path: `/questions/<question id>`

#### Path Parameters

| Parameter | Type |
| --- | --- |
| question id | int |

#### Example

##### Request
```
DELETE /questions/34
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "answer": "42", 
  "category": 5, 
  "difficulty": 1, 
  "id": 34, 
  "question": "What's the meaning of life?"
}
```

***

### Search Question

Path: `/questions/search`

#### Query Parameters

| Parameter | Type | Default Value |
| --- | --- | --- |
| page | int | 1 |

#### Body Parameters

| Parameter | Type |
| --- | --- |
| searchTerm | string |

#### Example

##### Request
```
POST /questions/search?page=1
Content-Type: application/json; charset=utf-8

{"searchTerm":"meaning"}
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "What's the meaning of life?"
    }
  ], 
  "total_questions": 1
}
```

***

### Questions by Category

Path: `/categories/<category id>/questions`

#### Path Parameters

| Parameter | Type |
| --- | --- |
| category id | int |

#### Example

##### Request
```
GET /categories/2/questions?page=1
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 4
}
```

***

### Play Quizzes

Path: `/quizzes`

#### Body Parameters

| Parameter | Type |
| --- | --- |
| previous_questions | list of ids (int) |
| quiz_category_id | id (int) |

#### Example

##### Request
```
POST /quizzes
Content-Type: application/json; charset=utf-8

{
  "previous_questions": [
    21
  ],
  "quiz_category_id": 1
}
```

##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json

{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }
}
```

***

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
