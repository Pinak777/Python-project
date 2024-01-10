from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
connection = sqlite3.connect('Market.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS User(UserID NUMBER PRIMARY KEY, Username VARCHAR(50) UNIQUE NOT NULL, Password VARCHAR(100) NOT NULL, UserRole VARCHAR(50) NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS Transactions (TransactionID INTEGER PRIMARY KEY, TransactionDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, TransactionType VARCHAR(50) NOT NULL, Amount NUMERIC(10, 2) NOT NULL, DealerID INTEGER, CustomerID INTEGER, TransactionStatus VARCHAR(20) DEFAULT "Pending", Category VARCHAR(50), Comments VARCHAR(255), CONSTRAINT fk_Party1 FOREIGN KEY (DealerID) REFERENCES User(UserID), CONSTRAINT fk_Party2 FOREIGN KEY (CustomerID) REFERENCES User(UserID))')

connection.commit()
connection.close()

@app.route('/show_all_users')
def show_all_users():
    connection = sqlite3.connect('Market.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    connection.close()
    return jsonify(users)

@app.route('/register_User', methods=['POST'])
def register_User():
    data = request.get_json()
    connection = sqlite3.connect('Market.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO User (UserID, Username, Password, UserRole) VALUES (?, ?, ?, ?)", (data['UserID'], data['Username'], data['Password'], data['UserRole']))
    connection.commit()
    connection.close()
    return "User created Successfully"

@app.route('/register_transactions', methods=['POST'])
def register_transactions():
    data = request.get_json()
    connection = sqlite3.connect('Market.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Transactions (TransactionID, TransactionDateTime, TransactionType, Amount, DealerID, CustomerID, TransactionStatus, Category, Comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['TransactionID'], data['TransactionDateTime'], data['TransactionType'], data['Amount'], data['DealerID'], data['CustomerID'], data['TransactionStatus'], data['Category'], data['Comments']))
    connection.commit()
    connection.close()
    return "Transaction created Successfully"

if __name__ == '__main__':
    app.run(port=5006)
