from typing import Optional

from pydantic import BaseModel


class GetAccount(BaseModel):
    id: int
    username: str
    amount: float


"""class GetAccounts(BaseModel):
    list: Optional[list] = [GetAccount]"""
