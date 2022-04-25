from dataclasses import dataclass as dc
from datetime import date

@dc
class Account:
    account_number : int
    balance : int

@dc
class Card:
    expeiration_date : date
    pin : str
    cvc : int
    bank : str
    saving: Account
    checking : Account

@dc
class ATM:
    bank : str = 'Bank Of America'
    card : Card = None
    
    