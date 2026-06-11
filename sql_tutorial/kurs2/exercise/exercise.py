from flask import Flask, url_for, request, redirect, render_template, flash, g 
from datetime import datetime 
import sqlite3 
import os 
from notification_priorities import NotificationPriorities

app=Flask(__name__) 
app.config["SECRET_KEY"]="123goniszty"
path_cantor_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
path_notifications_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
app_info={'db_notifications':path_notifications_db
          ,'db_notifications':path_notifications_db}
 
 
def get_db(): 
    if not hasattr(g, 'sqlite_db'): 
        conn = sqlite3.connect(app_info['db_notifications']) 
        conn.row_factory = sqlite3.Row 
        g.sqlite_db = conn 
    return g.sqlite_db 
 
@app.teardown_appcontext 
def close_db(error): 
    if hasattr(g, 'sqlite_db'): 
        g.sqlite_db.close() 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/notification', methods=['GET', 'POST']) 
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
 
        priority_type = notification_priorities.get_priority_by_code(priority) 
        print('found', priority_type.code) 
 
        flash('Notification has been sent') 
         
        the_hour = datetime.now().hour 
        raise_priority = (the_hour >= 20 or the_hour < 10) and priority == 'medium' 
         
        if raise_priority: 
            priority = 'high' 
            flash('Rising priority from medium to high') 
             
        db = get_db() 
        sql_command = 'insert into notifications(room_number, guest_name, notification, priority) values(?, ?, ?, ?)' 
        db.execute(sql_command, [room_number, guest_name, notification_text, priority]) 
        db.commit() 
 
        return render_template('notification_content.html', 
                room_number=room_number, guest_name=guest_name,  
                notification_text=notification_text, priority_type=priority_type) 
 
@app.route('/notifications') 
def notifications(): 
    db = get_db() 
    sql_command = 'select id, room_number, guest_name, notification, priority from notifications;' 
    cur = db.execute(sql_command) 
    notifications = cur.fetchall() 
 
    return render_template('notifications.html', active_menu='notifications', 
notifications=notifications) 

 
@app.route('/delete_notification/<int:notification_id>') 
def delete_notification(notification_id): 
 
    db = get_db() 
    sql_statement = 'delete from notifications where id = ?;' 
    db.execute(sql_statement, [notification_id]) 
    db.commit() 
 
    return redirect(url_for('notifications')) 

@app.route('/edit_notification/<int:notification_id>',methods=["GET","POST"])
def edit_notification(notification_id:int):
    notification_priorities = NotificationPriorities() 
    notification_priorities.load_priorities() 
    db=get_db()
    if request.method == 'GET': 
        sql_statement='select id,room_number,guest_name,notification,priority\
              from notifications where id=?'
        notif_obj=db.execute(sql_statement,[notification_id]).fetchone()
        if notification==None:
            flash(f"No founded notification id={notification_id}")
            return redirect('notifications')
        else: 
            return render_template('edit_notification.html'
                                , active_menu='notifications'
                                ,notif_obj=notif_obj 
                                ,list_of_priorities=notification_priorities.list_of_priorities)
    else: 
        room_number = request.form['room_number'] if 'room_number' in request.form else '' 
        guest_name = request.form['guest_name'] if 'guest_name' in request.form else '' 
        notification_text =  request.form['notification_text'] if 'notification_text' in request.form else '' 
        priority = request.form['priority'] if 'priority' in request.form else 'normal' 
 
        priority_type = notification_priorities.get_priority_by_code(priority) 
        print('found', priority_type.code) 
 
        flash('Notification has been sent') 
         
        the_hour = datetime.now().hour 
        raise_priority = (the_hour >= 20 or the_hour < 10) and priority == 'medium' 
         
        if raise_priority: 
            priority = 'high' 
            flash('Rising priority from medium to high') 
        #sql_command = 'insert into notifications(room_number, guest_name, notification, priority) values(?, ?, ?, ?)' 
        sql_command="update notifications\
            set room_number=?,guest_name=?,notification=?,priority=?,date_notification=? \
                where id=?"
        db.execute(sql_command
                ,[room_number, guest_name, notification_text, priority,datetime.utcnow(),notification_id]) 
        db.commit() 
        flash("Notification was updated")
        return redirect(url_for('notifications'))

@app.route('/about') 
def about(): 
    return render_template('about.html') 

if __name__=="__main__":
    app.run(port=5004)