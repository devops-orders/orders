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
Order Service

Paths:
------
GET /orders - Returns a list all of the Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new order record in the database
PUT /orders/{id} - updates an order record in the database
DELETE /orders/{id} - deletes an order record in the database
GET /orders/customers/:customer_id - return orders for given customer
GET /orders/products/:product_id - return orders for given product
PUT /orders/cancel/:id - cancel an order for a given order id
"""

import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
# from service.models import order, DataValidationError
from service.models import Order, DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################


######################################################################
# GET INDEX
######################################################################
<<<<<<< Updated upstream
@app.route('/orders/')
def index():
    """ Root URL response """
    return jsonify(name='Order Demo REST API Service',
                   version='1.0',), status.HTTP_200_OK


######################################################################
# LIST ALL ORDERS
######################################################################

@app.route('/orders', methods=['GET'])
def list_orders():
    """ Returns all of the Orders """
    app.logger.info('Request for order list')
    orders = []
    category = request.args.get('category')
    name = request.args.get('name')
    if category:
        orders = Order.find_by_category(category)
    elif name:
        orders = Order.find_by_name(name)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER
######################################################################

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
    """
    Retrieve an order

    This endpoint will return an order based on it's id
    """
    app.logger.info('Request for an order with id: %s', order_id)
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def order_post():
    """
    Creates an order
    This endpoint will create an order based the data in the body that is posted
    """
    app.logger.info('Request to create an order')
    check_content_type('application/json')
    order = Order()
    order.deserialize(request.get_json())
    order.save()
    message = order.serialize()
    location_url = url_for('get_orders', order_id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })



######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based the body that is posted
    """
    app.logger.info('Request to update order with id: %s', order_id)
    check_content_type('application/json')
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    order.deserialize(request.get_json())
    order.id = order_id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)




######################################################################
# DELETE A ORDER
######################################################################
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    """
    Delete an Order

    This endpoint will delete an Order based the id specified in the path
    """
    app.logger.info('Request to delete an order with id: %s', order_id)
    order = Order.find(order_id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Order.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
