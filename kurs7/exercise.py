#  app.py
from flask import Flask,request,url_for,render_template
from dotenv import load_dotenv
import os
import sys
load_dotenv(r"C:\Users\bNicewicz\Desktop\python\flask-mobilo-udemy-main\.flaskenv")

app = Flask(__name__)

@app.route('/notification', methods=['GET', 'POST'])
def notification():

    if request.method == 'GET':
        return render_template('notification.html')
    else:
        room_number = request.form['room_number'] if 'room_number' in request.form else ''
        guest_name = request.form['guest_name'] if 'guest_name' in request.form else ''
        notification_text =  request.form['notification_text'] if 'notification_text' in request.form else ''

        return render_template('notification_content.html',
                room_number=room_number, guest_name=guest_name, notification_text=notification_text)

if __name__=="__main__":
    app.run()