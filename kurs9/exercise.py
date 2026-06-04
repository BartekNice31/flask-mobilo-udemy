from flask import Flask,render_template,url_for,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from HOTEL WARSAW 101</h1>"  

@app.route("/notification",methods=["GET","POST"])
def notification():
    if request.method=="GET":
        print("METHOD GET")
        return render_template("notification.html")
    else:
        room_number=2
        guest_name="BARTEK"
        Notification="Damaged table in the room"
        if 'room_number' in request.form:
            room_number=request.form['room_number']
        if 'guest_name' in request.form:
            guest_name=request.form['guest_name']
        if 'Notification' in request.form:
            Notification=request.form['Notification']
        print("METHOD POST")
        return render_template("notification_results.html"
                            ,room_number=room_number
                            ,guest_name=guest_name
                            ,Notification=Notification)

if __name__=="__main__":
    app.run()