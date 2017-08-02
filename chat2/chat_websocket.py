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
Cribbing from:
https://github.com/storborg/aiochat/blob/master/aiochat/server.py
https://github.com/dpallot/simple-websocket-server/blob/master/SimpleWebSocketServer/SimpleWebSocketServer.py
https://github.com/dpallot/simple-websocket-server/blob/master/SimpleWebSocketServer/SimpleExampleServer.py

https://docs.python.org/3/library/asyncio.html
http://quietlyamused.org/blog/2015/10/02/async-python/
https://websockets.readthedocs.io/en/stable/api.html#websockets.protocol.WebSocketCommonProtocol
"""

import asyncio
import websockets
from http import cookies

from bottle import template

from models import Message, User, db
from models import get_user
import config
import url

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

message_template = """<p class="message">
    <span class="name">{{message.user.first_name}}</span>
    {{! message.content}}
    <span class="date">{{(message.date + config.timezone).strftime("%Y-%m-%d %H:%M%p")}}</span>
</p>"""

connected = set()


async def handler(websocket, path):
    """Handler for websockets.
           - Receive + auth incoming msgs
           - Post them out to everyone else."""
    global connected
    
    cookie = cookies.SimpleCookie()
    cookie.load(websocket.request_headers['Cookie'])
    user = get_user(request=None, token=cookie['token'].value)
    if not user:
        websocket.close()
        return
    websocket.user = user
    
    # When someone connects, we save it so that we can spam^Wmessage
    # them later on
    connected.add(websocket)
        
    # DEBUG
    print(("-" * 42))
    print(("REQUEST:", websocket.raw_request_headers))
    print(("RESPONSE:", websocket.raw_response_headers))
    #print("DIR:", dir(websocket))
    print(("TOKEN:", cookie['token'].value))
    print(("USER:", user.username))
    
    print(("-" * 42 + "\n"))
    while True:
        listener_task = asyncio.ensure_future(websocket.recv())
        
        # This needs to be a coroutine that finds/"produces" messages to 
        # send back to the web client, but it's not clear how this would work
        #producer_task = asyncio.ensure_future(producer())
        
        # Maybe we don't need a producer future/task?
        # try using the .send() function on every other connected websocket
        done, pending = await asyncio.wait(
            [listener_task],
            return_when=asyncio.FIRST_COMPLETED)
        
        # We haz a message - process it! :)
        message = listener_task.result()
        print(("MESSAGE:", message))
        
        message = url.make_urls(message)
        
        # insert message into db
        msg = Message(content=message, user=user)
        msg.save()
        
        await send_messages(msg, websocket)


async def send_messages(message, websocket):
    global connected
    
    message_html = template(message_template, message=message, config=config)

    for connection in connected:
        print(("STATE:", connection.state, connection.state_name, connection.user.username))
        if connection.state == 1:
            await connection.send(message_html)
        else:
            print(("Not sending, connection state is", 
                  connection.state, connection.state_name))

    # clean up closed connections...
    connected = set(ws for ws in connected if connection.state == 1)


start_server = websockets.serve(
                   handler,
                   config.websocket_ip,
                   config.websocket_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

