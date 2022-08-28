# The-Fantastic-Trivia-Game-Of-Udacity 

This is a trivia game that is set up to
entertain users accross the web, and also a project which gives developers
access to it's API. Interested developers can access the API to pull different
types of trivia games and also conribute to it, as it is an open project which
will continue to grow, eventually. 

The project has 2 folders at the top level:

<strong><li>FrontEnd</li></strong>
<strong><li>BackEnd</li></strong>

All backend code follows [PEP8 style
guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started ###

Pre-requisites and Local Development Developers using this project should
already have Python3, pip and node installed on their local machines. 

#### Backend 

From the backend folder run `pip install requirements.txt`. All required
packages are included in the requirements file. To run the application run the
following commands: 

```
export FLASK_APP=flaskr 
export FLASK_ENV=development
flask run 
``` 

These commands put the application in development and directs our
application to use the `__init__.py` file in our flaskr folder. 
Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/). 

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend 

From the frontend folder, run the following commands to start the client: 

``` 
npm install // only once to install dependencies 
npm start 
``` 

By default, the frontend will run on localhost:3000.

### Tests 

In order to run tests navigate to the backend folder and run the following commands: 

``` 
dropdb trivia 
createdb trivia 
psql trivia < trivia.psql
python test_flaskr.py 

```
The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

{
    "error": 404,
    "message": "Content not found!",
    "success": false
}

{
    "error": 422,
    "message": "Can't process an empty or invalid input!"
    "success": false
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 403: Forbidden
- 404: Content Not Found
- 409: Conflict
- 422: Not Processable 


### Endpoints 
#### GET /categories
- General:
    - Returns a list of category types, success value, and a message.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "message": "Ok",
    "success": true
}

```

#### GET /questions

- General:
    - Returns a list of questions that are paginated in groups of 10 per page, starting from 1.
    - It includes the success value, message, and total number of questions, categories of all the returned questions, and the current category of each question in order of each returned question.
    - Pages can also be queried with numbers if such page is available at the time of querying the pages.
 
- Sample: `curl http://127.0.0.1:5000/questions` 

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        "Entertainment",
        "Entertainment",
        "Sports",
        "Geography",
        "Geography",
        "Geography",
        "Art",
        "Art",
        "Art",
        "Art"
    ],
    "message": "Ok",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
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
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": 200,
    "total_questions": 19
}

```
- Sample (curl with page number): `curl http://127.0.0.1:5000/questions?pages=2` 

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        "Entertainment",
        "Entertainment",
        "Sports",
        "Geography",
        "Geography",
        "Geography",
        "Art",
        "Art",
        "Art",
        "Art"
    ],
    "message": "Ok",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
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
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": 200,
    "total_questions": 19
}

```

#### POST /questions

- General:
    - A new question is created using the submitted question, answer, category and difficulty. If successful, returns success value, and the question that has just been added to the database.
    - If the question or answer body is empty, or the question has already been added, before, the question will not be added by the server.
    
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is Computer?", "answer":"Computer is a machine receives data and processes information.", "difficulty":"1", "category": "Science"}'`

```
{
    "answer": "Computer is a machine receives data and processes information.",
    "category": "1",
    "difficulty": "1",
    "message": "Ok",
    "question": "What is Computer?",
    "success": true
}

```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted book, and a success value. 
- `curl -X DELETE http://127.0.0.1:5000/questions/12`

```
{
    "deleted_question": 12,
    "message": "Ok",
    "success": 200
}

```

#### POST /questions/
- General:
    - Takes the input query, and provides questions based on the search "string". Returns a list of any question that includes the search term.
    _ It returns the list in paginated form, list of all the questions, the current category of each question, the total number of pulled questions, and the search term, itself.

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`

```
{
    "current_category": [
        "Entertainment"
    ],
    "message": "Ok",
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "searchTerm": "title",
    "success": true,
    "total_questions": 1
}

```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions by their IDs, the total number of questions by their ID, the category name, and a success value (if the ID is true/found).

- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
    "current_category": [
        "Geography",
        "Geography"
    ],
    "message": "Ok",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": 200,
    "total_questions": 2
}

```

#### POST /quizzes
- General:
    - Takes category and previous question parameters and returns a random question based on the category selected or requested.
    _ It returns a random question on each refresh, success status, total number of questions in that category and the category name.

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"type": "Sports", "id": 6}, "previous_questions": []}'`

```
{
    "category": "Sports",
    "message": "OK",
    "question": {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    "success": true,
    "total_questions": 3
}

```


## Authors
Yours truly, Coach Kerry McCarthy and Session Leader, Anthony.

## Acknowledgements 
The awesome team at Udacity and all my fellow students who helped through their hints and beautiful ideas, soon to be full stack extraordinaires! 

