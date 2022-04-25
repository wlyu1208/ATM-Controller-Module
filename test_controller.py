from random import randrange
from datetime import datetime
from copy import deepcopy

from controller.atm import AtmController
from model.atm import Account, Card

def create_basic_card():
    basic_saving = Account(randrange(1e15, 1e16), 1000)
    basic_checking = Account(randrange(1e15, 1e16), 3000)

    #PIN:8663
    basic_card = Card(datetime(2100, 12, 15), '8F61098BCCB435C779FD08685F85CB4BCC2704EFE7761A431FC8CD85EBFBC3E7', 123, 'Bank Of America', basic_saving, basic_checking)

    return basic_card

def create_expired_card():
    basic_card = create_basic_card()
    
    expired_card = deepcopy(basic_card)
    expired_card.expiration_date = datetime(1999, 12, 15)
    
    return expired_card


def test_insert_working_card():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    assert basic_atm_controller.insert(basic_card) == True

def test_inserted_card_data_in_atm():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    result = basic_atm_controller.insert(basic_card)
    assert basic_atm_controller.state.card == basic_card

def test_insert_expired_card():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    expired_card = create_expired_card()

    assert basic_atm_controller.insert(expired_card) == False

def test_expired_card_data_in_atm():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    expired_card = create_expired_card()

    result = basic_atm_controller.insert(expired_card)
    assert basic_atm_controller.state.card == None

def test_correct_pin():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    assert basic_atm_controller.enter_pin(8663) == True

def test_wrong_pin():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    assert basic_atm_controller.enter_pin(1234) == False

def test_choose_saving_and_check_balance():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(1)
    assert basic_atm_controller.account.balance == 1000

def test_choose_checking_and_check_balance():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(2)
    assert basic_atm_controller.account.balance == 3000

def test_deposit_from_saving():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(1)
    basic_atm_controller.deposit(100)
    account_balance = basic_atm_controller.account.balance
    cash_balance = basic_atm_controller.state.cash 
    assert (account_balance, cash_balance) == (1100, 100)

def test_deposit_from_checking():
    # Empty ATM
    basic_atm_controller = AtmController(0)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(2)
    basic_atm_controller.deposit(200)
    account_balance = basic_atm_controller.account.balance
    cash_balance = basic_atm_controller.state.cash
    assert (account_balance, cash_balance) == (3200, 200)

def test_withdraw_from_saving():
    #ATM with $100
    basic_atm_controller = AtmController(500)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(1)
    basic_atm_controller.withdraw(200)
    account_balance = basic_atm_controller.account.balance
    cash_balance = basic_atm_controller.state.cash 
    assert (account_balance, cash_balance) == (800, 300)
 
def test_withdraw_from_checking():
    #ATM with $100
    basic_atm_controller = AtmController(500)
    basic_card = create_basic_card()

    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(2)
    basic_atm_controller.withdraw(100)
    account_balance = basic_atm_controller.account.balance
    cash_balance = basic_atm_controller.state.cash 
    assert (account_balance, cash_balance) == (2900, 400)

def test_withdraw_over_cash():
    #ATM with $10
    basic_atm_controller = AtmController(10)
    basic_card = create_basic_card()
    basic_atm_controller.insert(basic_card)
    basic_atm_controller.choose_account(1)
    assert basic_atm_controller.withdraw(200) == False
