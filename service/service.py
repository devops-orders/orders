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
    location_url = url_for('get_order', order_id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })



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

