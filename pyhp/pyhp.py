import hashlib
import json

from bottle import route, run, template, static_file, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from peewee import Model, TextField, CharField, DateTimeField, ForeignKeyField, SqliteDatabase

db = SqliteDatabase('pyhp.db')
db.connect()

class SessionStore(Model):
    token = CharField()
    data = CharField()
    
try:
    db.create_table(SessionStore)
except:
    pass

def get_token():
    token = ''.join([random.choice('0123456789abcdef') for i in range(32)])

env = Environment(
    loader=FileSystemLoader('pages'),
    autoescape=select_autoescape(['html', 'xml'])
)

"""
@route('/')
@route('/hello')
@route('/hello/')
@route('/hello/<name>')
def hello(name="Stranger"):
    return template("Hello {{name}}, how are you?", name=name)
"""

@route('/static/<path:path>')
def static(path):
    return static_file(path, root="static")

@route('<path:path>')
def pyhp(path):
    # filter path name (no leading /, no ..),
    # make sure it's not /static/, /session/, /pyhp.py, etc.
    #   (maybe put all pages in /pages/ ?
    if path == '/':
        path = '/index.pyhp'
    print(f"TEST Attempting to load path: '{path}'")
    
    ## get template file
    template = env.get_template(path)
    
    ## load session (using cookie hash)
    
    ## databass?

    ## extract cookies, forms, etc. from request?

    ## save session data
    
    ## return page or error
    #return "ha ha butts: " + path + " " + str(dict(request.query))
    return template.render(request=request, session={})


run(host='localhost', port=8080, debug=True, reloader=True)
