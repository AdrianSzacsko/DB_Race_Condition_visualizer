# Database Race Condition visualizer
*Adrian Szacsko*

The project's main purpose is to visualize database race conditions using graphs, which are generated through database race condition simulations. The website also houses an exploit that can cause race condition real time in the database.

## Technologies

This project is built on top of the following (main) packages:
* Alembic migrations
* FastAPI backend
* Uvicorn web server
* SQLAlchemy ORM
* Jinja2
* HTML
* CSS
* Bootstrap
* JS
* PostgreSQL
## Requirements

The package requirements for this project are  located in the `requirements.txt` file. This `requirements.txt` file contains packages needed to run the project along with packages used for debugging purposes (like jupyter notebook).

## Installation & Usage

```bash
$ git clone git@github.com:TODO add link
$ cd fastapi-web-starter
# install packages
$ pip install -r requirements.txt
# .env file
#!!!Copy THE .env_examle FILE CONTENTS to .env WITH YOUR OWN DATABASE CREDENTIALS!!!
# run migrations
$ alembic upgrade head
# start the server[DEBUG mode]
$ uvicorn app.main:app --reload --port 8000
```

Visit http://127.0.0.1:8000/

![[Pasted image 20231120111156.png]]

## Features
### Home
From the theoretical viewpoint describes what race conditions are, what causes race conditions in general, what are some counter measures and mitigation techniques.
### Transfers
In this page the user can run a predefined exploit that causes race condition in a database. The database is a PostgreSQL database and the backend is using the most common packages and techniques used in backend development. Transactions are set as default (*READ COMMITTED*) and SQLAlchemy ORM models are used through all the endpoints which access the database. 

The exploit works by spawning a predefined number of threads which then calls the POST method (wants to transfer money from one account to the other). The exploit runs until a race condition happen.

*The exploit is located at `RaceConditionScript/main.py`*
### Anomalies
In this page the user run a predefined set of anomalies, which can cause race conditions. With the use of anomalies, the PostgreSQL database can be tested at different isolation levels on different anomalies. Every time an anomaly runs, the database initializes a new table and then the backend runs the two concurrent transactions using multithreading. This way, the anomalies can be reproduced anytime without the hassle of time management. 

The anomalies together with the SQL queries and descriptions are stored in a JSON file located in `app/pages/anomalies.json`. New anomalies can be added anytime to the JSON file and tested. The JSON's structure is as follows:

```json
[  
  {  
    "name": "Write cycles",  
    "isolation_level": "read committed",  
    "url": "write_cycles",  
    "prevents": true,  
    "description": "In this anomaly, two or more transactions concurrently attempt to write to the same data item without proper synchronization.",  
    "consequence": "The final state of the data may depend on the order in which the transactions commit, leading to inconsistent or incorrect data.",  
    "query1": [["begin; set transaction isolation level read committed;"],  
               ["update accounts set amount = 600 where username = 'Adam';"],  
               ["update accounts set amount = 400 where username = 'Oliver';",  
                "commit;",  
                "select * from accounts;"]],  
    "query2": [["begin; set transaction isolation level read committed;"],  
               ["update accounts set amount = 400 where username = 'Adam';"],  
               ["update accounts set amount = 600 where username = 'Oliver';",  
                "commit;",  
                "select * from accounts;"]]  
  }
]
```

The `query1` and `query2` list is defined as follows:

```json
"query1": [["begin; set transaction isolation level read committed;"],  
           ["update accounts set amount = 600 where username = 'Adam';"],  
           ["update accounts set amount = 300 where username = 'Adam';",  
            "commit;"]],
```
* The first list `"query1 : "[<content>]` houses all the SQL queries`
* The second list `"query1 : "[[<content>], [<content>], [<content>]]` houses a batch of queries that will be run one-by-one without the interruption of the second transaction
* The string elements in `"query1 : "[["<content>", "<content>"]]` should contain a valid SQL query.

*In case any of the SQL queries fail, the program returns the error and plots the graph with the error as well.*


The images for the graphs are stored in `app/static/images/`. In case any of the images are missing, the program will generate the images and store them in the same folder.

## Licence

【MIT License】

Copyright 2023 Adrian Szacsko

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*This project is built on top of the FastAPI Web Starter by* https://github.com/shinokada/fastapi-web-starter