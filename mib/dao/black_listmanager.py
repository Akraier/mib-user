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
        result = jsonify({ "black_list": l}), 200
        return result

    @staticmethod
    def delete_blacklist(user_id):

        black_list = db.session.query(blacklist.c.user_id).filter(blacklist.c.user_id==user_id).first()
        if black_list is not None:
            #clear only if the blacklist is not empty
            st = blacklist.delete().where(blacklist.c.user_id == user_id)
            db.session.execute(st)   
            db.session.commit()
            black_list = db.session.query(blacklist).filter(blacklist.c.user_id == user_id).all()
            return jsonify({'status':'Your blacklist is now Empty','content': []}), 200  
        else:
            return jsonify({'status':'Your blacklist already now Empty','content': []}), 201
            
   
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

 #Delete from the blacklist
    @staticmethod
    def delete_id(user_id,black_id):
        print(user_id, black_id)
        u1 = UserManager.retrieve_by_id(user_id)
        u2 = UserManager.retrieve_by_id(black_id)
        if u1 is not None and u2 is not None:
                #Deleteblack_id from current user's blacklist
                bl_target = db.session.query(blacklist).filter((blacklist.c.user_id == user_id)&(blacklist.c.black_id ==black_id)).first()
                if bl_target is not None:
                    #check thatblack_id is already into the black list 
                    st = blacklist.delete().where((blacklist.c.user_id == user_id)&(blacklist.c.black_id ==black_id))
                    db.session.execute(st)
                    db.session.commit()
                    user_bl = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id).all()
                    result = [user.serialize() for user in user_bl]
                    l = aux_filter(result)
                    return jsonify({'status':'Target removed from the blacklist', 'content': l }),200
                else:
                    user_bl = db.session.query(User).filter(blacklist.c.user_id == user_id).filter(blacklist.c.black_id == User.id).all()
                    result = [user.serialize() for user in user_bl]
                    l = aux_filter(result)
                    return jsonify({'status':'This user is not in your blacklist!','content': l}), 200    
        else:
            #User orblack_id not in db
            return jsonify({'status':'Please check that you select a correct user'}),404
         
      


   

def aux_filter(result):
        l = []
        for i in result:
            Dict = dict()
            print(i)
            Dict['id']=i.get('id')
            Dict['email']=i.get('email')
            Dict['firstname']=i.get('firstname')
            Dict['lastname']=i.get('lastname')
            l.append(Dict)
        return l

    

   
    
  