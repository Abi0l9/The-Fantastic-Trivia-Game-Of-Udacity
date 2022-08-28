import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_name = 'trivia'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "admin", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # paginated pages test

    def test_paginated_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 200)
        self.assertEqual(data['message'], 'Ok')
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_paginated_questions_fail(self):
        res = self.client().get('/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Content not found!')

    # categories test
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    #delete test (success)
    def test_delete_question_success(self):
        res = self.client().delete('/questions/8')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_question_id'])

    #delete test (failed) question already deleted or not found
    def test_delete_question_fail(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # questions by category (success)
    def test_get_questions_by_category_success(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Ok')
        self.assertTrue(data['questions'])

    # questions by category (failed)
    def test_get_questions_by_category_fail(self):
        res = self.client().get('/categories/80/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #new question was successfully added to the database using post method
    def test_post_new_question_success(self):
        res = self.client().post(
            '/questions', json={'question': 'The full meaning of CLI is ?', 'answer': 'Command Line Interface', 'difficulty': 3, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Ok')

    # new question fail test due to duplicate entry (RETURNS SUCCESS AT TEST EXECUTION)
    def test_post_new_question_fail(self):
        res = self.client().post(
            '/questions', json={'question': 'The full meaning of CLI is ?', 'answer': 'Command Line Interface', 'difficulty': 3, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)

    # new question failed test due to duplicate entry (RETURNS FAILED AT TEST EXECUTION)
    def test_post_new_question_fail(self):
        res = self.client().post(
            '/questions', json={'question': 'The full meaning of CLI is ?', 'answer': 'Command Line Interface', 'difficulty': 3, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # new question fail test due to an empty body (success)
    def test_post_new_question_fail_two(self):
        res = self.client().post(
            '/questions', json={'question': '', 'answer': '', 'difficulty': 3, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # search test (success)
    def test_search_success(self):
        res = self.client().post(
            '/questions/', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['searchTerm'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # search test (fail)
    def test_search_fail(self):
        res = self.client().post(
            '/questions/', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_quizzes_page(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'type': 'Sports', 'id': 6}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_invalid_page(self):
        res = self.client().get('/sports')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Content not found!')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
