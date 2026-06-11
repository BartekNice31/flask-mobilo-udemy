from flask import Flask,render_template,url_for,request,flash
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from notification_priorities import NotificationPriorities
from priority_type import PriorityType
# load_dotenv(r".flaskenv")
load_dotenv(r'C:\Users\bNicewicz\Desktop\python\flask-mobilo-udemy-main\.flaskenv')

app=Flask(__name__)
app.config["SECRET_KEY"]="SomethingWhatNo1CanSee"
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/notification",methods=["GET","POST"])
def notification():
    notification_priorities = NotificationPriorities()
    notification_priorities.load_priorities()

    if request.method == 'GET':
        return render_template('notification.html', 
                            list_of_priorities=notification_priorities.list_of_priorities)
    else:
        room_number = request.form['room_number'] if 'room_number' in request.form else ''
        guest_name = request.form['guest_name'] if 'guest_name' in request.form else ''
        notification_text =  request.form['notification_text'] if 'notification_text' in request.form else ''
        priority = request.form['priority'] if 'priority' in request.form else 'normal'

        flash('Notification has been sent')
        
        the_hour = datetime.now().hour
        raise_priority = (the_hour >= 20 or the_hour < 6) and priority == 'medium'
        
        if raise_priority:
            priority = 'high'
            flash('Rising priority from medium to high')

        priority_type = notification_priorities.get_priority_by_code(priority)
        print('found', priority_type.code)

        return render_template('notification_content.html',
                room_number=room_number, guest_name=guest_name, 
                notification_text=notification_text, priority_type=priority_type)


if __name__=="__main__":
    app.run(port=5003)