# coding=utf8
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as AuthUser
from django.db.utils import IntegrityError

from models import User_Profile


class User(object):
    
    class PasswordLessIllegal(Exception):
        def __init__(self):
            self.__message = "password illegal"
        def __str__(self):
            return repr(self.__message)

    class LoginEmailDoesNotExist(Exception):
        def __init__(self, email):
            self.__message = "login email \'%s\' is not exist" % email
        def __str__(self):
            return repr(self.__message)
    
    class LoginPasswordIncorrect(Exception):
        def __init__(self):
            self.__message = "login password is incorrect"
        def __str__(self):
            return repr(self.__message)
    
    class EmailExistAlready(Exception):
        def __init__(self, email):
            self.__message = "email \'%s\' is exist" % email
        def __str__(self):
            return repr(self.__message)
    
    class EmailDoesNotExist(Exception):
        def __init__(self, email):
            self.__message = "email \'%s\' does not exist" % email
        def __str__(self):
            return repr(self.__message)
    
    class NicknameExistAlready(Exception):
        def __init__(self, nickname):
            self.__message = "nickname \'%s\' is exist" % nickname
        def __str__(self):
            return repr(self.__message)
        
    class UsernameExistAlready(Exception):
        def __init__(self, username):
            self.__message = "username \'%s\' is exist" % username
        def __str__(self):
            return repr(self.__message)
        
    def __init__(self, user_id):
        self.user_id = int(user_id) 
    
    def __ensure_user_obj(self):
        if not hasattr(self, 'user_obj'):
            self.user_obj = AuthUser.objects.get(pk = self.user_id)
    
    def __ensure_user_profile_obj(self):
        if not hasattr(self, 'user_profile_obj'):
            try:
                self.user_profile_obj = User_Profile.objects.get(user_id = self.user_id)
            except User_Profile.DoesNotExist:
                self.user_profile_obj = None
                
    def get_username(self):
        self.__ensure_user_obj()
        return self.user_obj.username
    
    def get_email(self):
        self.__ensure_user_obj()
        return self.user_obj.email
    
    def get_profile(self):
        self.__ensure_user_profile_obj()
        return self.user_profile_obj;
    
    def read(self):
        self.__ensure_user_obj()
        self.__ensure_user_profile_obj()
        
        _basic_info = {}
        _basic_info['email'] = self.user_obj.email;
        _basic_info['username'] = self.user_obj.username;
        
        _basic_info['nickname'] = self.user_profile_obj.nickname;
        _basic_info['location'] = self.user_profile_obj.location;
        _basic_info['city'] = self.user_profile_obj.city;
        _basic_info['bio'] = self.user_profile_obj.bio;
        _basic_info['gender'] = self.user_profile_obj.gender;
        _basic_info['website'] = self.user_profile_obj.website;
        
        return _basic_info
    
    def check_auth(self, password):
        self.__ensure_user_obj()
        if authenticate(username = self.get_username(), password = password):
            return True
        return False
    
    def set_profile(self, nickname, location = u'', city = u'', gender = 'O', bio = '', website = ''):
        if nickname != None:
            nickname = nickname.strip()
            if User.nickname_exist(nickname):
                    raise User.NicknameExistAlready(nickname)

        self.__ensure_user_profile_obj()
        
        if self.user_profile_obj == None:
            _user_profile_obj = User_Profile.objects.create(
                user_id = self.user_id,
                nickname = nickname.strip(),
                location = location,
                city = city,
                gender = gender,
                bio = bio,
                website = website
            )
            self.user_profile_obj = _user_profile_obj
        else:
            if nickname != None:
                self.user_profile_obj.nickname = nickname.strip()
            if location != None:
                self.user_profile_obj.location = location.strip()
            if city != None:
                self.user_profile_obj.city = city.strip()
            if bio != None:
                self.user_profile_obj.bio = bio.strip()
            if website != None:
                self.user_profile_obj.website = website.strip()
            if gender != None:
                self.user_profile_obj.gender = gender.strip()
            self.user_profile_obj.save()
        
    def delete(self):
        self.__ensure_user_obj()
        self.user_obj.delete()
        
    @staticmethod
    def nickname_exist(nickname):
        try:
            User_Profile.objects.get(nickname = nickname)
            return True
        except User_Profile.DoesNotExist, e:
            return False

    @classmethod
    def login(cls, email, password):
        try:
            _user_obj = AuthUser.objects.get(email = email)
        except AuthUser.DoesNotExist, e:
            raise User.LoginEmailDoesNotExist(email)

        _inst = cls(_user_obj.id)
        _inst.user_obj = _user_obj
        
        if not _inst.check_auth(password):
            raise User.LoginPasswordIncorrect()
        return _inst
    
    @staticmethod
    def email_exist(email):
        if AuthUser.objects.filter(email = email).count() > 0:
            return True
        return False
    
    @classmethod
    def create(cls, email, password, username = ''):
        if User.email_exist(email):
            raise User.EmailExistAlready(email) 

        try:
            _user = AuthUser.objects.create(username = username, email = email)
            _user.set_password(password)
            _user.save()
            _inst = cls(_user.id)
            return _inst
        except IntegrityError:
            raise User.UsernameExistAlready(username)
