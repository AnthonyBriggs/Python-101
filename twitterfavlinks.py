# twitterfavlinks.py - Throw back all your favorites that contain a url. Get any applicable redirects. Note there are Twitter API
# limits, so if you have a gazillion favorites, you probably won't get them all. YMMV
# 
# Author: @curi0usJack
#
# Dependencies:
#   Tweepy: sudo pip install tweepy
#   Twitter API access. Set up here: https://apps.twitter.com/

# from https://gist.github.com/curi0usJack/4c1a732385250c78febfcdd73b0aa1f8

import tweepy
import urllib.request, urllib.error, urllib.parse
import re

# Enter the handle to search for (minus the @ sign). You can search for any user.
handle="HANDLETOSEARCHFOR"

# Enter twitter application keys
consumer_key = "CONSUMERKEY"
consumer_secret = "CONSUMERSECRET"
access_token = "ACCESSTOKEN"
access_secret = "ACCESSSECRET"

# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

favs = api.favorites(screen_name=handle, count=200)

# Get favorites
while len(favs) > 0:
    lastfavid = 0
    for fav in favs:
        toprint = False
        lastfavid = fav.id
        if handle not in fav.text:
            urls = re.findall("https:\/\/t\.co\/[a-zA-Z0-9]+", fav.text)
            strtxt = fav.text
            links = ""
            for url in urls:
                try:
                    landingurl = urllib.request.urlopen(url).geturl()
                except:
                    landingurl = "(ERROR GETTING URL: {0})".format(url)

                strtxt = strtxt.replace(url, landingurl)
                toprint = True

            if toprint:
                print(strtxt.encode('utf-8').replace('\n', ' '))
                lastfavid = fav.id

    favs = api.favorites(screen_name=handle, count=200, max_id=lastfavid)
