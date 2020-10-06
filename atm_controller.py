import sys

class ATM_Bank:
    def __init__(self):
        self.bank_info = {}

    def add_entry(self, card_num, pin, account, amt):
        self.bank_info[card_num] = {"pin":pin, "acc":{account:amt}}

    def add_account(self, card_num, account, amt):
        if card_num in self.bank_info:
            self.bank_info[card_num]["acc"][account] = amt

    def check_pin(self, card_num, entered_pin):
        if card_num in self.bank_info and self.bank_info[card_num]["pin"] == entered_pin:
            return self.bank_info[card_num]["acc"]
        else:
            return None

    def acc_update(self, card_num, account, amt):
        if self.bank_info[card_num]["acc"][account] in self.bank_info[card_num]["acc"]:
            self.bank_info[card_num]["acc"][account] = amt
            return True
        else:
            return False

class ATM_Controller:
    def __init__(self, bank, cash):
        self.ATM_Bank = bank
        self.accounts = None
        self.cash_bin = cash

    def card_swipe(self, card_num, pin):
        self.accounts = self.ATM_Bank.check_pin(card_num, pin)
        if self.accounts is None:
            return 0, "Invalid card/incorrect pin!"
        else:
            return 1, "Welcome!"

    def bank_account(self, acc):
        if acc in self.accounts:
            return True
        else:
            return False

    def account_actions(self, card_num, account, action, amt=0):
        if action == "Check Balance":
            return self.accounts[account], 1
        elif action == "Deposit":
            if self.accounts[account] >= amt and self.cash_bin >= amt:
                new_balance = self.accounts[account] - amt
                self.accounts[account] = new_balance
                self.ATM_Bank.acc_update(card_num, account, new_balance)
                return self.accounts[account], 1
            else:
                return self.accounts[account], 0
        elif action == "Withdraw":
            new_balance = self.accounts[account] + amt
            self.cash_bin += amt
            self.accounts[account] = new_balance
            self.ATM_Bank.acc_update(card_num, account, new_balance)
            return self.accounts[account], 1
        else:
            return self.accounts[account], 2

    # Test method
    def __call__(self, card_num, pin, account, action_list):
        cust_exit = False
        # Look for specific actions until Exit is specified
        while cust_exit is not True:
            # Swipe the card with and enter the pin
            ret, m = self.card_swipe(card_num, pin)
            if ret == 0:
                return "Invalid Card or Incorrect Pin!"
            ret = self.bank_account(account)
            if ret is False:
                return "Invalid account"
            for action in action_list:
                if action[0] == "Exit":
                    return "Bye bye! See you soon."
                balance, ret = self.account_actions(card_num, account, action[0], action[1])
                if ret == 0:
                    continue
                elif ret == 2:
                    return "Invalid action"
                else:
                    continue
            return "Test completed and successful"


if __name__ == "__main__":

    # Test Controller on Empty Bank
    empty_bank = ATM_Bank()
    empty_atm = ATM_Controller(empty_bank, 0)
    valid, message = empty_atm.card_swipe(0, 0)
    if valid == 0:
        print("TEST CASE 0: Empty ATM: PASS")
    else:
        print("TEST CASE 0: Empty ATM: FAIL")


    #################### Populate accounts, card numbers and pins #################### 

    my_bank = ATM_Bank() 
    # Add accounts 
    my_bank.add_account("0000-1111-2222-3333","savings",1000)
    my_bank.add_account("1111-2222-3333-0000","savings",2000)
    my_bank.add_account("2222-3333-0000-1111","savings",3000)
    my_bank.add_account("3333-0000-1111-2222","savings",4000)

    # Add pin for each card
    my_bank.add_entry("0000-1111-2222-3333","1111","checking",1000)
    my_bank.add_entry("1111-2222-3333-0000","2222","checking",2000)
    my_bank.add_entry("2222-3333-0000-1111","3333","checking",1000)
    my_bank.add_entry("3333-0000-1111-2222","4444","checking",4000)

    my_atm = ATM_Controller(my_bank, 50000)

    test1 = [("Check Balance",0), ("Withdraw", 40), ("Withdraw", 1000), ("Deposit", 100)]

    # Executes correctly
    if my_atm("3333-0000-1111-2222", "4444", "checking", test1) == "Test completed and successful":
        print("TEST CASE 1: Valid ATM: PASS")
    else:
        print("TEST CASE 1: Valid ATM: FAIL")

    # Handles overdraft attempt without crashing
    if my_atm("2222-3333-0000-1111", "3333", "checking", test1) == "Test completed and successful":
        print("TEST CASE 2: Overdraft handling: PASS")
    else:
        print("TEST CASE 2: Overdraft handling: FAIL")

    # Incorrect PIN number
    if my_atm("1111-2222-3333-0000", "2122", "checking", test1) == "Invalid Card or Incorrect Pin!":
        print("TEST CASE 3: Incorrect Pin Number: PASS")
    else:
        print("TEST CASE 3: Incorrect Pin Number: FAIL")

    # Incorrect Account number, PIN does not matter in this case
    if my_atm("1111-1111-1111-1111", "1111", "checking", test1) == "Invalid Card or Incorrect Pin!":
        print("TEST CASE 4: Incorrect Account Number: PASS")
    else:
        print("TEST CASE 4: Incorrect Account Number: FAIL")

    my_bank2 = ATM_Bank()
    my_bank2.add_entry("0000-1111-2222-3333", "1111", "checking", 1000)
    my_bank2.add_account("0000-1111-2222-3333", "savings", 1000)
    my_bank2.add_entry("1111-2222-3333-0000", "2222", "checking", 5000)
    my_atm2 = ATM_Controller(my_bank2, 10000)
    overflow_cash_bin = [("Check Balance", 0), ("Withdraw", 100000)]

    # Tests cash bin excess handling on account balance
    if my_atm("3333-0000-1111-2222", "4444", "checking", overflow_cash_bin) == "Test completed and successful":
        print("TEST CASE 5: Cash bin overflow: PASS")
    else:
        print("TEST CASE 5: Cash bin overflow: FAIL")

    exit_test = [("Check Balance", 0), ("Exit", 0)]
    if my_atm("3333-0000-1111-2222", "4444", "checking", exit_test) == "Bye bye! See you soon.":
        print("TEST CASE 6: Exit: PASS")
    else:
        print("TEST CASE 6: Exit: FAIL")
