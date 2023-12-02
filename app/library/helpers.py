import os.path
import re
import threading
import time
from datetime import datetime
from enum import Enum
from threading import Thread
from typing import TextIO
from app.schemas.accounts import GetAccount

import markdown


def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data


class CustomLogger:
    buffer: [str]
    # file: TextIO
    file_path: str

    def __init__(self, file_path: str):
        self.buffer = []
        # self.file = open(file_path, "a")
        self.file_path = file_path

    def write(self):
        file = open(self.file_path, "a")
        file.writelines(self.buffer)
        self.buffer = []
        file.close()

    def info(self, message: str, time: datetime):
        level = "INFO"
        log_format = f"{time}|{level}|{message}\n"
        self.buffer.append(log_format)


def to_array(result):
    instance = [GetAccount(id=id, username=username, amount=amount) for id, username, amount in result]
    return [row.__dict__ for row in instance]


class CustomThread(Thread):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.value = None

    def run(self):
        self.value = self.func(*self.args, **self.kwargs)


class Reporter:
    #reports = []

    def __init__(self):
        self.reports = []

    def transaction(self, isolation_level):
        #date = datetime.now()
        date = time.perf_counter()
        query = f"begin; set transaction isolation level {isolation_level};"
        self.reports.append(str(date) + "|" + query + "|")
        return

    def query(self, query):
        # date = datetime.now()
        date = time.perf_counter()
        # return 1 if select to run fetchall, return 0 if anything else
        sql_select_pattern = r'(?i)^\s*SELECT\s+.+\s+FROM\s+.+;$'
        if re.match(sql_select_pattern, query):
            return True
        self.reports.append(str(date) + "|" + query + "|")
        return False

    def select(self, query, fetchall):
        # date = datetime.now()
        date = time.perf_counter()
        self.reports.append(str(date) + "|" + query + "|" + fetchall)

    def return_values(self):
        return self.reports

    def commit(self):
        # date = datetime.now()
        date = time.perf_counter()
        self.reports.append(str(date) + "|" + f"commit;" + "|")

    def error(self, error: str):
        date = time.perf_counter()
        self.reports.append(str(date) + "|" + f"{error};" + "|")

    def late_execution(self, date):
        self.reports.append(str(date) + "|" + f"Previous query Execution" + "|")

