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
        self.database_name = "trivia_test"
        self.database_path = f"postgresql://postgres:Possible001#@localhost:5432/{self.database_name}"

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
    def test_get_categories(self):
        """Test getting categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_404_if_category_not_found(self):
        res = self.client().post('/question', json={"question": 4353,
         "answer": True, "category": "3"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_questions(self):
        """Test getting categories"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_404_if_question_not_found(self):
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question(self):
        """Test delete question"""
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_delete_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/127890')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_404_if_question_not_specified(self):
        res = self.client().delete('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_create_new_questions(self):
        """Test create new question"""
        res = self.client().post('/questions', json={"question": "Elon Musk's dog's name?",
         "answer": "flukky", "category": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_400_error_for_create_new_questions(self):
        """Test getting categories"""
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_405_if_question_creation_is_not_allowed(self):
        res = self.client().post('/questions/432', json={"question": 4353,
         "answer": True, "category": "3"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_404_if_question_creation_does_not_exist(self):
        res = self.client().post('/question', json={"question": 4353,
         "answer": True, "category": "3"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    def test_search_for_question_with_result(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'india'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_for_question_without_result(self):
        res = self.client().post('/questions/search', json={'searchTerm':'korukpe'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_error_400_search_for_question_without_search_item(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


    def test_retieve_question_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_error_405_retieve_question_by_category(self):
        res = self.client().post('/categories/565/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    
    def test_play_quiz(self):
        new_quiz = {'previous_questions': [23, 12],
                        'quiz_category': {'type': 'History', 'id': 4}
                        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['previous_questions'])
        self.assertTrue(data['question'])

    def test_play_quiz_without_quiz_category(self):
        new_quiz = {'previous_questions': [23, 12]}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['previous_questions'])
        self.assertTrue(data['question'])

    def test_play_quiz_without_previous_questions(self):
        new_quiz = { 'previous_questions': {},'quiz_category': {'type': 'History', 'id': 4}}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['previous_questions'])
        self.assertTrue(data['question'])

    def test_play_quiz_without_previous_questions_and_quiz_category(self):
        new_quiz = { 'previous_questions': {}}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['previous_questions'])
        self.assertTrue(data['question'])

    def test_error_404_play_quiz(self):
        new_quiz = { 'previous_questions': {},'quiz_category': {'type': 'History', 'id': 4}}
        res = self.client().post('/quiz', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''def test_error_404_play_quiz(self):
        new_quiz = { 'previous_questions': {},'quiz_category': {'type': 'History', 'id': 4}}
        res = self.client().get('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')'''


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()