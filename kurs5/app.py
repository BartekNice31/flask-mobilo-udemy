from flask import Flask,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r"C:\Users\barte\Desktop\python projekty\flask mobilo udemy\.flaskenv")

app=Flask(__name__)

@app.route("/")
def index(): 
    color='black'
    if 'color' in request.args:
        color=request.args['color']
    style='normal'
    if 'style' in request.args:
        style=request.args['style'] 

    print('-'*30)
    print("Received arguments:")
    for arg in request.args:
        print(f"key:{arg}")
        print(f"value={request.args[arg]}")
        print('-'*30)

    return f'<h1 style="color: {color};font-style:{style};">\
        Hello world</h1>'

@app.route("/cantor/<string:currency>/<float:amount>")
def cantor(currency:str,amount:float):
    message=f"<h1>You selected currency: {currency}\
        and amount: {amount}</h1>"
    return message

@app.route("/user_data_form")
def user_data_form():
    body='''
    <form id="exchange_form" action="/user_data_form_process" method="POST">
    <label for="first_name">First Name</label>
    <input type="text" id="first_name" name="first_name" value="Bartek"><br>
    <label for="last_name">Last Name</label>
    <input type="text" id="last_name" name="last_name" value="Nicewicz"><br>
    <label for="age">Age</label>
    <input type="age" id="age" name="age" value="33"><br>
    <label>Are you over 18 years old?
    <input type="checkbox" name="check_age" id="check_age">
    </label>
    <input type="submit" value="Send user form">
    </form>
    '''
    return body

@app.route("/user_data_form_process",methods=["POST"])
def user_data_form_process():
    first_name=""
    last_name=""
    age=""

    if "first_name" in request.form:
        first_name=request.form["first_name"]

    if "last_name" in request.form:
        last_name=request.form['last_name']

    if "age" in request.form:
        age=request.form["age"]
    
    body=f"<h1>Your first name={first_name} last name={last_name} age={age}</h1>"
    return body

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    if request.method=="GET":
        body='''
        <form id="exchange_form" action="/exchange" method="POST">
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

@app.route("/exchange_process",methods=["POST"])
def exchange_process():
    currency='EUR'
    if 'currency' in request.form:
        currency=request.form['currency']
    amount='100'
    if 'amount' in request.form:
        amount=request.form['amount']

    body=f"<h1>You want to exchange {currency} {amount}</h1>"   
    return body

@app.route("/plc_request")
def plc_request():
    body='''
    <form id="exchange_form" action="plc_request_process" method="POST">
    <label for="PLC NAME">PLC NAME</label>
    <input type="text" id="plc_name" name="plc_name" value="plc1"><br>
    <label for="PLC ID ADDRESS">PLC ADDRESS IP</label>
    <input type="text" id="plc_address_ip" name="plc_address_ip" value="192.168.0.1"><br>
    <input type="submit" value="SEND INFO">
    </form>
    '''
    return body

@app.route("/plc_request_process",methods=["POST"])
def plc_request_process():
    plc_name="plc1"
    plc_address_ip="192.168.0.1"

    if plc_name in request.form:
        plc_name=request.form["plc_name"]
    if plc_address_ip in request.form:
        plc_address_ip=request.form["plc_address_ip"]   

    body=f"<h1>{plc_name} {plc_address_ip}</h1>"
    return body

@app.route("/about")
def about():
    return "<h1>We are programmers</h1>"

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