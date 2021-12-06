from flask import json
from .view_test import ViewTest
from faker import Faker


class TestUsers(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()

    def test_delete_user(self):
        user = self.login_test_user()
        rv = self.client.delete('/user/%d' % user.id)
        assert rv.status_code == 202

    def test_get_user_by_id(self):
        # get a non-existent user
        rv = self.client.get('/user/0')
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
        _data = {
            "birthdate": user.date_of_birth,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "password": user.password,
            "phone": user.phone
        }
        rv = self.client.put("/user/%d" % user.id, json=_data)
        print(rv.status_code)

        #update with wrong password

    
    def test_get_black_list(self):
        #get the blacklist
        rv = self.client.get("/user/blacklist/%d"%0)
        print(rv)
        assert rv.status_code == 200
         #get the blacklist
        rv = self.client.get("/user/blacklist/%d")
        print(rv)
        assert rv.status_code == 404
    
    def test_delete_blacklist(self):
        #delete the blacklist
        rv = self.client.delete("/user/blacklist/%d"%0)
        assert rv.status_code == 200
         #delete the blacklist
        rv = self.client.delete("/user/blacklist/%d")
        assert rv.status_code == 404
    
    def test_insert_target_black_id(self):
        #Adding a target to a non existing user
        _data = {
            "black_id": 0,
            "user_id": 0
            }

        rv = self.client.post("/user/blacklist/target", json= _data)
        #Insert an element in the blacklistù
        user = self.login_test_user()
        data = {
            "black_id": user.id,
            "user_id": user.id
            }

        rv = self.client.post("/user/blacklist/target", json= data)
        assert rv.status_code == 200

    def test_delete_target_black_id(self):
            #Adding a target to a non existing user
            _data = {
                "black_id": 0,
                "user_id": 0
                }

            rv = self.client.delete("/user/blacklist/target", json= _data)
            #Insert an element in the blacklistù
            user = self.login_test_user()
            data = {
                "black_id": user.id,
                "user_id": user.id
                }

            rv = self.client.delete("/user/blacklist/target", json= data)
            assert rv.status_code == 200



        

       




        
        

