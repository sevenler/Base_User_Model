# -*- coding: UTF-8 -*- 
from django.db import models
from djangosphinx.models import SphinxSearch
from django.contrib.auth.models import User


class User_Profile(models.Model):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, u'男'),
        (Woman, u'女'),
        (Other, u'其他')
    )
    
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=64, db_index=True, unique=True)
    location = models.CharField(max_length=32, null=True, default=u'北京')
    city = models.CharField(max_length=32, null=True, default=u'朝阳')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=Other)
    bio = models.CharField(max_length=1024, null=True, blank=True)
    website = models.CharField(max_length=1024, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
 
    search = SphinxSearch(
        index='users',
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )
     
    def __unicode__(self):
        return self.nickname
    
class Avatar(models.Model):
    user = models.OneToOneField(User)
    avatar_origin = models.CharField(max_length = 1024, null = False, blank = False)
    avatar_small = models.CharField(max_length = 1024, null = False, blank = False)
    avatar_large = models.CharField(max_length = 1024, null = False, blank = False)
    uploaded_time = models.DateField(auto_now_add = True)
    
    class Meta:
        ordering = ['-uploaded_time']