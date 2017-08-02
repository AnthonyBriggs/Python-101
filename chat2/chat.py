#!/usr/bin/env python

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
Simple webchat thingo. Well, maybe not so simple now that I've added users,
   registration, login, password change, blah blah blah

http://blog.pythonisito.com/2012/07/realtime-web-chat-with-socketio-and.html
http://docs.peewee-orm.com/en/latest/peewee/querying.html#sorting-records
http://bottlepy.org/docs/dev/async.html
http://bottlepy.org/docs/dev/index.html
http://bottlepy.org/docs/dev/stpl.html

Installing Python 3.5 from scratch:
https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=134828
(and http://www.extellisys.com/articles/python-on-debian-wheezy)
"""

import json
import os.path
import random

import bottle
from bottle import run, request, response, redirect, abort
from bottle import Bottle, template, SimpleTemplate, static_file
from peewee import SqliteDatabase


from flash import message_plugin
from models import db, Message, User
from models import get_user, check_login, set_user_password
import config

app = Bottle()
app.install(message_plugin)


def set_user_token(user):
    token = ''.join([random.choice('0123456789abcdef') for i in range(64)])
    response.set_cookie('token', token)
    user.token = token
    user.save()


@app.route('/')
def index():
    user = get_user(request)
    the_html = open('the.html').read()
    last_msgs = Message.select().order_by(-Message.id)[:10]
    return template(the_html, messages=reversed(last_msgs), 
                    user=user, request=request, config=config)

@app.route('/static/<filename>')
def server_static(filename):
    if filename.endswith('.wav'):
        response.headers['Content-type'] = "audio/wav;"
    return static_file(filename, root=config.static_path)


@app.route('/register')
def register():
    """Register a new account"""
    # This is done through user.txt for the moment...
    pass

@app.route('/confirm')
def confirm():
    """Confirm an account (via clicking a link in email)."""
    token = request.query.token
    user = get_user(request, token)
    if user:
        set_user_token(user)
        redirect('/set_password')
    return "<p>No user with that token</p>"


@app.get('/set_password')
def set_password():
    """Display password reset form"""
    user = get_user(request)
    the_html = open('password_change.html').read()
    return template(the_html, user=user, request=request)

@app.post('/set_password')
def post_set_password():
    user = get_user(request)
    if user:
        password = request.forms.get('password')
        password_check = request.forms.get('password_check')
        if password != password_check:
            the_html = open('password_change.html').read()
            response.flash("Those passwords don't match!")
            return template(the_html, user=user, request=request)
        set_user_password(user, password)
        response.flash("Your password has been changed")
        redirect('/')


# TODO: /forgot_password


@app.get('/edit_profile')
def edit_profile():
    """Display edit profile form"""
    user = get_user(request)
    the_html = open('edit_profile.html').read()
    return template(the_html, user=user, request=request)

@app.post('/edit_profile')
def post_edit_profile():
    user = get_user(request)
    if user:
        
        # Username shouldn't already exist
        username = request.forms.get('username')
        try:
            existing_user = User.get(username=username)
            if existing_user and existing_user != user:
                the_html = open('edit_profile.html').read()
                response.flash("That username is taken!")
                return template(the_html, user=user, request=request)
        except User.DoesNotExist:
            pass
        
        # Email should look vaguely legitimate
        # TODO: security thing - should we enforce confirmation
        # w/ the old email address?
        email = request.forms.get('email')
        if '@' not in email and '.' not in email.split('@')[1]:
            the_html = open('edit_profile.html').read()
            response.flash("That email is invalid!")
            return template(the_html, user=user, request=request)

        user.username = request.forms.get('username')
        user.first_name = request.forms.get('first_name')
        user.last_name = request.forms.get('last_name')
        user.email = request.forms.get('email')
        user.save()
        
        response.flash("Your profile has been updated")
    redirect('/')


@app.post('/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = check_login(username, password)
    if user:
        set_user_token(user)
        response.flash("Welcome, " + user.first_name)
    else:
        response.flash("No user found with that login")
    redirect('/')

@app.route('/logout')
def logout():
    response.delete_cookie('token')
    response.flash("You have been logged out!")
    redirect('/')


run(app, host="0.0.0.0", port=config.web_port)

