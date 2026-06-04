from flask import Flask,render_template,url_for,request,flash
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from notification_priorities import NotificationPriorities
from priority_type import PriorityType
load_dotenv(r".flaskenv")

app=Flask(__name__)
app.config["SECRET_KEY"]="SomethingWhatNo1CanSee"
@app.route("/")
def route():
    return "<h1>Hello from HOTEL WARSAW 101</h1>"  

@app.route("/notification",methods=["GET","POST"])
def notification():
    notification_priorities=NotificationPriorities()
    notification_priorities.load_priorities()
    if request.method=="GET":
        print("METHOD GET")
        return render_template("notification.html"
                            ,notification_priorities=notification_priorities)
    else:
        flash("Notification has been sent")
        room_number=2
        guest_name="BARTEK"
        Notification="Damaged table in the room"
        selected="NOT URGENT"
        if 'room_number' in request.form:
            room_number=request.form['room_number']
        if 'guest_name' in request.form:
            guest_name=request.form['guest_name']
        if 'Notification' in request.form:
            Notification=request.form['Notification']
        if 'selected' in request.form:
            selected=request.form['selected']
        time_now=datetime.now()
        # hour_now=time_now.hour
        hour_now=14
        if selected=="MEDIUM" and (hour_now>=22 and hour_now<=24):
            selected="HIGH PRIORITY"
            flash("Rising priority from medium to high") 
            print("Rising priority from medium to high")  
        elif selected=="MEDIUM" and (hour_now>=0 and hour_now<=6):
            selected="HIGH PRIORITY"
            flash("Rising priority from medium to high")  
            print("Rising priority from medium to high")   
        else:
            selected=request.form['selected']

        print(selected)
        print("METHOD POST")
        return render_template("notification_results.html"
                            ,room_number=room_number
                            ,guest_name=guest_name
                            ,Notification=Notification
                            ,priority_info=notification_priorities.get_priority_by_code(code=selected))

if __name__=="__main__":
    app.run()