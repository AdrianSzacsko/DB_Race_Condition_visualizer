import os
import requests

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

def path_exists(url):
    return requests.get(url).status_code == 200
    #return os.path.exists(url)

def clever_function():
    return u'HELLO'

templates.env.globals.update(clever_function=clever_function)

templates.env.globals.update(path_exists=path_exists)