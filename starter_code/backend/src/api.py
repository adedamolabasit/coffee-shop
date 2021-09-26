import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

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

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drinks():
    drinks=Drink.query.order_by(Drink.id).all()
    drink_short=[drink.short() for drink in drinks]
    return jsonify({
        'success':True,
        'drinks':drink_short,

    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detailed_list():
    try:
        drinks=Drink.query.all()
        drink_long=[drink.long() for drink in drinks]
        return jsonify({
            'success':True,
            'drinks':drink_long
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def drinks_create():
    try:
        body=request.get_json()
        title_body=body.get('title',None)
        recipe_body=body.get('recipe',None)
        drinks=Drink(title=title_body,recipe=recipe_body)
        drink_create=drinks.insert()
        return jsonify({
            'success':True,
            'drinks':drink_create.long()
        })
    except:
        abort(422)





'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def drink_patial_edit(drink_id):
    try:
        drink=Drink.query.get(drink_id)
        if drink is None:
            abort(404)
        body=request.get_json()
        if 'title'.lower() in body:
            title=body.get('title',None)
        elif 'recipe'.lower() in body:
            recipe=body.get('recipe',None)
        drinks=Drink(title=title,recipe=recipe)
        

        return jsonify({
            'success':True,
            'drink':drinks.long()

        })
    except:
        abort(422)
        


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def drink_delete(drink_id):
    try:
        drink=Drink.query.get(id=drink_id)
        if drink_id == None:
             abort(404)
        drink.delete()
        return jsonify({
            'drink':drink.id
        })
    except:
         abort(404)
            




# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Bad Request"
                    }), 400
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404