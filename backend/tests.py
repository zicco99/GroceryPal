import unittest
import json
from flask import jsonify

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

#Schemas to deserialize etc.
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    Config.TEST_USERNAME_ROLE, Config.TEST_PASSWORD_ROLE, Config.TEST_DB_IP, Config.TEST_PORT, Config.TEST_DB_NAME)

class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app, self.session, self.metadata = create_app(Config,connection_string,True)
        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(self):
        pass

    ############################### ENDPOINT TESTING ############################################
    #create

    def test_products(self):

        new_product = Product(
            barcode=5410041001204,
            ingredient_id=None,
            name='TUC',
            brand='boh',
            labels=[True, False, True],  # Gluten-free, not vegan, healthy
            eco_score=4,
            nova_score=2,
            big_image_url='https://example.com/image.jpg',
            mini_image_url='https://example.com/mini_image.jpg',
            # Not breakfast, lunch, not snack, dinner
            meal=[False, True, False, True],
            allergens=['nuts', 'peanuts', 'gluten'],
            quantity=100)
        
        response = self.client.post(
            'api/products/{}'.format(new_product.barcode), json=product_schema.dump(new_product))
        self.assertEqual(response.status_code, 201)

        with self.app.app_context():
            new_product_serialized = product_schema.dump(new_product)
            new_product_deserialized = product_schema.load(
                new_product_serialized, session=self.session)
            print(new_product_deserialized)
            response = self.client.post('api/products/{}'.format(new_product.barcode), json = new_product_serialized)
            self.assertEqual(response.status_code, 201)

            response = self.client.get('api/products/{}'.format(new_product.barcode))
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(new_product_serialized, response.json)


    """ def test_get_feedbacks(self):
        response = self.client.get('api/feedbacks')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1) """

    # add more test cases for other endpoints and edge cases


if __name__ == '__main__':
    unittest.main()
