import urllib

import jinja2
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import environment, Environment, FileSystemLoader

from app.library.helpers import *
from app.routers import transfers, race_conditions

from loguru import logger


import os

logger.add("logging.log", format="{time}|{level}|{message}")

app = FastAPI()

template = Environment(loader=FileSystemLoader("templates"))

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(transfers.router)
app.include_router(race_conditions.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name + ".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})



