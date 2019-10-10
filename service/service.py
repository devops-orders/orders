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



######################################################################
# RETRIEVE AN ORDER

######################################################################



######################################################################
# ADD A NEW ORDER

######################################################################


######################################################################
# UPDATE AN EXISTING ORDER


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
