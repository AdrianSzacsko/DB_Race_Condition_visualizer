import os
import threading
import time

from fastapi import FastAPI, Request, Form, APIRouter, Depends

from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.db.plain_db import db_connection
from app.library.helpers import to_array, CustomThread, Reporter

from app.library.graph import Graph
import json as JSON
from app.__init__ import path_exists

from loguru import logger

router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"],
)
templates = Jinja2Templates(directory="templates/")


templates.env.globals.update(path_exists=path_exists)

def transaction_handler(queries_1: list, queries_2: list):
    queries_number = len(queries_1) if len(queries_1) > len(queries_2) else len(queries_2)
    event1 = threading.Event()
    event2 = threading.Event()
    event1.set()
    thread1 = CustomThread(thread_handler, queries_1, event1, event2, "T1")
    thread2 = CustomThread(thread_handler, queries_2, event2, event1, "T2")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    dictionary1 = thread1.value
    dictionary2 = thread2.value
    return dictionary1, dictionary2


def thread_handler(queries: list, event_my: threading.Event, event_other: threading.Event, name: str):
    # if my turn, event_my is set, unset event_other. When finished, unset event_my and set event_other
    conn = db_connection()
    # conn.set_isolation_level(extensions.ISOLATION_LEVEL_READ_COMMITTED)
    reporter = Reporter()
    # reporter.transaction(extensions.ISOLATION_LEVEL_READ_COMMITTED)
    try:
        if conn is None:
            return "Unable to establish a database connection."
        with conn.cursor() as cur:
            for query in queries:
                event_my.wait(2)
                for subquery in query:
                    time.sleep(1)
                    start_time = time.perf_counter()
                    if reporter.query(subquery):
                        cur.execute(subquery)
                        reporter.select(subquery, str(to_array(cur.fetchall())))
                    else:
                        cur.execute(subquery)
                    if (time.perf_counter() - start_time) > 1: # the sql query took more than 1 second
                        reporter.late_execution(time.perf_counter())
                event_my.clear()
                event_other.set()
        # reporter.commit()
        conn.commit()
    except Exception as e:
        conn.cancel()
        reporter.error(str(e))
        reporter.query("abort;")
        event_my.clear()
        event_other.set()
    # logger.info(f"commit;" + "|")
    return reporter.return_values()


# @router.get("/create_db", response_class=HTMLResponse, name="transfers_page")
def test_create_db():
    conn = db_connection()
    if conn is None:
        return "Unable to establish a database connection."
    with conn.cursor() as cur:
        cur.execute("drop table if exists accounts;")
        cur.execute("""create table accounts(
                            id serial primary key ,
                            username varchar(50),
                            amount numeric(12,2) default 0
                            );""")
        cur.execute("insert into accounts(username, amount) values ('Adam', 500), ('Oliver', 500);")
        cur.execute("select * from accounts;")
        result = cur.fetchall()

    conn.commit()
    return JSONResponse({'accounts': to_array(result)})


@router.post("/run_test/", response_class=HTMLResponse, name="transfers_page")
def run_test(request: Request, id: int):
    test_create_db()
    # open json
    anomalies = JSON.loads(open("C:\\FIIT\\ZS_2023\\BIT\\Projekt\\app\\pages\\anomalies.json", "r").read())
    if not anomalies[id]:
        return JSONResponse()
    # isolation = "READ COMMITTED"
    queries_1 = anomalies[id]['query1']
    queries_2 = anomalies[id]['query2']
    result1, result2 = transaction_handler(queries_1, queries_2)
    json = {"query1": result1, "query2": result2}
    Graph(json, anomalies[id]['url'] + ".png")
    return RedirectResponse(url='/anomalies', status_code=302)
    #return JSONResponse(json)


@router.get("/", response_class=HTMLResponse, name="transfers_page")
def index(request: Request):
    anomalies = JSON.loads(open("C:\\FIIT\\ZS_2023\\BIT\\Projekt\\app\\pages\\anomalies.json", "r").read())
    return templates.TemplateResponse('anomalies.html', context={'request': request, 'data': anomalies})
