from flask import Flask,request,url_for,render_template
from dotenv import load_dotenv
import os
import sys
load_dotenv(r"C:\Users\bNicewicz\Desktop\python\flask-mobilo-udemy-main\.flaskenv")

app=Flask(__name__)
@app.route("/")
def index():
    return "This is index"

@app.route("/exchange"
           ,methods=['GET','POST']
           )
def exchange():
    # if request.method=='POST':
    #     return "Formularz exchange odebrany"
    return render_template('exchange.html')

@app.route("/user_form",methods=["GET","POST"])
def user_form():
    if request.method=='POST':
        return "Formularz user form odebrany"
    return render_template('user_form.html')

if __name__=="__main__":
    app.run(port=5002)