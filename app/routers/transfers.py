import time

from fastapi import FastAPI, Request, Form, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from RaceConditionScript.main import RaceCondition
import os
from sqlalchemy import func
from sqlalchemy.orm import Session
#from starlette.responses import RedirectResponse
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from app.db.database import create_connection
from app.library.helpers import CustomLogger
from app.models import User, Log, Log2
from typing import Optional

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
)
templates = Jinja2Templates(directory="templates/")

logger = CustomLogger("logging.log")


@router.get("/", response_class=HTMLResponse, name="transfers_page")
def transfers_page(request: Request,
             db: Session = Depends(create_connection),
             error_msg: Optional[str] = None):
    users = db.query(User).order_by(User.id).all()
    logs = db.query(Log.date, User.username, Log.amount_before, Log.amount.label('log_amount'), User.amount.label('user_amount')).join(User).order_by(Log.date.desc()).limit(100).all()
    data = {
        'users': [row.__dict__ for row in users],
        'bank_amount': sum(row.__dict__['amount'] for row in users),
        'logs': [{'date': row.date,
                  'username': row.username,
                  'amount_before': row.amount_before,
                  'log_amount': row.log_amount,
                  'user_amount': row.user_amount} for row in logs],
    }
    return templates.TemplateResponse('transfers.html', context={'request': request, 'data': data, 'error': error_msg})


@router.post("/form/", response_class=HTMLResponse)
def form_post(request: Request,
              sender_id: int,
              receiver_id: int,
              number: int = Form(...),
              db: Session = Depends(create_connection)):
    sender_obj = db.query(User.id.label('id'), User.username.label('username'), User.amount.label('amount'), func.current_timestamp().label("time")).filter(User.id == sender_id)
    sender = sender_obj.first()

    # check sender
    if not sender:
        error = 'User not found'
        redirect_url = f"/transfers?error_msg={error}"
        return RedirectResponse(redirect_url, status_code=302)
    if sender.amount < number:
        error = 'Can not transfer this amount, not enough funds'
        # return request.url_for("transfers_page", error_msg=error)
        redirect_url = f"/transfers?error_msg={error}"
        return RedirectResponse(redirect_url, status_code=302)
        # return templates.TemplateResponse('transfers.html', context={'request': request, 'error': error})

    receiver_obj = db.query(User.id.label('id'), User.username.label('username'), User.amount.label('amount'), func.current_timestamp().label("time")).filter(User.id == receiver_id)
    receiver = receiver_obj.first()

    # check receiver
    if not receiver:
        error = 'User not found'
        redirect_url = f"/transfers?error_msg={error}"
        return RedirectResponse(redirect_url, status_code=302)

    db.query(User).filter(User.id == sender_id).update({User.amount: sender.amount - number})
    db.query(User).filter(User.id == receiver_id).update({User.amount: receiver.amount + number})

    db.commit()
    #logger.write()
    return RedirectResponse(url='/transfers', status_code=302)


@router.get("/check_amount/")
def get_amount(request: Request,
           db: Session = Depends(create_connection)):
    users = db.query(User).all()
    amount = 0
    for row in users:
        amount += row.amount

    return JSONResponse({'amount': amount})


@router.post("/run_script/")
def run_script(request: Request,
               threads: int = Form(...)):
    if threads <= 0:
        return RedirectResponse(url='/transfers', status_code=302)
    x = RaceCondition(threads, str(request.base_url), "transfers/form/")
    x.run()
    return RedirectResponse(url='/transfers', status_code=302)


@router.post("/delete/")
def delete(request: Request,
           db: Session = Depends(create_connection)):

    db.query(Log).delete()
    db.query(Log2).delete()
    db.commit()
    file = open("logging.log", "w")
    file.close()
    return RedirectResponse(url='/transfers', status_code=302)
