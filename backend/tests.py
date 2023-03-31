import unittest

from sqlalchemy import create_engine
from config import Config
from main import create_app

# Import models
from database.mappers.feedback import *
from database.mappers.user import *
from database.mappers.userfridge import *
from database.mappers.step import *
from database.mappers.recipeingredient import *
from database.mappers.product import *
from database.mappers.ingredient import *
from database.mappers.fridgeproduct import *
from database.mappers.recipe import *
from database.mappers.fridge import *


class TestCase(unittest.TestCase):

    def setUp(self):
        self.connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
            Config.TEST_USERNAME_ROLE, Config.TEST_PASSWORD_ROLE, Config.TEST_DB_IP, Config.TEST_PORT, Config.TEST_DB_NAME)

        app, session, metadata = create_app(Config, self.connection_string)
        self.session = session
        self.metadata = metadata
        self.client = app.test_client

    def tearDown(self):
        engine = create_engine(self.connection_string)
        self.metadata.drop_all(bind=engine)

    ############################### ENDPOINT TESTING #############################################

    def test_get_feedbacks(self):
        response = self.client().get('api/feedback')
        print(response)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    """ def test_create_feedback(self):
        data = {
            'user_id': 1,
            'recipe_id': 1,
            'is_chosen': False,
            'rating': 3,
            'notes': 'Not bad.'
        }

        response = self.client().post('/feedback/', json=data)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['recipe_id'], 1)
        self.assertEqual(data['is_chosen'], False)
        self.assertEqual(data['rating'], 3)
        self.assertEqual(data['notes'], 'Not bad.')

    def test_get_feedback_by_id(self):
        response = self.client().get('/feedback/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['recipe_id'], 1)
        self.assertEqual(data['is_chosen'], True)
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['notes'], 'Delicious!')

    def test_update_feedback(self):
        data = {
            'user_id': 1,
            'recipe_id': 1,
            'is_chosen': False,
            'rating': 2,
            'notes': 'Could be better.'
        }

        response = self.client().put('/feedback/1', json=data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['recipe_id'], 1)
        self.assertEqual(data['is_chosen'], False)
        self.assertEqual(data['rating'], 2)
        self.assertEqual(data['notes'], 'Could be better.')

    def test_delete_feedback(self):
        response = self.client().delete('/feedback/1')

        self.assertEqual(response.status_code, 200)

        response = self.client().get('/feedback/1')
        self.assertEqual(response.status_code, 404)

    def test_get_user_feedbacks(self):
        response = self.client().get('/feedback/user-feedbacks/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1) """


if __name__ == '__main__':
    unittest.main()
