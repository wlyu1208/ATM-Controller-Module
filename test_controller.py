from random import randrange
from datetime import datetime
from copy import deepcopy

from controller.atm import AtmController
from model.atm import Account, Card

# basic card that works fine
def create_basic_card():
    basic_saving = Account(randrange(1e15, 1e16), 1000)
    basic_checking = Account(randrange(1e15, 1e16), 3000)

    # PIN:8663
    basic_card = Card(datetime(2100, 12, 15), '8F61098BCCB435C779FD08685F85CB4BCC2704EFE7761A431FC8CD85EBFBC3E7', 123, 'Bank Of America', basic_saving, basic_checking)

    return basic_card

# expired credit card
def create_expired_card():
    basic_card = create_basic_card()
    
    expired_card = deepcopy(basic_card)
    expired_card.expiration_date = datetime(1999, 12, 15)
    
    return expired_card

# test if inserted correctly
def test_insert_working_card():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    assert atm_machine.insert(basic_card) == True

# test atm correctly read inserted card
def test_inserted_card_data_in_atm():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    result = atm_machine.insert(basic_card)
    assert atm_machine.state.card == basic_card

# test atm does not take expired card
def test_insert_expired_card():
    # Empty ATM
    atm_machine = AtmController(0)
    expired_card = create_expired_card()

    assert atm_machine.insert(expired_card) == False

# test expred card is not read in atm
def test_expired_card_data_in_atm():
    # Empty ATM
    atm_machine = AtmController(0)
    expired_card = create_expired_card()

    result = atm_machine.insert(expired_card)
    assert atm_machine.state.card == None

# test if entered pin is same as pin that is encrypted in card information
def test_correct_pin():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    assert atm_machine.enter_pin(8663) == True

# test if wrong pin not working
def test_wrong_pin():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    assert atm_machine.enter_pin(1234) == False

# Check if saving is chosen correctly and balance is same
def test_choose_saving_and_check_balance():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(1)
    assert atm_machine.account.balance == 1000

# Check if checking is chosen correctly and balance is same
def test_choose_checking_and_check_balance():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(2)
    assert atm_machine.account.balance == 3000

# Check if deposit correctly work on saving in card and cash in atm
def test_deposit_from_saving():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(1)
    atm_machine.deposit(100)
    account_balance = atm_machine.account.balance
    cash_balance = atm_machine.state.cash 
    assert (account_balance, cash_balance) == (1100, 100)

# Check if deposit correctly work on checking in card and cash in atm
def test_deposit_from_checking():
    # Empty ATM
    atm_machine = AtmController(0)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(2)
    atm_machine.deposit(200)
    account_balance = atm_machine.account.balance
    cash_balance = atm_machine.state.cash
    assert (account_balance, cash_balance) == (3200, 200)

# Check if withdraw works correctly in saving account and card
def test_withdraw_from_saving():
    #ATM with $100
    atm_machine = AtmController(500)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(1)
    atm_machine.withdraw(200)
    account_balance = atm_machine.account.balance
    cash_balance = atm_machine.state.cash 
    assert (account_balance, cash_balance) == (800, 300)
 
# Check if withdraw work correctly in checking
def test_withdraw_from_checking():
    #ATM with $100
    atm_machine = AtmController(500)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(2)
    atm_machine.withdraw(100)
    account_balance = atm_machine.account.balance
    cash_balance = atm_machine.state.cash 
    assert (account_balance, cash_balance) == (2900, 400)

# test if withdraw not work if ATM has no cash
def test_withdraw_over_cash():
    #ATM with $10
    atm_machine = AtmController(10)
    basic_card = create_basic_card()

    atm_machine.insert(basic_card)
    atm_machine.choose_account(1)
    assert atm_machine.withdraw(200) == False

# test complex scenario 
# used case: 1. saving +200 -> -50 | 2. 
def test_atm():
    #ATM with $2000
    atm_machine = AtmController(2000)
    # Saving: $1000 Checking: $3000
    basic_card = create_basic_card()

    # expect True
    check_insert = atm_machine.insert(basic_card)

    # choose saving
    atm_machine.choose_account(1)
    atm_machine.deposit(200)
    atm_machine.withdraw(50)
    # 1000 + 200 - 50 = 1150
    saving_balance = atm_machine.account.balance
    # 2000 + 200 - 50 = 2150
    cash_atm_first = atm_machine.state.cash

    # Change Account to Checking
    atm_machine.reinitialize()
    atm_machine.choose_account(2)

    atm_machine.withdraw(1000)
    atm_machine.deposit(100)
    # 3000 - 1000 + 100 = 2100
    checking_balance = atm_machine.account.balance
    # 2150 - 1000 + 100 = 1250
    cash_atm_second = atm_machine.state.cash

    atm_machine.reinitialize()
    new_card_info = atm_machine.reset_machine()
    assert (check_insert, saving_balance, checking_balance, cash_atm_first, cash_atm_second) == (True, 1150, 2100, 2150, 1250)
    
    
