import sqlite3
from datetime import datetime

bank_db = sqlite3.connect('kubera_bank.db')
bank_cursor = bank_db.cursor()

# Create the users table
bank_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT,
                        password TEXT,
                        fname TEXT, 
                        mname TEXT,
                        lname TEXT, 
                        dob DATE, 
                        ssn TEXT, 
                        phone TEXT, 
                        email TEXT)''')

data = ('jSmith76', 'smithsonian11', 'John', 'Bartholomew', 'Smith', '1956/01/10', '111-12-2222', '860-999-9999', 'test@gmail.com')
bank_cursor.execute("INSERT INTO users (username, password, fname, mname, lname, dob, ssn, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

user_id = bank_cursor.lastrowid
bank_cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
username = bank_cursor.fetchone()[0]  
print(username)

bank_cursor.execute('''CREATE TABLE IF NOT EXISTS transactions_checking (
                        id TEXT PRIMARY KEY, 
                        username TEXT,
                        date DATETIME,
                        type TEXT,
                        vendor TEXT,
                        amount FLOAT, 
                        balance FLOAT,                    
                        FOREIGN KEY (username) REFERENCES users(username))''')

current_datetime = datetime.now()
current_date = current_datetime.strftime('%Y%m%d')
current_time = current_datetime.strftime('%H%M%S')
transaction_id = f'{username}_{current_date}_{current_time}'

checking_data = (transaction_id, username, current_datetime, 'DEPOSIT', 'SELF', 100.00, 100.00)
bank_cursor.execute("INSERT INTO transactions_checking (id, username, date, type, vendor, amount, balance) VALUES (?, ?, ?, ?, ?, ?, ?)", checking_data)

bank_cursor.execute('''CREATE TABLE IF NOT EXISTS transactions_savings (
                        id TEXT PRIMARY KEY, 
                        username TEXT,
                        date DATETIME,
                        type TEXT,
                        amount FLOAT, 
                        balance FLOAT,
                        FOREIGN KEY (username) REFERENCES users(username))''')

savings_data = (transaction_id, username, current_datetime, 'DEPOSIT', 50.00, 50.00)
bank_cursor.execute("INSERT INTO transactions_savings (id, username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?, ?)", savings_data)

bank_db.commit()
bank_cursor.close()
bank_db.close()

