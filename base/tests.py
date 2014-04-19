# coding=utf8
from django.test import TestCase

from base.user import User


class UserTest(TestCase):
    
    @staticmethod
    def assert_exception(do, exception_type):
        try:
            do()
        except Exception, e:
            if (type(e) !=  exception_type):
                print type(e)
                assert (type(e) ==  exception_type)
    
    @staticmethod            
    def print_user(user):
        print user.get_username(), user.get_email(), user.get_profile().nickname, user.get_profile().location, user.get_profile().city, user.get_profile().city, user.get_profile().bio, user.get_profile().website;
    
    def setUp(self):
        User.create('johnnyxyzw@gmail.com', '123456', 'johnny');

    def test_base_user_login(self):
        UserTest.assert_exception((lambda : User.login('johnnyxyzw@gmail.com', '23456')), User.LoginPasswordIncorrect)
        UserTest.assert_exception((lambda : User.login('john@gmail.com', '23456')), User.LoginEmailDoesNotExist)
        User.login('johnnyxyzw@gmail.com', '123456')

    def test_base_user_create(self):
        UserTest.assert_exception((lambda : User.create('johnnyxyzw@gmail.com', '123456', 'johnny')), User.EmailExistAlready)
            
    def test_base_user_profile(self):
        user = User.login('johnnyxyzw@gmail.com', '123456')
        user.set_profile('johnny', location='北京', city = '朝阳', gender='M', bio='我是你大爷', website='www.baidu.com');
        UserTest.print_user(user)
        
        us = User.create('johnnyxyzw2@gmail.com', '123456', 'johnny1')
        UserTest.assert_exception((lambda:us.set_profile('johnny')), User.NicknameExistAlready)
        us.set_profile('johnny2');
        UserTest.print_user(us)
        


