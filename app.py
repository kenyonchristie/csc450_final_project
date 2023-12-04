import math
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
from datetime import date, datetime
from functions import User, Bank

global user

def call_database():
    connection = None
    try:
        connection = sqlite3.connect('kubera_bank.db')
        print("Connection to existing SQLite database successful")
        return connection
    except sqlite3.Error as e:
        print("Error connecting to SQLite database:", e)

def get_db_user(username):
    connection = call_database()
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        if user_data:         
            cursor.execute("SELECT balance FROM transactions_savings WHERE username=?", (username,))
            savings_data = cursor.fetchone()
            if savings_data:
                user = Bank(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8], user_data[9], savings_data[0])
                return user
            else:
                user = User(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8], user_data[9])
                return user
        else:
            return None

def register_user(username, password, fname, mname, lname, dob, ssn, phone, email):    
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    connection = call_database()
    with connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, fname, mname, lname, dob, ssn, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, password, fname, mname, lname, dob, ssn, phone, email))
        cursor.execute("INSERT INTO transactions_checking (username, date, type, vendor, amount, balance) VALUES (?, ?, ?, ?, ?, ?)", (username, current_date, 'OPEN', 'None', 0.00, 0.00))
        cursor.execute("INSERT INTO transactions_savings (username, date, type, amount, balance) VALUES (?, ?, ?, ?, ?)", (username, current_date, 'OPEN', 0.00, 0.00))
        connection.commit()
        print("User registered successfully")

def authenticate_user(username, password):
    connection = call_database()
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user_data = cursor.fetchone()
        print(user_data)
        if user_data:
            user = User(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8], user_data[9])  # Unpack the tuple into named variables
            session['user'] = user.username
            return user
        else:
            return None

def get_savings_balance(username):
    connection = call_database()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT balance FROM transactions_savings WHERE username=? ORDER BY date DESC LIMIT 1", (username,))
            result = cursor.fetchone()
            if result:
                balance = result[0]
                return f'{balance:.2f}'
            else:
                return None
    except sqlite3.Error as e:
        print("Error fetching account balances:", e)
        return None    
    
def get_checking_balance(username):
    connection = call_database()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT balance FROM transactions_checking WHERE username=? ORDER BY date DESC LIMIT 1", (username,))
            result = cursor.fetchone()            
            if result:
                balance = result[0]
                print(balance)
                return f'{balance:.2f}'
            else:
                return None
    except sqlite3.Error as e:
        print("Error fetching account balances:", e)
        return None
        
def get_checking_transactions(username):
    connection = call_database()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT date, type, vendor, amount, balance FROM transactions_checking WHERE username=? ORDER BY date DESC", (username,))
            result = cursor.fetchall()
            return result
    except sqlite3.Error as e:
        print("Error fetching account transactions:", e)
        return None
    
def get_savings_transactions(username):
    connection = call_database()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT date, type, amount, balance FROM transactions_savings WHERE username=? ORDER BY date DESC", (username,))
            result = cursor.fetchall()
            return result
    except sqlite3.Error as e:
        print("Error fetching account transactions:", e)
        return None

app = Flask(__name__)
app.secret_key = 'c4!c24K1976$'

@app.route('/')
def page_home():    
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def page_login():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user == None:
            message = f'Username and/or password do not match. Please try again.'
            return render_template('login.html', message = message)            
        else:
            #session['user'] = user.username
            #print(session['user'])
            print("Login Successful")
            # bank = Bank(user.username)
            # return render_template('accountsummary.html', user=user, bank=bank)
            savings_balance  = get_savings_balance(username)
            checking_balance = get_checking_balance(username)
            print(savings_balance)
            print(checking_balance)
            return render_template('accountsummary.html', savings_balance=savings_balance, checking_balance=checking_balance)
    else: 
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def page_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        dob = request.form['dob']
        ssn = request.form['ssn']
        phone = request.form['phone']
        email = request.form['email']
        if username and password and fname and mname and lname and dob and ssn and phone and email:
            register_user(username, password, fname, mname, lname, dob, ssn, phone, email)
            print('Account Created')
            return render_template('login.html')
        else:
            print('Invalid input')
            return render_template('register.html')
    else: 
        return render_template('register.html')
    
@app.route('/deposit', methods = ['GET', 'POST'])
def page_deposit():    
    username = session.get('user') 
    user = get_db_user(username) 
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y%m%d')
    current_time = current_datetime.strftime('%H%M%S')
    transaction_id = f'{username}_{current_date}_{current_time}'
    checking_balance = get_checking_balance(username)
    savings_balance = get_savings_balance(username)
    if request.method == 'POST':
        amount = request.form['deposit']
        deposit_type = request.form['type']
        if isinstance(user, Bank) and deposit_type == 'checking':            
            user.deposit_checking(transaction_id, current_datetime, amount, checking_balance)
        if isinstance(user, Bank) and deposit_type == 'savings':
            user.deposit_savings(transaction_id, current_datetime, amount, savings_balance)
    return render_template('deposit.html')

@app.route('/transfer', methods = ['GET', 'POST'])
def page_transfer():   
    username = session.get('user') 
    user = get_db_user(username)    
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y%m%d')
    current_time = current_datetime.strftime('%H%M%S')
    transaction_id = f'{username}_{current_date}_ {current_time}'    
    checking_balance = get_checking_balance(username)
    savings_balance = get_savings_balance(username)
    if request.method == 'POST':    
        amount = request.form['transfer']
        from_type = request.form['from_type']
        to_type = request.form['to_type']
        if isinstance(user, Bank):
            user.transfer(transaction_id, current_datetime, amount, from_type, to_type, checking_balance, savings_balance)
    return render_template('transfer.html')

@app.route('/billpay', methods = ['GET', 'POST'])
def page_billpay():
    username = session.get('user') 
    user = get_db_user(username) 
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y%m%d')
    current_time = current_datetime.strftime('%H%M%S')
    transaction_id = f'{username}_{current_date}_{current_time}'    
    balance = get_checking_balance(username)
    if request.method == 'POST':
        amount = request.form['pay']
        vendor = request.form['vendor']
        if isinstance(user, Bank):        
            user.bill_pay(transaction_id, current_datetime, vendor, amount, balance)
    return render_template('billpay.html')

@app.route('/transaction')
def page_transaction():
    return render_template('transaction.html')

@app.route('/accountsummary')
def page_summary():
    user = session['user']
    savings_balance  = get_savings_balance(user)
    checking_balance = get_checking_balance(user)
    print(savings_balance)
    print(checking_balance)
    return render_template('accountsummary.html', savings_balance=savings_balance, checking_balance=checking_balance)

@app.route('/checking')
def page_checking():
    user = session['user']
    checking_transactions = get_checking_transactions(user)
    print(checking_transactions)
    return render_template('checking.html', checking_transactions = checking_transactions)

@app.route('/savings')
def page_savings():
    user = session['user']
    savings_transactions = get_savings_transactions(user)
    print(savings_transactions)
    return render_template('savings.html', savings_transactions = savings_transactions)

@app.route('/logout', methods=['GET'])
def page_logout():
    return render_template('logout.html')

@app.route('/logout', methods=['POST'])
def confirm_logout():
    session.pop('user', None)
    return redirect(url_for('page_login'))

if __name__ == '__main__':
    app.run(debug=True)



