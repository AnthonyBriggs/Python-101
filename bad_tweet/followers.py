#!/usr/bin/env python

import os
import sys
import time

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import tweepy
from tweepy import Cursor

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# API setup
# wait on rate limit means wait if we're rate limited, ie. don't error out
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(
          auth_handler=auth,
          wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)
me = api.me()

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "nero"

# list all of the idiots' ids.
# You can check which idiot is which id via:
#    https://twitter.com/intent/user?user_id=<idiot's id>,
# eg. https://twitter.com/intent/user?user_id=2916601
for idiot in list(Cursor(api.followers_ids, screen_name=username).items()):
    print(idiot)

