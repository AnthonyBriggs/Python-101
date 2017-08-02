#!/usr/bin/env python3

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
Add a user to the system.
"""

import random
import sys

from peewee import SqliteDatabase

from models import db, Message, User
from models import get_user, check_login, set_user_password
import config


print("Chat-thing.")
print("Users in the system:")
for user in User.select():
    # fixin' an error:
    if user.email.endswith("\n"):
        user.email = user.email.strip()
        user.save()
        
    print((("    {user.username}\t" 
           "{user.first_name} {user.last_name}\t"
           "{user.email}").format(user=user)))

while True:
    username = input("Enter a username for the new user > ").strip()
    if User.select().where(User.username == username).count() > 0:
        print("That username already exists!")
    else:
        break

print(("Enter details for '{0}':".format(username)))

first_name = input("First name: ").strip()
last_name = input("Last name: ").strip()

while True:
    email = input("Email: ").strip()
    if '@' not in email and '.' not in email.split('@')[1]:
        print("Invalid email address!")
    else:
        break

token = ''.join([random.choice('0123456789abcdef') for i in range(32)])
rand_pwd = ''.join([random.choice('0123456789abcdef') for i in range(16)])

new_user = User(username=username, email=email,
                first_name=first_name, last_name=last_name,
                password=rand_pwd, token=token)
new_user.save()

# send confirmation email
import smtplib
from email.mime.text import MIMEText
msg = MIMEText(
"""Hi {user.first_name},

You have been added to {config.operator_name}'s chat system.

To accept the invitation, follow this link, where you can set a password:

    http://{config.server}/confirm?token={token}

Your username is: {user.username}

Cheers,

{config.operator_name}""".format(
    config=config, token=token, user=new_user))

print(("Sending invitation to {0}:".format(user.email)))
print(msg)

msg['Subject'] = "Invitation to %s's chat system" % config.operator_name
msg['From'] = config.operator
msg['To'] = "%s %s <%s>" % (user.first_name, user.last_name, user.email)

sender = smtplib.SMTP(config.mail_server)
sender.login(config.mail_user, config.mail_password)
sender.sendmail(msg['From'], [msg['To']], msg.as_string())
sender.quit()

print("Sent!")
