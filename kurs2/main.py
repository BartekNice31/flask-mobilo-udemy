from flask import Flask
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from python</h1>"

@app.route("/cantor/<string:currency>/<float:amount>")
def cantor(currency:str,amount:float):
    message=f"<h1>You selected currency: {currency}\
        and amount: {amount}</h1>"
    return message

@app.route("/temperature/<float:temperature>")
def temperature(temperature:float):
    temperature=float(temperature)
    if not isinstance(temperature,float):
        return "<h1>Type of entered temperature is not correct</h1>"
    else:
        return f"<h1>Temperature: {temperature} *C\
                    Temperature: {temperature*(9.0/6.0)+32.0} F\
                    Temperature: {temperature} K</h1>"
@app.route("/about")
def about():
    return "<h1>We are programmers</h1>"

@app.route("/python_version")
def python_version():
    version=sys.version
    return f"<h1>You are working on {version}</h1>"    

if __name__=="__main__":
    app.run()