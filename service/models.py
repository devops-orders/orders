# Copyright 2016, 2019 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Order Service

All of the models are stored in this module

Models
------
Order - An Order used in the e-commerce app

Attributes:
-----------
uuid (string) : unique string identifier for an irder
customer_id (integer) : customer id for whom order is created
product_id (integer) : product id
price (integer) : unit price of the product
quantity (integer) : number of products items in the order

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Order(db.Model):
    """
    Class that represents an Order

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(63))
    product_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


    def save(self):
        """
        Saves a Order to the data store
        """
        Order.logger.info('Saving %s', self.uuid)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Order from the data store """
        Order.logger.info('Deleting %s', self.uuid)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Order into a dictionary """
        return {"id": self.id,
                "uuid": self.uuid,
                "customer_id": self.customer_id,
                "product_id": self.product_id,
                "price": self.price,
                "quantity": self.quantity
                }

    def deserialize(self, data):
        """
        Deserializes a Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data
        """
        try:
            self.uuid = data['uuid']
            self.customer_id = data['customer_id']
            self.product_id = data['product_id']
            self.price = data["price"]
            self.quantity = data["quantity"]
        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid order: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Orders in the database """
        cls.logger.info('Processing all Orders')
        return cls.query.all()

    @classmethod
    def find(cls, order_id):
        """ Finds a Order by it's ID """
        cls.logger.info('Processing lookup for id %s ...', order_id)
        return cls.query.get(order_id)

    @classmethod
    def find_by_product(cls, product):
        """ Returns all of the Orders linked to a product

        Args:
            product (int): the product of the Orders you want to match
        """
        cls.logger.info('Processing category query for %s ...', product)
        cls.logger.info(type(product))
        cls.logger.info(cls.query.filter(cls.product_id == product))
        return cls.query.filter(cls.product_id == product)
    

    @classmethod
    def find_or_404(cls, order_id):
        """ Find a Order by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', order_id)
        return cls.query.get_or_404(order_id)
