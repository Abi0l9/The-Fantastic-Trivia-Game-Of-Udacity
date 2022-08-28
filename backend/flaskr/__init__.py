from http.client import FORBIDDEN
from multiprocessing import current_process
from models import setup_db, Question, Category, db
import random
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


####################################

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

    """
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    ###################   Functions ###########################
    #+++++ Pagination
    def paginate_items(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        items = [item.format() for item in selection]
        curr_item = items[start:end]

        return curr_item

    # +++++ Get Current Category

    def get_current_category(int):
        current_category = ''
        if int:
            current_category = [category[0].format() for category in db.session.query(Category.type,
                                                                                      Question.category).join(Question,
                                                                                                              Category.id == Question.category).order_by(Question.category).distinct().all()]
            return current_category[int - 1]
        else:
            current_category = [category[0].format() for category in db.session.query(Category.type,
                                                                                      Question.category).join(Question,
                                                                                                              Category.id == Question.category).order_by(Question.id).all()]
            return paginate_items(request, current_category)

    # ++++++ Get Category Type
    def get_category_types():
        all_categories = Category.query.all()

        final_categories = {}
        for category in all_categories:
            final_categories[category.id] = category.type
        return final_categories
    #########################################################
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():

        # use get_category_type function to get the category types
        return jsonify({
            "success": 200,
            "message": 'Ok',
            "success": True,
            "categories": get_category_types()
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/', methods=['GET'])
    @app.route('/questions', methods=['GET'])
    def questions():
        '''
        query the database to get all the questions
        paginate the questions according to the method
        use get_category_type function to get the category types
        throw an error if question is zero(0)
        '''
        all_questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_items(request, all_questions)

        if len(paginated_questions) == 0:
            return not_found()

        return jsonify({
            "success": True,
            "success": 200,
            "message": 'Ok',
            "questions": paginated_questions,
            "total_questions": len(all_questions),
            "categories": get_category_types(),
            "current_category": get_current_category(0)
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # listen to the id of the question to be deleted
        question = Question.query.get(question_id)
        # question needs to be available to have successful session
        if question:
            try:
                question.delete()
                return jsonify({
                    "success": True,
                    "success": 200,
                    "message": 'Ok',
                    "deleted_question_id": question_id
                })
            except:
                db.session.rollback()
            finally:
                db.session.close()
        # otherwise we present the response with error message
        else:
            return not_found()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        # JSON method is used here to grab the json formatted input from the frontend or through curl request
        question = request.json['question']
        answer = request.json['answer']
        difficulty = request.json['difficulty']
        category = request.json['category']

        # creates a new question
        new_question = Question(
            question=question, answer=answer, difficulty=difficulty, category=category)

        # query the database for validation purpose to check if the question already exist in there
        query_questions = Question.query.all()
        for questions in query_questions:
            if questions.question == question:
                return conflict()

        # questions without answers or vice-versa are forbidden and rejected.
        # There is no need to check for difficulty and categories because they've  been selected, automatically.
        if question == '' or answer == '':
            return forbidden_request()

        try:
            # adds the new question to the database
            new_question.insert()
            return jsonify({
                "success": True,
                "message": 'Ok',
                "question": question,
                "answer": answer,
                "difficulty": difficulty,
                "category": category,
            })

        except:
            # rollback if there are errors
            db.session.rollback()
        finally:
            # close session at the end of either success or failure
            db.session.close()

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/', methods=['POST'])
    def search_question():
        # get the input or data query
        searchTerm = request.json['searchTerm']

        # query the database with the input and store the result in a variable
        result = Question.query.filter(
            Question.question.like("%"+searchTerm+"%")).order_by(Question.category).all()

        # format and paginate results
        paginate_result = paginate_items(request, result)

        # get the current category of each question by looping through the result
        current_category = [get_current_category(question.category)
                            for question in result]

        # empty search is understood but wont be processed
        if searchTerm == "":
            return unprocessed()

        return jsonify({
            "success": True,
            "message": 'Ok',
            "questions": paginate_result,
            "total_questions": len(result),
            "current_category": current_category,
            "searchTerm": searchTerm
        })
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_category(id):
        query = db.session.query(Question).filter(
            Question.category == id).all()

        # format the results derived from the initial query
        questions = [question.format() for question in query]

        # get the id of the categories in the formatted result
        categories = [q.category for q in query]

        # loop through the categories and assign each to its appropriate id
        current_categories = [get_current_category(
            category) for category in categories]

        # Get request for an invalid category
        if id > 6:
            return not_found()

        return jsonify({
            "success": True,
            "success": 200,
            "message": 'Ok',
            "questions": questions,
            "total_questions": len(questions),
            "current_category": current_categories
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # get the input from the body through the clicked category or request
        quiz_category = request.json['quiz_category']

        # previous questions' ids are appended here after they have been answered
        previous_questions = request.json['previous_questions']

        # get the id of the selected category and save it the variable
        category_id = quiz_category['id']

        # present the UI with questions related to the clicked category or request through
        # the generated id
        # generate all questions in case the user clicked 'All'
        query = Question.query.all()

        # generate questions based on category in case the user clicked or request for any of the
        # listed categories (Sports, Art....)
        questions_by_category = Question.query.filter(
            Question.category == category_id).all()

        # logic to present the user the questions selected based on id
        formatted_questions = [question.format() for question in query] if category_id == 0 else [
            question.format() for question in questions_by_category]

        # present random questions but get the indexes first through random method
        question_index = random.randrange(0, len(formatted_questions))

        # current question is derived based on the index
        current_question = formatted_questions[question_index]

        return jsonify({
            "success": True,
            "message": 'OK',
            "question": current_question,
            "total_questions": len(formatted_questions),
            "category": quiz_category['type']
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request():
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Invalid input or bad request!"
        }), 400

    @app.errorhandler(403)
    def forbidden_request():
        return jsonify({
            "success": False,
            "error": 403,
            "message": "The server understands the request but fails to authorize it!"
        }), 403

    @app.errorhandler(404)
    def not_found():
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Content not found!"
        }), 404

    @app.errorhandler(409)
    def conflict():
        return jsonify({
            "success": False,
            "error": 409,
            "message": "Request not completed due to a conflict with the correct state of resource... duplicate entry!"
        }), 409

    @app.errorhandler(422)
    def unprocessed():
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Can't process an empty or invalid input!"
        }), 422

    @app.errorhandler(500)
    def server_error():
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server couldn't process the request...Invalid request!"
        }), 500

    ##################################################
    # Invalid link definition

    @app.route('/<string:link>', methods=['GET'])
    def inalid_links(link):
        site_links = ['questions', 'categories', 'quizzes']
        for i in range(len(site_links)):
            if link not in site_links:
                return not_found()

        return jsonify({
            "success": False,
            "message": 'Requested page is not found on this server!'
        })
    ##################################################
    return app
