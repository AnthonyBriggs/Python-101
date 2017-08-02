
"""
Copyright (C) 2016 Anthony Briggs <anthony.briggs@gmail.com>

This file is part of Chat-thing.

    Chat-thing is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as 
    published by the Free Software Foundation, either version 3 of 
    the License, or (at your option) any later version.

    Chat-thing is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public 
    License along with Chat-thing.  If not, see 
    <http://www.gnu.org/licenses/agpl.txt>.
"""

"""
Database models for the chat server
"""

import datetime, time
import hashlib

from peewee import Model, TextField, CharField, DateTimeField, ForeignKeyField, SqliteDatabase

import config

db = SqliteDatabase('messages.db')

class User(Model):
    username = CharField()
    password = CharField()  # hashed
    token = CharField()
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    
    class Meta(object):
        database = db
    
class Message(Model):
    # TODO: date + user
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, related_name='messages')
    
    class Meta(object):
        database = db

for model in (User, Message):
    try:
        db.create_table(model)
    except:
        pass

def get_user(request, token=None):
    if not token:
        token = request.cookies.get('token', 'NO_TOKEN')
    try:
        user = User.get(User.token == token)
        return user
    except User.DoesNotExist:
        return None

def check_login(username, password):
    pwd_hash = hashlib.sha224((config.password_salt + password).encode('utf-8')).hexdigest()
    try:
        user = User.get(
                  User.username == username,
                  User.password == pwd_hash)
        return user
    except User.DoesNotExist:
        return None

def set_user_password(user, password):
    pwd_hash = hashlib.sha224((config.password_salt + password).encode('utf-8')).hexdigest()
    user.password = pwd_hash
    user.save()


