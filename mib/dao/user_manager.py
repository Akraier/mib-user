from mib.dao.manager import Manager
from mib.models.user import User


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
    def retrieve_by_phone(phone):
        Manager.check_none(phone=phone)
        return User.query.filter(User.phone == phone).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    #Delete of a user --> we don't delete rows of db, we only set to false the is_active field
    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        if user is None: #to check the existance of user
            return None
        user.is_active = False # deactivate the user
        print(user.is_active)
        UserManager.update_user(user)
        return user
    
    #retrieve all users in the DB filtering 
    @staticmethod
    def retrieve_all():
        return User.query.all()