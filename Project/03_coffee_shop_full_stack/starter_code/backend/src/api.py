from crypt import methods
import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth
from .database.models import (
    db,
    db_drop_and_create_all,
    Drink,
    setup_db
)

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()


# -----------------------------API Endpoints----------------------------- #

BASE_URL = '/api/v1'

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate
        status code indicating reason for failure
'''


@app.route(f'{BASE_URL}/drinks', methods=['GET'])
def retrieve_all_drinks():
    # Handle data
    try:
        drinks = db.session.query(Drink).all()
        formatted_drinks = [drink.short() for drink in drinks]
    except BaseException:
        print(sys.exc_info())
        abort(500)

    # Handle response
    return jsonify({
        'success': True,
        'status_code': 200,
        'drinks': formatted_drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate
        status code indicating reason for failure
'''


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate
        status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate
        status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate
        status code indicating reason for failure
'''


# -----------------------------Error Handling----------------------------- #

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(405)
def methhod_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(422)
def unporcessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable entity'
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'requested resource not found'
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    # Determine error code (401, 403)
    status_code = error.status_code

    # Handle response
    return (get_401_error_response(error) if status_code == 401
            else get_403_error_response(error))


def get_401_error_response(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized request',
    }), 401


def get_403_error_response(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'forbidden request',
    }), 403
