


"""
Copyright (c) 2014, Outernet Inc
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of Outernet Inc.
"""

"""
From: https://github.com/Outernet-Project/bottle-utils-flash

.. module:: bottle_utils.flash
   :synopsis: Cookie-based flash messages

.. moduleauthor:: Outernet Inc <hello@outernet.is>
"""


import sys
import functools

from bottle import request, response


MESSAGE_KEY = str('_flash')
ROOT = b'/'
# This is not to keep cookie content secret, it's to allow UTF8 cookies
SECRET = 'flash'


def get_message(local_request):
    """
    Return currently set message and delete the cookie.

    :returns: message
    """
    response.delete_cookie(MESSAGE_KEY, path=ROOT, secret=SECRET)
    return request._message


def set_message(msg):
    """
    Sets a message and makes it available via ``request`` object. This function
    sets the message cookie and assigns the message to the
    ``bottle.request._message`` attribute.

    :param msg: message string
    """
    response.set_cookie(MESSAGE_KEY, msg, path=ROOT, secret=SECRET)
    request._message = msg


def message_plugin(func):
    """
    Manages flash messages. This is a Bottle plugin that adds attributes to
    ``bottle.request`` and ``bottle.response`` objects for setting and
    consuming the flash messages.

    See `How it works`_.

    Example::

        bottle.install(message_plugin)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cookie = request.get_cookie(MESSAGE_KEY, str(), secret=SECRET)
        request._message = cookie
        request.message = get_message
        response.flash = set_message
        return func(*args, **kwargs)
    return wrapper

