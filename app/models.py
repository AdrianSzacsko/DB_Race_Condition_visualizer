from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, ForeignKey, text, CheckConstraint, NUMERIC, Enum, DDL
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR, TEXT, Numeric

from .db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    amount = Column(Numeric(12, 2, asdecimal=False), default=0)

    # Define a one-to-many relationship with the logs table
    # logs = relationship('Log', back_populates='user')


# Define the Log model
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP, default=datetime.now())
    account_from = Column(Integer, ForeignKey('users.id'))
    amount_before = Column(Numeric(12, 2, asdecimal=False))
    amount = Column(Numeric(12, 2, asdecimal=False))

    # Define a many-to-one relationship with the users table
    # user = relationship('User', back_populates='logs')


class Log2(Base):
    __tablename__ = 'logs2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP, default=datetime.now())
    message = Column(VARCHAR(50))
    account = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric(12, 2, asdecimal=False))


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    amount = Column(Numeric(12, 2, asdecimal=False), default=0)

    # Define a one-to-many relationship with the logs table
    # logs = relationship('Log', back_populates='user')

