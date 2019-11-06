"""
Test cases for Order Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
import uuid
from werkzeug.exceptions import NotFound
from service.models import Order, DataValidationError, db
from service import app

DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/test')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrders(unittest.TestCase):
    """ Test Cases for Orders """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Order.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_order(self):
        """ Create a order and assert that it exists """
        uuid_str = str(uuid.uuid4())
        order = Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1)
        self.assertTrue(order != None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.uuid, uuid_str)
        self.assertEqual(order.product_id, 1)
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(order.price, 10)
        self.assertEqual(order.quantity, 1)

    def test_add_a_order(self):
        """ Create a order and add it to the database """
        orders = Order.all()
        self.assertEqual(orders, [])
        uuid_str = str(uuid.uuid4())
        order = Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1)
        self.assertTrue(order != None)
        self.assertEqual(order.id, None)
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_update_a_order(self):
        """ Update an Order """
        uuid_str = str(uuid.uuid4())
        order = Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1)
        order.save()
        self.assertEqual(order.id, 1)
        # Change it an save it
        order.product_id = 2
        order.save()
        self.assertEqual(order.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].product_id, 2)

    def test_delete_a_order(self):
        """ Delete an Order """
        uuid_str = str(uuid.uuid4())
        order = Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1)
        order.save()
        self.assertEqual(len(Order.all()), 1)
        # delete the order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_a_order(self):
        """ Test serialization of an Order """
        uuid_str = str(uuid.uuid4())
        order = Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1)
        data = order.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('uuid', data)
        self.assertEqual(data['uuid'], uuid_str)
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], 1)
        self.assertIn('customer_id', data)
        self.assertEqual(data['customer_id'], 1)
        self.assertIn('price', data)
        self.assertEqual(data['price'], 10)
        self.assertIn('quantity', data)
        self.assertEqual(data['quantity'], 1)

    def test_deserialize_a_order(self):
        """ Test deserialization of an Order """
        data = {"uuid" : "2edf8761-0c1f-4039-9f5c-907a5a03f39c","product_id" : 1,"customer_id" : 1,"price" : 10,"quantity" : 1, "status": "In Progress"}
        order = Order()
        order.deserialize(data)
        self.assertNotEqual(order, None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.uuid, "2edf8761-0c1f-4039-9f5c-907a5a03f39c"),
        self.assertEqual(order.product_id, 1),
        self.assertEqual(order.customer_id, 1),
        self.assertEqual(order.price, 10),
        self.assertEqual(order.quantity, 1)


    # def test_get_order_customerid(self):
    #     """ Tests get a single order by customer id"""
    #     # get the customer id of an order
    #     test_order = self._create_orders(1)[0]
    #     resp = self.app.get('/orders/customers/{}'.format(test_order.customer_id),
    #                         content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     data = resp.get_json()
    #     self.assertEqual(data['uuid'], test_order.name)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_find_order(self):
        """ Find an Order by ID """
        uuid_str = str(uuid.uuid4())
        Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1).save()
        next_order = Order(uuid = "2edf8761-0c1f-4039-9f5c-907a5a03f39c", product_id = 1, customer_id = 1, price = 10, quantity = 1)
        next_order.save()
        order = Order.find(next_order.id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, next_order.id)
        self.assertEqual(order.uuid, "2edf8761-0c1f-4039-9f5c-907a5a03f39c")
        self.assertEqual(order.product_id, 1),
        self.assertEqual(order.customer_id, 1),
        self.assertEqual(order.price, 10),
        self.assertEqual(order.quantity, 1)
    
    def test_find_order_by_product(self):
        """ Find an Order by Product ID """
        uuid_str = str(uuid.uuid4())
        Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1).save()
        next_order = Order(uuid = "2edf8761-0c1f-4039-9f5c-907a5a03f39c", product_id = 2, customer_id = 1, price = 10, quantity = 1)
        next_order.save()
        order = Order.find_by_product(2)[0]
        self.assertIsNot(order, None)
        self.assertEqual(order.id, next_order.id)
        self.assertEqual(order.uuid, "2edf8761-0c1f-4039-9f5c-907a5a03f39c")
        self.assertEqual(order.product_id, 2),
        self.assertEqual(order.customer_id, 1),
        self.assertEqual(order.price, 10),
        self.assertEqual(order.quantity, 1)
    
    

    

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        uuid_str = str(uuid.uuid4())
        Order(uuid=uuid_str, product_id = 1, customer_id = 1, price = 10, quantity = 1).save()
        next_order = Order(uuid = "2edf8761-0c1f-4039-9f5c-907a5a03f39c", product_id = 1, customer_id = 1, price = 10, quantity = 1)
        next_order.save()
        order = Order.find_or_404(next_order.id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, next_order.id)
        self.assertEqual(order.uuid, "2edf8761-0c1f-4039-9f5c-907a5a03f39c")
        self.assertEqual(order.product_id, 1),
        self.assertEqual(order.customer_id, 1),
        self.assertEqual(order.price, 10),
        self.assertEqual(order.quantity, 1)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Order.find_or_404, 0)
