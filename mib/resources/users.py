from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.models.user import User
from datetime import datetime


def create_user():
    """This method allows the creation of a new user.
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = User()
    birthday = datetime.strptime(post_data.get('birthdate'),'%d/%m/%Y')
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(birthday)
    #user.set_phone(post_data.get('phone'))
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201

def get_list_of_users():
    """
    Retreive a list of every user in the db
    """
    list_user = UserManager.retrieve_all() #see if list_user is a list of User objs
    if list_user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    
    result = {}
    for user in list_user:
        val = {user.id : jsonify(user.serialize())}
        result.update(val)
    return jsonify(result), 200

def get_user(user_id):
    """
    Get a user by its current id.

    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_user_by_email(user_email):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def delete_user(user_id):
    """
    Delete the user with id = user_id.

    :param user_id the id of user to be deleted
    :return json response
    """
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202

def report_user(user_id):
    UserManager.report_user(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully reported',
    }
    return jsonify(response_object),202
