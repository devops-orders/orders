# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Order API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import Order, DataValidationError, db
from .order_factory import OrderFactory
from service.service import app, init_db, initialize_logging


DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/test')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderServer(unittest.TestCase):
    """ Order Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        initialize_logging(logging.INFO)
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 30
        init_db()

    @classmethod
    def tearDownClass(cls):
        # db.drop_all()
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()



    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(app).dispose()


    def _create_orders(self, count):
        """ Factory method to create orders in bulk """
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            resp = self.app.post('/orders',
                                 json=test_order.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create a test order')
            new_order = resp.get_json()
            test_order.id = new_order['id']
            orders.append(test_order)
        return orders

    def test_root_url(self):
        """ Test / route """
        resp = self.app.get('/',
                            content_type='application/json')
        print(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """ Get a list of Orders """
        self._create_orders(5)
        resp = self.app.get('/orders')
        print(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_order(self):
        """ Get a single order """
        test_order = self._create_orders(1)[0]
        resp = self.app.get('/orders/{}'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['uuid'], test_order.uuid)

    def test_get_order_by_product(self):
        """ Get an order linked to product"""
        test_order = self._create_orders(1)[0]
        resp = self.app.get('/orders/products/{}'.format(test_order.product_id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['uuid'], test_order.uuid)

    def test_get_order_not_found(self):
        """ Get an order thats not found """
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order(self):
        """ Update an existing Order """
        # create a order to update
        test_order = OrderFactory()
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = resp.get_json()
        new_order['product_id'] = 2
        resp = self.app.put('/orders/{}'.format(new_order['id']),
                            json=new_order,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_order = resp.get_json()
        self.assertEqual(updated_order['product_id'], 2)

    def test_update_order_failure(self):
        """ Update an existing Order (failure) """
        # create a order to update
        test_order = OrderFactory()
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = resp.get_json()
        new_order['product_id'] = 2
        resp = self.app.put('/orders/{}'.format(5),
                            json=new_order,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """ Delete a Order """
        test_pet = self._create_orders(1)[0]
        resp = self.app.delete('/orders/{}'.format(test_pet.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/orders/{}'.format(test_pet.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_order(self):
        """ cancel an existing Order """
        # create a order to cancel
        test_order = OrderFactory()
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # cancel the order
        new_order = resp.get_json()
        new_order['status'] = 'Cancelled'
        resp = self.app.put('/orders/{}/cancel'.format(new_order['id']),
                            json=new_order,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        cancelled_order = resp.get_json()
        self.assertEqual(cancelled_order['status'], 'Cancelled')

    def test_cancel_order_failure(self):
        """ Failure test for cancelling an existing Order """
        # create a order to cancel
        test_order = OrderFactory()
        resp = self.app.post('/orders',
                             json=test_order.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # cancel the order
        new_order = resp.get_json()
        new_order['status'] = 'Cancelled'
        resp = self.app.put('/orders/{}/cancel'.format(23),
                            json=new_order,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_server_error(self):
        """Test INTERNAL_SERVER_ERROR"""
        resp = self.app.post('/orders')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_get_order_by_customer(self):
        """ Get an order linked to customer id"""
        test_order = self._create_orders(1)[0]
        print(test_order.customer_id)
        resp = self.app.get('/orders/customers/{}'.format(test_order.customer_id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()[0]
        self.assertEqual(data['uuid'], test_order.uuid)

    def test_get_order_by_customer_fail(self):
        """ Get an order linked to customer id (FAILURE)"""
        test_order = self._create_orders(1)[0]
        print(test_order.customer_id)
        resp = self.app.get('/orders/customers/{}'.format(0),
                            content_type='application/json')
        print(resp.status_code)
        print(resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual([], resp.get_json())

    def test_order_reset(self):
        """Test reset order list by deleting all"""
        test_order = self._create_orders(1)[0]
        resp = self.app.delete('/orders/reset')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/orders/{}'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
