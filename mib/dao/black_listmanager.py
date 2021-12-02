from flask.json import jsonify
from mib.dao.manager import Manager
from mib.models.user import User,blacklist
from mib.dao.user_manager import UserManager
from mib import db

class BlackListManager(Manager):

   
    
    #retrieve the list of blacklist
    @staticmethod
    def retrive_blacklist(user_id):
        _user = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id)
        if _user is None:
            response = {'status': 'Cannot retrieve the list of blacklist'}
            return jsonify(response), 404
    
        result = [user.serialize() for user in _user]
        l = aux_filter(result)
        result = jsonify({ "users_list": l}), 200
        return result


     #Insert in the blacklist
    @staticmethod
    def insert_id(user_id,black_id):
        print(user_id, black_id)
        u1 = UserManager.retrieve_by_id(user_id)
        u2 = UserManager.retrieve_by_id(black_id)
        if u1 is not None and u2 is not None:
            #Query the blacklist and check that the user is not already in the blacklist
            inside =  db.session.query(blacklist).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == black_id).first()
            if inside is None: #the user is NOT already in the blacklist
                 u1.black_list.append(u2)
                 db.session.commit()
                 user_bl = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id).all()
                 result = [user.serialize() for user in user_bl]
                 l = aux_filter(result)
                 return jsonify({'status':'Target added to the blacklist', 'content': l }),200
            else:
                #The user is already in blacklist
                user_bl = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id).all()
                result = [user.serialize() for user in user_bl]
                l = aux_filter(result)
                return jsonify({'status':'This user is already in your blacklist!','content': l}), 200    
        else:
            return jsonify({'status':'Please check that you select a correct user'}),404

       

def aux_filter(result):
        l = []
        for i in result:
            Dict = dict()
            print(i)
            Dict['email']=i.get('email')
            Dict['firstname']=i.get('firstname')
            Dict['lastname']=i.get('lastname')
            l.append(Dict)
        return l

    

   
    
  