#!/usr/bin/env python

import os
import sys
import time

import tweepy
from tweepy import Cursor
from tweepy.binder import bind_api

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


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


# Check parameters
print(sys.argv)
if len(sys.argv) != 3:
    print("Bad tweet needs two values, the action and the url of the bad tweet.")
    print("Something like:")
    print(" $ python bad_tweet.py mute https://twitter.com/idiot/status/1234567890123456")
    sys.exit(1)

action = sys.argv[-2]
if action not in ('mute', 'block'):
    print("The first argument to bad tweet needs to be either 'mute' or 'block'")
    sys.exit(2)

bad_tweet_url = sys.argv[-1]
if (not bad_tweet_url.startswith('http') or
    'twitter.com' not in bad_tweet_url or
    'status' not in bad_tweet_url):
    print("The second argument doesn't seem to be a tweet url")
    sys.exit(3)


# API setup
# wait on rate limit means wait if we're rate limited, ie. don't error out
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = SkippableAPI(
          auth_handler=auth,
          wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)

          
# Find our account, build a whitelist of our followers so we don't mute them
"""
me = api.me()
whitelist = [me.id_str]
for followed in Cursor(api.friends).items():
    whitelist.append(followed.id_str)
print "You are following %d people" % len(whitelist)
print whitelist
"""

bad_tweet_id = bad_tweet_url.split('/')[-1]
print(bad_tweet_id)
#for retweet in api.retweets(id=bad_tweet_id, trim_user=1, count=100):
#    print retweet.author.id

for retweeter in api.retweeters(id=bad_tweet_id):
    print(retweeter)

