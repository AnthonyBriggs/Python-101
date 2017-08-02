#!/usr/bin/env python

import os
import sys
import time

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import tweepy
from tweepy import Cursor
from tweepy.binder import bind_api

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

if len(sys.argv) > 1:
    BLOCKFILE = sys.argv[1]
else:
    BLOCKFILE = "idiots.csv"


class SkippableAPI(tweepy.API):
    """Override the create_block function so that it accepts
    the 'skip_status' option (ie. don't return the user from the command,
    so that it returns faster."""
    @property

    def create_block(self):
        """ :reference: https://dev.twitter.com/rest/reference/post/blocks/create
            :allowed_param:'id', 'user_id', 'screen_name', 'skip_status'
        """
        return bind_api(
            api=self,
            path='/blocks/create.json',
            method='POST',
            payload_type='user',
            allowed_param=['id', 'user_id', 'screen_name', 'skip_status'],
            require_auth=True)

    @property
    def blocks_ids(self):
        """ :reference: https://dev.twitter.com/rest/reference/get/blocks/ids
            :allowed_param:'cursor'"""
        return bind_api(
            api=self,
            path='/blocks/ids.json',
            payload_type='json',
            allowed_param=['cursor'],
            require_auth=True)


# API setup
# wait on rate limit means wait if we're rate limited, ie. don't error out
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = SkippableAPI(
          auth_handler=auth,
          wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)
me = api.me()
whitelist = [me.id_str]
for followed in list(Cursor(api.friends).items()):
    whitelist.append(followed.id_str)
print("You are following %d people" % len(whitelist))
print(whitelist)

# download our list of current blocks. Unfortunately, blocks_id doesn't
# seem to paginate, even though it should...
# UPDATE: Better to paste all of your exported block csv files together,
# so I removed this download bit. I might reinstate once I work out a fast
# way to d/l them all.

blocked_idiots = [each_id.strip() for each_id in file('blocked_idiots.csv').readlines()]
print("Already blocked %d idiots" % len(blocked_idiots))
print(blocked_idiots[:20])
sys.exit()

blocked_idiots = set(blocked_idiots)

idiots = [each_id.strip() for each_id in file(BLOCKFILE).readlines()
              if each_id.strip() not in blocked_idiots]
print("Loaded %d idiots" % len(idiots))

# We save our progress to a file, just in case we get interrupted,
# then we don't hit the API as hard/things go faster.
progress = file('blocked_idiots.csv', 'a+')

count = 0
for idiot in idiots:
    # Don't look up the name, it slows us (also API limit maybe)
    #name = api.get_user(user_id=int(idiot)).screen_name
    #print "Blocking id %s (%s)..." % (idiot, name),
    if idiot not in blocked_idiots:
        print("Blocking id %s..." % idiot, end=' ') 
        try:
            if idiot.isdigit(): 
                api.create_block(user_id=int(idiot), skip_status=True)
                # add them to the local list
                blocked_idiots.add(idiot)
                progress.write(idiot + "\n")
                progress.flush()
                count += 1
            else:
                # API limit; have another go around :)
                continue 
        except tweepy.error.TweepError:
            # Usually this is because the idiot has been
            # banned by Twitter before we can get to them
            continue
        print("done")
    if count % 100 == 0:
        print("%d / %d idiots blocked" % (count, len(idiots)))
print("All finished!")
progress.close()

