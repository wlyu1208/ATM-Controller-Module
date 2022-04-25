import hashlib
from datetime import date

from model.atm import AtmState

class AtmController():
    SAVING = 1
    CHECKING = 2

    def __init__(self, cash):
        self.state = AtmState(cash)
        self.account = None
        self.chosen_acc = None
    
    # insert method
    def insert(self, card):
        if card.expiration_date.strftime("%Y/%m/%d") < date.today().strftime("%Y/%m/%d"):
            return False
        else:
            self.state.card = card
            return True
    
    # check if encryted pin in card is same as enetered pin
    def enter_pin(self, pin):
        hashed_pin = hashlib.sha256(str(pin).encode()).hexdigest().upper()
        
        if hashed_pin == self.state.card.pin:
            return True
        else:
            return False
    
    # choose account in card
    def choose_account(self, num):
        self.chosen_acc = num

        if num == self.SAVING:
            self.account = self.state.card.saving
        
        if num == self.CHECKING:
            self.account = self.state.card.checking
    
    # return balance of account
    def balance(self):
        return self.account.balance

    # depoist number that customer put in atm and card
    def deposit(self, num):
        self.account.balance += num
        self.state.cash += num
    
    # withdraw cash to customer if enough cash in atm
    def withdraw(self, num):
        if self.state.cash < num:
            return False
        else:
            print(self.account.balance)
            self.account.balance -= num
            self.state.cash -= num
            return True
    
    # reinitialize machine if transaction is changed
    def reinitialize(self):
        if self.chosen_acc == self.SAVING:
            self.state.card.saving = self.account
        elif self.chosen_acc == self.CHECKING:
            self.state.card.checking = self.account
    
    # reset machine with its latest cash and return card if ended
    def reset_machine(self):
        self.__init__(self.state.cash)
        
        return self.state.card
    