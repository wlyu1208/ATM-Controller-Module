from dataclasses import dataclass as dc
from datetime import date

@dc
class Account:
    number : str
    balance : int

@dc
class Card:
    expiration_date : date
    pin : str
    cvc : int
    bank : str
    saving: Account
    checking : Account

@dc
class AtmState:
    cash : int
    bank : str = 'Bank Of America'
    card : Card = None
    