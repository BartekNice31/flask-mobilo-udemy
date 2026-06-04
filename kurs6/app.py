from flask import Flask,request,url_for
from dotenv import load_dotenv
import os
import sys
load_dotenv(r"C:\Users\barte\Desktop\python projekty\flask mobilo udemy\.flaskenv")

app=Flask(__name__)

@app.route("/")
def index(): 
    menu=f'''<h1>MENU</h1>
    <p>Go <a href="{url_for('exchange')}">here</a> to exchange money</p>
    <p>Go <a href="{url_for('user_form')}">here</a> to fill user form</p>
    <p>To exchange 50 CHF go <a href="{url_for('cantor',currency='CHF',amount=50,_external=True)}">here</a></p>
    '''
    return menu

@app.route("/cantor/<string:currency>/<float:amount>")
def cantor(currency:str,amount:float):
    message=f"<h1>You selected currency: {currency}\
        and amount: {amount}</h1>"
    return message

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    if request.method=="GET":
        body=f'''
        <form id="exchange_id" action="{url_for('exchange')}" method="POST">
        <label for="currency">Currency</label>
        <input type="text" id="currency" name="currency" value="EUR"><br>
        <label for="amount">Amount</label>
        <input type="text" id="amount" name="amount" value="100"><br>
        <input type="submit" value="Send">
        </form>
        '''
        return body
    else:
        currency='EUR'
        if 'currency' in request.form:
            currency=request.form['currency']
        amount='100'
        if 'amount' in request.form:
            amount=request.form['amount']

        body=f"<h1>You want to exchange {currency} {amount}</h1>"
        return body

@app.route("/user_form",methods=["GET","POST"])
def user_form():
    if request.method=="GET":
        body='''
        <form id='user_form' method='POST'>
        <label for='FIRST NAME'>FIRST NAME</label>
        <input type='text' id='FIRSTNAME' name='FIRST NAME' value='ENTER FIRST NAME'><br>
        <label for='LAST NAME'>LAST NAME</label>
        <input type='text' id='LASTNAME' name='LAST NAME' value='ENTER LAST NAME'><br>
        <label for='AGE'>AGE</label>
        <input type='text' id='AGE' name='AGE' value='ENTER AGE'><br>
        <label for='LIVING ADDRESS'>LIVING ADDRESS</label>
        <input type='text' id='ADDRESS' name='ADDRESS' value='ENTER ADDRESS'><br>
        <label for='GENDER'>GENDER
            <select id='SELECT_GENDER'>
            <option id='FEMALE' value='FEMALE'>FEMALE</option>
            <option id='MALE' value='MALE'>MALE</option>
            </select>
        </label>
        <input type='SUBMIT' value='SEND YOUR FORM'>
        </form>
        '''
        return body
    else:
        FIRSTNAME,LASTNAME,AGE,ADDRESS='','','',''
        if 'FIRSTNAME' in request.form:
            FIRSTNAME=request.form['FIRSTNAME']
        if 'LASTNAME' in request.form:
            LASTNAME=request.form['LASTNAME']
        if 'AGE' in request.form:
            AGE=request.form['AGE']
        if 'ADDRESS' in request.form:
            ADDRESS=request.form['ADDRESS']
        body=f"""<h1>TWOJE DANE:
            <p>IMIĘ:{FIRSTNAME}</p>
            <p>NAZWISKO:{LASTNAME}</p>
            <p>WIEK:{AGE}</p>
            <p>ADRES ZAMIESZKANIA:{ADDRESS}</p>
            </h1>"""
        return body


if __name__=="__main__":
    app.run()