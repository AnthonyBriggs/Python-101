https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04


BLOOOOCKED
----------

Dodgy Python scripts to download a big list of someone's followers
and block them en masse. Alpha version, not really any UI to speak of,
Python and UNIX knowledge is probably a good idea.

I highly recommend also using the GG autoblocker and Block Together,
especially the 'block new accounts' option of Block Together (it stops
harassers making new accounts immediately).

How to use:

1.  [(VERY) OPTIONAL, if you've blocked lots of people this might take a while]
    Go to Twitter settings and download "csv" files of all the people
    you're currently blocking. Stick them into the blocked_export folder,
    as a temporary holding place, and cat them all into a file called
    "blocked_idiots.csv" in the same place as the script.
    
    This is a bit faster, since it saves the program from trying to block
    people you've already blocked. This is optional though, since the 
    blockem.py script will update the list itself.

2.  Make a Twitter app (via https://apps.twitter.com/), generate a
    read/write key-token thing (there'll be four(!) tokens). Stick the
    tokens in config.py (copy this from config_sample.py)

3.  Install Python, set up a virtualenv, install all the requirements:
        pip install -r requirements.txt

4a. The script uses ids for most things, which is faster in Twitter's API.
    If you want to check who's behind an id, you can go to:
        https://twitter.com/intent/user?user_id=<the_id>
    which will show you who they are and give you a link to their
    username/handle.

4.  Run the script!

        python blockem.py

    If everything's working, the script will pause for a few seconds
    while it reads the big list of idiots, then start blocking:
    
		Blocking id 2572929678... done
		Blocking id 2820726802... done
		Blocking id 1863644514... done
		Blocking id 1107481592... done
		Blocking id 1633560752... done
		Blocking id 2851884963... done

    It'll take a while to chew through the list, but doesn't seem to
    use much bandwidth, so just let it chug along in the background.
    It saves its progress to blocked_idiots.csv as it goes, so should
    be safe to stop and restart if you need to. "idiots.csv" is a big
    list of all of @Nero's followers as of 2015-09-10, so by default
    this will block everyone who was following @Nero at that time.

5.  There's a followers.py script which I used to generate all of the ids

       python followers.py > idiots.csv

    You probably want to either move the existing idiots file before you 
    do that, or else build one for each idiot, eg.

       python followers.py nero > idiots_nero.csv
       python followers.py jason > idiots_jason.csv
       python followers.py lousiemensch > idiots_louisemensch.csv
    
    then cat them into idiots.csv:

       cat idiots_*.csv | sort -u > idiots.csv

    You might also want to share your .csv files with people that you
    trust/who trust you, so they don't have to download the whole thing
    over again.


I'm very open to suggestions on how to improve this script. You can message me
on Twitter: @AnthonyBriggs

TODO: package this up into a self-contained program so that anyone can
      use it?
TODO: more user-friendly, fire and forget

