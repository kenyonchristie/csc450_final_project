from datetime import date, datetime
import sqlite3

class User():
    def __init__(self, username, password, fname, mname, lname, dob, ssn, phone, email):
        self.username = username
        self.password = password
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.dob = dob
        self.ssn = ssn
        self.phone = phone
        self.email = email
    
class Bank(User):
    def __init__(self, username, password, fname, mname, lname, dob, ssn, phone, email, balance = 0):
        super().__init__(username, password, fname, mname, lname, dob, ssn, phone, email)
        self.username = username
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.dob = dob
        self.ssn = ssn
        self.phone = phone
        self.email = email
        self.balance = balance

    def bill_pay(self, transaction_id, current_datetime, vendor, amount, balance):
        self.amount = float(amount)
        self.transaction_id = transaction_id
        self.current_datetime = current_datetime
        self.vendor = vendor
        transaction_type = 'WITHDRAWAL'
        self.balance = float(balance)
        new_balance = self.balance - self.amount

        with sqlite3.connect('kubera_bank.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO transactions_checking (id, username, date, type, vendor, amount, balance) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (self.transaction_id, self.username, self.current_datetime, transaction_type, self.vendor, self.amount, new_balance))       
            connection.commit() 
    
    def deposit_savings(self, transaction_id, current_datetime, amount, balance):
        self.amount = float(amount)   
        self.transaction_id = transaction_id
        self.current_datetime = current_datetime
        transaction_type = 'DEPOSIT'
        self.balance = float(balance)
        new_balance = self.balance + self.amount

        with sqlite3.connect('kubera_bank.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO transactions_savings (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                           (self.transaction_id, self.username, self.current_datetime, transaction_type, self.amount, new_balance)) 
            connection.commit()     

    def deposit_checking(self, transaction_id, current_datetime, amount, balance):
        self.amount = float(amount)
        self.transaction_id = transaction_id
        self.current_datetime = current_datetime
        transaction_type = 'DEPOSIT'
        self.balance = float(balance)
        new_balance = self.balance + self.amount

        with sqlite3.connect('kubera_bank.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO transactions_checking (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                           (self.transaction_id, self.username, self.current_datetime, transaction_type, self.amount, new_balance))       
            connection.commit() 
    
    def transfer(self, transaction_id, current_datetime, amount, from_type, to_type, checking_balance, savings_balance):
        self.amount = float(amount)
        self.transaction_id = transaction_id
        self.current_datetime = current_datetime
        self.from_type = from_type
        self.to_type = to_type
        self.checking_balance = float(checking_balance)
        self.savings_balance = float(savings_balance)
        transaction_type_withdraw = 'WITHDRAWAL'
        transaction_type_deposit = 'DEPOSIT'

        if self.from_type == 'checking':
            if self.amount > self.checking_balance:
                return f'Insufficient Funds in {self.from_type} account: ${self.checking_balance}'
            else:
                self.checking_balance -= self.amount
                self.savings_balance += self.amount
                with sqlite3.connect('kubera_bank.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO transactions_checking (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.transaction_id, self.username, self.current_datetime, transaction_type_withdraw, self.amount, self.checking_balance))
                    connection.commit() 
                    cursor.execute("INSERT INTO transactions_savings (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.transaction_id, self.username, self.current_datetime, transaction_type_deposit, self.amount, self.savings_balance))
                    connection.commit() 
        else:
            if self.amount > self.savings_balance:
                return f'Insufficient Funds in {from_type} account: ${self.savings_balance}'
            else:
                self.savings_balance -= self.amount
                self.checking_balance += self.amount
                with sqlite3.connect('kubera_bank.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO transactions_savings (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.transaction_id, self.username, self.current_datetime, transaction_type_withdraw, self.amount, self.savings_balance))
                    connection.commit() 
                    cursor.execute("INSERT INTO transactions_checking (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)",
                            (self.transaction_id, self.username, self.current_datetime, transaction_type_deposit, self.amount, self.checking_balance))
                    connection.commit()
            return f'Transfer successful. {self.from_type} balance: ${self.savings_balance}, {self.to_type} balance: ${self.checking_balance}'
