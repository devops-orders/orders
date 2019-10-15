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
Pet Store Service

Paths:
------
GET /pets - Returns a list all of the Pets
GET /pets/{id} - Returns the Pet with a given id number
POST /pets - creates a new Pet record in the database
PUT /pets/{id} - updates a Pet record in the database
DELETE /pets/{id} - deletes a Pet record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
# from service.models import Pet, DataValidationError
from service.models import Pet, DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################


######################################################################
# GET INDEX

######################################################################


######################################################################
# LIST ALL ORDERS

######################################################################



######################################################################
# RETRIEVE AN ORDER

######################################################################



######################################################################
# ADD A NEW ORDER

######################################################################


######################################################################
# UPDATE AN EXISTING ORDER
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



######################################################################
# DELETE A ORDER


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """


def check_content_type(content_type):
    """ Checks that the media type is correct """


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
