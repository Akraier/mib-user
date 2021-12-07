from flask import json
from .view_test import ViewTest
from faker import Faker


class TestUsers(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()
        
    def test_create_user(self):
        #create a new user
        _data = {
            "birthdate": "2/2/1980",
            "email": "nonesisto@gmail.com",
            "firstname": "nonesisto",
            "lastname": "nonesisto",
            "password": "1234567890",
            "phone": "4455667788"
        }
        rv = self.client.post('/create_user', json=_data)
        assert rv.status_code == 201
        

    def test_delete_user(self):
        user = self.login_test_user()
        rv = self.client.delete('/user/%d' % user.id)
        assert rv.status_code == 202

    def test_get_user_by_id(self):
        # get a non-existent user
        rv = self.client.get('/user/%d' % 987)
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user/%d' % user.id)
        assert rv.status_code == 200

    def test_get_user_by_email(self):
        # get a non-existent user with faked email
        rv = self.client.get('/user_email/%s' % TestUsers.faker.email())
        assert rv.status_code == 404
        # get an existent user
        user = self.login_test_user()
        rv = self.client.get('/user_email/%s' % user.email)
        assert rv.status_code == 200
    
    def test_get_list_user(self):
        # get the list of user
        rv = self.client.get('/users')
        print(rv.status_code)
        assert rv.status_code == 200

    def test_set_content(self):
        #put to true the content filter
        user = self.login_test_user()
        _data = {
            "filter": True,
            "id": user.id
            }
        
        rv = self.client.put('/myaccount/set_content', json=_data)
        print(rv.status_code)
        assert rv.status_code == 200

    def test_update_user(self):
        #update the user
        user = self.login_test_user()
        '''_data = {
            "birthdate": user.date_of_birth,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "password": user.password,
            "phone": user.phone
        }'''
        rv = self.client.put('/user/%d' % user.id, 
            json = {
                "birthdate": "2/2/1980",
                "email": str(user.email),
                "firstname": str(user.firstname),
                "lastname": str(user.lastname),
                "password": str(user.password),
                "newpassword": str(user.password),
            }
            
            )
        print(rv.status_code)


    
    def test_get_black_list(self):
        user = self.login_test_user()
        
        #get the blacklist
        rv = self.client.get("/user/blacklist/%d"%0)
        print(rv)
        assert rv.status_code == 200
        
        '''#get the blacklist
        rv = self.client.get("/user/blacklist/%d" % 987)
        print(rv.data)
        assert rv.status_code == 404'''
    
    def test_delete_blacklist_alrdy_empty(self):
        #delete the blacklist
        rv = self.client.delete("/user/blacklist/%d"%0)
        assert rv.status_code == 201 #blacklist already empty
        #delete the blacklist
        rv = self.client.delete("/user/blacklist/%d")
        assert rv.status_code == 404
        
    
    def test_insert_target_black_id_and_delete_NotEmpty(self):
       
        #Insert an element in the blacklistù
        user = self.login_test_user()
        data = {
            "black_id": 2,
            "user_id": user.id
            }

        rv = self.client.post("/user/blacklist/target", json= data)
        assert rv.status_code == 200
        
        #deleting that user from the blacklist
        rv = self.client.delete("/user/blacklist/%d"% user.id)
        assert rv.status_code == 200 #blacklist was not empty
        
        rv = self.client.post('/report_user/%d' % user.id)
        assert rv.status_code == 202

    def test_insert_target_already_in_black_and_delete_target(self):
           
        #Insert an element in the blacklistù
        user = self.login_test_user()
        
        rv = self.client.get("/user/blacklist/%d"% user.id)
        print("\n")
        print("o" * 30)
        print("UTENTE: ", user.id)
        print(rv.data)
        print("o" * 30)
        
        data = {
            "black_id": 2,
            "user_id": user.id
            }

        rv = self.client.post("/user/blacklist/target", json= data)
        assert rv.status_code == 200
        
        rv = self.client.get("/user/blacklist/%d"% user.id)
        print("a" * 30)
        print("UTENTE: ", user.id)
        print(rv.data)
        print("a" * 30)
        
        #Insert again
        data = {
            "black_id": 2,
            "user_id": user.id
            }

        rv = self.client.post("/user/blacklist/target", json= data)
        
        print("g" * 30)
        print("UTENTE: ", user.id)
        print(rv.data)
        print("g" * 30)
        
        assert rv.status_code == 200
        
        #Insert using two unknown ids
        data = {
            "black_id": 99,
            "user_id": 98
            }
        
        rv = self.client.post("/user/blacklist/target", json= data)
        assert rv.status_code == 404
        
        
        #delete the user 2 from blacklist
        _data = {
            "black_id": 2,
            "user_id": user.id
            }
        rv = self.client.delete("/user/blacklist/target", json= _data)
        assert rv.status_code == 200
        
        #delete again the user 2 that is no more in blacklist
        _data = {
            "black_id": 2,
            "user_id": user.id
            }
        rv = self.client.delete("/user/blacklist/target", json= _data)
        assert rv.status_code == 200
        
        
        #delete a non existent user from blacklist
        _data = {
            "black_id": 99,
            "user_id": user.id
            }
        rv = self.client.delete("/user/blacklist/target", json= _data)
        assert rv.status_code == 404
        
        



        

       




        
        

