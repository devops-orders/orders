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

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()



    def tearDown(self):
        db.session.remove()
        db.drop_all()


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
        resp = self.app.get('/orders/', 
                            content_type='application/json')
        print(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_order(self):
        """ Get a single order """
        test_order = self._create_orders(1)[0]
        resp = self.app.get('/orders/{}'.format(test_order.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['uuid'], test_order.uuid)

    def test_get_order_not_found(self):
        """ Get an order thats not found """
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)