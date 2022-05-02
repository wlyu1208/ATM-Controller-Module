# ATM-Controller-Module
Repository for simple ATM contoller module with card insertion, account selection and basic ATM functions 

# Objective
 - Simple ATM machine controller that only has frame parts of a machine.
 - This controller can integrate to real machine if specific and secured features are added to frames.
 - controller and model are already initialized as module, so anyone can call them as module. 

# Features
 1. Insert Card and check if card is valid or not
 2. Check if eneted pin is correct or not
 3. Choose Account that user wants to use
 4. Balance, Deposit, Withdraw that shows, adds, subtracts from the balance of chosen account
 
# Development Environment
 - Language : Python 3.9
 - OS: Windows Subsystem for Linux
 - SW:
    - Anaconda
    - Lanaguage Package:
        - dataclasses
        - pytest

# How to Test
 - If you use Anaconda, create environment with python = 3.9
 1. Clone repository with https `https://github.com/wlyu1208/ATM-Controller-Module.git`
    ```console
    $ git clone https://github.com/wlyu1208/ATM-Controller-Module.git
    ```
 
 2. Install libraries that are used in this project
    ```console
    $ pip install -r requirements.txt
    ```

 3. Run pytest where test_controller.py is placed
    ```console
    $ pytest
    ``` 

 4. There are 14 test cases in test_controll.py, and all tests need to be passed. 
