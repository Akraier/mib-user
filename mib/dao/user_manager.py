from mib.dao.manager import Manager
from mib.models.user import User
from datetime import datetime

class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()
    

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def ban(user:User):
        user.ban_expired_date = datetime.today + datetime.timedelta(days=3)
        user.n_report = 0
        UserManager.update_user(user)
    @staticmethod
    def report(user:User):
        user.n_report += 1
        UserManager.update_user(user)
        
    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    #retrieve all users in the DB filtering 
    @staticmethod
    def retrieve_all():
        return User.query.all()