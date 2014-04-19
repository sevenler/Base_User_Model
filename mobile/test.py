# coding=utf8
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json

class MobileTest(TestCase):
    
    def setUp(self):
        self.client = Client() 
    
    def test_mobile_login(self):
        response = self.client.post('/mobile/v1/register/',
                                    {'email':'johnny@gmail.com',
                                     'password':'123456',
                                     'username':'johnny',
                                     'nickname':'johnny',
                                     'api_key':'secret'});
        assert (json.loads(response.content)['session'] != None)
        
        #email重复
        response = self.client.post('/mobile/v1/register/',
                                    {'email':'johnny@gmail.com',
                                     'password':'123456',
                                     'username':'johnny',
                                     'nickname':'johnny',
                                     'api_key':'secret'});
        assert (json.loads(response.content)['type'] == 'email')
        
        #username重复
        response = self.client.post('/mobile/v1/register/',
                                    {'email':'johnny1@gmail.com',
                                     'password':'123456',
                                     'username':'johnny',
                                     'nickname':'johnny',
                                     'api_key':'secret'});
        assert (json.loads(response.content)['type'] == 'username')
        
        #nickname重复
        response = self.client.post('/mobile/v1/register/',
                                    {'email':'johnny2@gmail.com',
                                     'password':'123456',
                                     'username':'johnny1',
                                     'nickname':'johnny',
                                     'api_key':'secret'});
        assert (json.loads(response.content)['type'] == 'nickname')