from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import bcrypt

from mib import db

blacklist = db.Table('blacklist',
    
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True), # actual user id
    db.Column('black_id', db.Integer, db.ForeignKey('User.id'), primary_key=True), # blocked user id
)

class User(db.Model):
    """Representation of User model."""

    # The name of the table that we explicitly set
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'firstname', 'lastname', 'is_active', 'authenticated', 'is_anonymous', 'ban_expired_date', 'filter_isactive', 'n_report', 'date_of_birth']

    # All fields of user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    firstname = db.Column(db.Unicode(128), nullable=False, unique=False)
    lastname = db.Column(db.Unicode(128), nullable=False, unique=False)
    password = db.Column(db.Unicode(128)) # To avoid having warining. We store binary datas for the password (the result of bcrypt.hashpw)
    date_of_birth = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True) # To know if a user is active, in the sense that its account is not deleted
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False
    authenticated = db.Column(db.Boolean, default=True)
    phone = db.Column(db.Unicode(128), nullable=False, unique=True)

    filter_isactive = db.Column(db.Boolean, default=False) #content filter for user
    n_report = db.Column(db.Integer, default = 0) #number of report that the user received 
    ban_expired_date = db.Column(db.DateTime, default = None) #data a cui finisce il ban dell'utente
    lottery_ticket_number = db.Column(db.Integer, default = -1) #lottery ticker number 0-99
    lottery_points = db.Column(db.Integer, default = 0) #points gained with the monthly lottery

    black_list = relationship('User',
    secondary=blacklist,
    primaryjoin=id==blacklist.c.user_id,
    secondaryjoin=id==blacklist.c.black_id,
    backref="user_id",
    lazy = 'dynamic')

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.authenticated = False

    def set_email(self, email):
        self.email = email
    
    def set_first_name(self, firstname):
        self.firstname = firstname

    def set_last_name(self, lastname):
        self.lastname = lastname

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA -----------------> " + self.password)
        
    def set_birthday(self, birthday):
        self.date_of_birth = birthday

    def is_authenticated(self):
        return self.authenticated

    def set_phone(self, phone):
        self.phone = phone

    def authenticate(self, password):
        #checked = check_password_hash(self.password, password) OLD
        checked = bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')) #check password hash and salt
        self.authenticated = checked
        return self.authenticated

    def get_id(self):
        return self.id

    def serialize(self):
        return dict([(k,self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
