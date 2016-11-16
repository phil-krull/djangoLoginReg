from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def add_user(self, postData):
        print postData
        errors = []
        if len(postData['first_name']) < 2:
            # add errors
            errors.append('First Name must be at least 2 characters long.')
        if len(postData['last_name']) < 2:
            # add errors
            errors.append('Last Name must be at least 2 characters long.')
        if not postData['email']:
            errors.append('Email field is required')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Enter a valid email')
        if len(postData['password']) < 8:
            errors.append('Password field must be at least 8 characters long.')
        if not postData['password'] == postData['confirm_password']:
            errors.append('Password fields must match')
        user = self.filter(email=postData['email'])
        if user:
            errors.append('Email already exists')

        response = {}

        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = self.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'],password=password)
            response['status'] = True
            response['new_user'] = new_user

        return response

    def check_user(self, postData):
        user = self.filter(email=postData['email'])
        errors = []
        response = {}
        if user:
            # validate password
            # bcrypt.checkpw(postData['password'].encode(), bcrypt.gensalt())
            if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password.encode():
                print("It Matches!")
                response['status'] = True
                response['loggedin_user'] = user[0]
            else:
                print("It Does not Match :(")
                errors.append('Invalid email/password combination.')
                response['status'] = False
                response['errors'] = errors
        else:
            # email does not exits in DB
            errors.append('Email does not exist.')
            response['status'] = False
            response['errors'] = errors

        return response

class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
