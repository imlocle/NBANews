# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):
        errorlist = []
        the_user = User.objects.filter(email = email)

        if len(first_name) < 2:
            errorlist.append("First name is too short")            
        if len(last_name) < 2:
            errorlist.append("Last name is too short")           
        if not EMAIL_REGEX.match(email):
            errorlist.append('Please enter a valid email') 
        if the_user:
            errorlist.append("Email already taken")           
        if confirm_password != password:
            errorlist.append("Passwords don\'t match")
        if len(password) < 8:
            errorlist.append("Please enter a password longer than 8 characters")
        if (errorlist.count) > 0:
            return errorlist
        else:
            return True

    def login(self, email, password):
        errorlist = []
        the_user = User.objects.filter(email = email)
        if the_user:
            if bcrypt.hashpw(password.encode('utf-8'), the_user[0].password.encode('utf-8')) == the_user[0].password:
                return True
            else:
                errorlist.append("Wrong email or password")
                return errorlist
        else:
            errorlist.append("Wrong email or password")
            return errorlist

class CommentManager(models.Manager):
    def create_comment(self, create_comment):
        curse_words = [
            re.compile("fuck"),
            re.compile("shit"),
            re.compile("cunt")
        ]
        errorlist = []
        if len(create_comment) < 2:
            errorlist.append("Comment is too short.")
        if len(create_comment) > 200:
            errorlist.append("Comment is too long.")
        if (regex.match(create_comment) for regex in curse_words):
            errorlist.append("Let's be a little bit more mature please.")
        if len(errorlist) > 0:
            return errorlist
        else:
            return True


class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name= 'user_to_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()



