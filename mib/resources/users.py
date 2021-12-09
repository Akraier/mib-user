from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.models.user import User
from datetime import datetime as dt
from mib.dao.black_listmanager import BlackListManager

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
    birthday = dt.strptime(post_data.get('birthdate'),'%d/%m/%Y')
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('firstname'))
    user.set_last_name(post_data.get('lastname'))
    user.set_birthday(birthday)
    user.set_phone(post_data.get('phone'))
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
        response = {'status': 'Cannot retrieve the list of users'}
        return jsonify(response), 404
    
    result = [user.serialize() for user in list_user]
    
    return jsonify({ "users_list": result}), 200

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



#TO MODIFY
def delete_user(user_id):
    """
    Delete the user with id = user_id.
    Our delete is to set the "is_active" field to False.

    :param user_id the id of user to be deleted
    :return json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404
    else:
        user.is_active = False # deactivate the user
        UserManager.update_user(user)
        response = {
            'status': 'success',
            'message': 'Successfully deleted',
        }
        return jsonify(response), 202

def content_filter():
    putdata = request.get_json()
    user = UserManager.retrieve_by_id(putdata.get('id'))
    
    user.filter_isactive = putdata.get('filter')
    UserManager.update_user(user)
    response = {
        'status': 'success',
        'message': 'Successfully updated content filter',
    }
    return jsonify(response), 200

def report_user(user_id):
    #Check the count of n report, if threshold passed ban the user, else increase the n of report
    threshold_ban = 3
    user = UserManager.retrieve_by_id(user_id)
    if not user:
        return {'message':'User not found'}, 404
    if user.n_report == threshold_ban - 1:
        #ban the user
        UserManager.ban(user)
        message = 'User banned'
        return {'message':message}, 201
    else:
        UserManager.report(user)
        message = 'User reported'
        return {'message':message}, 200
    

#to update a user profile (used for myaccount/modify)
def update_user(user_id):
    new_data = request.get_json()
    user = UserManager.retrieve_by_id(user_id)
    current_psw = new_data.get('password')
    new_psw = new_data.get('newpassword')
    if current_psw != new_psw and new_psw != "":
        #check that the password has been changed with a valid value before update
        user.set_password(new_psw)
    
    user.email = new_data.get('email')
    user.firstname = new_data.get('firstname')
    date_string = new_data.get('birthdate')
    date_obj_datetime = dt.strptime(date_string, '%d/%m/%Y').date()
    user.date_of_birth = date_obj_datetime
    user.lastname = new_data.get('lastname')
    
    UserManager.update_user(user)
    
    response_object = {
        'status': 'success',
        'message': 'Successfully updated',
    }
    
    return jsonify(response_object), 200

#Get the list of Blacklist
def get_blacklist(user_id):
    """
    Retreive the blacklist
    """
    response = BlackListManager.retrive_blacklist(user_id)
    
    return response
    


# Insert a value in the blacklist
def post_blacklist_target():
    """
    Insert the Target inside the blacklist
    """
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    black_id = post_data.get('black_id')

    return BlackListManager.insert_id(user_id,black_id)
    
#Delete the black-list
def delete_blacklist(user_id):
    return BlackListManager.delete_blacklist(user_id)

# Delete a user in the blacklist
def delete_target_blacklist():
    """
    Delete the target inside the blacklist
    """
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    black_id = post_data.get('black_id')

    return BlackListManager.delete_id(user_id,black_id)



