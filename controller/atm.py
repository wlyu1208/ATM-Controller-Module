import hashlib
from datetime import date

from model.atm import AtmState

class AtmController():
    SAVING = 1
    CHECKING = 2
    BANK = "Bank Of America"

    def __init__(self, cash):
        self.state = AtmState(cash)
        self.account = None
        self.chosen_acc = None
    
    def insert(self, card):
        if card.expiration_date.strftime("%Y/%m/%d") < date.today().strftime("%Y/%m/%d"):
            return False
        else:
            self.state.card = card
            return True
    
    def enter_pin(self, pin):
        hashed_pin = hashlib.sha256(str(pin).encode()).hexdigest().upper()
        
        if hashed_pin == self.state.card.pin:
            return True
        else:
            return False
    
    def choose_account(self, num):
        self.chosen_acc = num

        if num == self.SAVING:
            self.account = self.state.card.saving
        
        if num == self.CHECKING:
            self.account = self.state.card.checking
    
    def balance(self):
        return self.account.balance

    def deposit(self, num):
        self.account.balance += num
        self.state.cash += num
    
    def withdraw(self, num):
        if self.state.cash < num:
            return False
        else:
            print(self.account.balance)
            self.account.balance -= num
            self.state.cash -= num
            return True
    
    def end(self):
        if self.chosen_acc == self.SAVING:
            self.card.saving = self.account
        elif self.chosen_acc == self.CHECKING:
            self.card.checking = self.account
        
        self.__init__(self.cash)

        return self.card
    