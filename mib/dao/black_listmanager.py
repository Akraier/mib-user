from flask.json import jsonify
from mib.dao.manager import Manager
from mib.models.user import User,blacklist
from mib.dao.user_manager import UserManager
from mib import db

class BlackListManager(Manager):

   
    
    #retrieve all users in the DB filtering 
    @staticmethod
    def retrive_blacklist(user_id):
        _user = db.session.query(User.id, User.email,User.firstname,User.lastname,blacklist).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id)
        return _user

     #retrieve all users in the DB filtering 
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
                 print(user_bl)
                 result = [user.serialize() for user in user_bl]
                 return jsonify({'status':'Target added to the blacklist', 'content': result }),200
            else:
                user_bl = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id).all()
                print(user_bl)
                result = [user.serialize() for user in user_bl]
                return jsonify({'status':'This user is already in your blacklist!','content': result}), 200    
        else:
            return jsonify({'status':'Please check that you select a correct user'}),404

       
    
    # if existUser is not None and existTarget is not None and current_user.id != target: 
    #             inside = db.session.query(blacklist).filter(blacklist.c.user_id == current_user.id).filter(blacklist.c.black_id == target).first()
    #             if inside is None: #the user is NOT already in the blacklist
    #                 existUser.black_list.append(existTarget)
    #                 db.session.commit()
    #                 user_bl = db.session.query(User.email,User.firstname,User.lastname,blacklist).filter(blacklist.c.user_id == current_user.id).filter(blacklist.c.black_id == User.id)
    #                 return render_template('black_list.html',action="User "+target+" added to the black list.",black_list = user_bl)
    #             else: #target already in the blacklist
    #                 user_bl = db.session.query(User.email,User.firstname,User.lastname,blacklist).filter(blacklist.c.user_id == current_user.id).filter(blacklist.c.black_id == User.id)
    #                 return render_template('black_list.html',action="This user is already in your blacklist!",black_list = user_bl)
    #         else:
    #             #User or Target not in db
    #             return render_template('black_list.html',action="Please check that you select a correct user",black_list=[])  
    
  