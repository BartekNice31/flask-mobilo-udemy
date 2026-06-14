from flask import Flask, url_for, request, redirect, render_template, flash, g,session 
from datetime import datetime 
import sqlite3 
import os 
from notification_priorities import NotificationPriorities

import hashlib
import random
import string
import binascii 

app=Flask(__name__) #
app.config["SECRET_KEY"]="123goniszty"
path_cantor_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
path_notifications_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
# path_cantor_db=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
# path_notifications_db=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
app_info={'db_cantor':path_cantor_db
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
        
class UserPass:
    def __init__(self,user='',password=''):
        self.user=user
        self.password=password
        self.email=''
        self.is_valid=False
        self.is_admin=False
    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii') 
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000) 
        pwdhash = binascii.hexlify(pwdhash) 
        return (salt + pwdhash).decode('ascii')
    def verify_password(self, stored_password, provided_password):
        """    Verify a stored password against one provided by user.    """
        salt = stored_password[:64]
        stored_password = stored_password[64:]

        pwdhash = hashlib.pbkdf2_hmac('sha512',
            provided_password.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )

        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == stored_password


    def get_random_user_password(self):
        random_user = ''.join(
            random.choice(string.ascii_lowercase)
            for i in range(3)
        )

        self.user = random_user

        password_characters = string.ascii_letters
        # password_characters = (
        #     string.ascii_letters +
        #     string.digits +
        #     string.punctuation
        # )

        random_password = ''.join(
            random.choice(password_characters)
            for i in range(3)
        )

        self.password = random_password
    def login_user(self):
        db=get_db()
        sql_statement='select id,name,email,password,is_active,is_admin from users where name=?;'
        user_record=db.execute(sql_statement,[self.user]).fetchone()
        if user_record!=None and self.verify_password(user_record['password'],self.password):
            return user_record
        else:
            self.user=None
            self.password=None
            return None 
    def get_user_info(self):
        db=get_db()
        sql_statement='select name,email,is_active,is_admin from users where name=?'
        cur=db.execute(sql_statement,[self.user])
        db_user=cur.fetchone()
        if db_user is None:
            self.email=''
            self.is_valid=False
            self.is_admin=False
        elif db_user['is_active']!=1:
            self.email=db_user['email']
            self.is_admin=False
            self.is_valid=False
        else:
            self.is_valid=True
            self.is_admin=db_user['is_admin']
            self.email=db_user['email']


#hec uzytkownik haslo PRH
@app.route('/init_app')
def init_app():
    # check if there are users defined
    # (at least one active admin required)

    db = get_db()

    sql_statement = '''
        SELECT count(*) AS cnt
        FROM users
        WHERE is_active AND is_admin;
    '''

    cur = db.execute(sql_statement)
    active_admins = cur.fetchone()

    if active_admins is not None and active_admins['cnt'] > 0:
        flash('Application is already set-up. Nothing to do')
        return redirect(url_for('index'))

    # if not - create/update admin account
    # with a new password and admin privileges

    user_pass = UserPass()
    user_pass.get_random_user_password()

    sql_statement = '''
        INSERT INTO users(
            name,
            email,
            password,
            is_active,
            is_admin
        )
        VALUES (?, ?, ?, True, True);
    '''

    db.execute(
        sql_statement,
        [
            user_pass.user,
            'noone@nowhere.no',
            user_pass.hash_password()
        ]
    )

    db.commit()

    flash(
        'User {} with password {} has been created'.format(
            user_pass.user,
            user_pass.password
        )
    )

    return redirect(url_for('index')) 
        
@app.route("/login",methods=["GET","POST"])
def login():
    login=UserPass(session.get('user'))
    login.get_user_info()
    if request.method=='GET':
        return render_template('login.html',active_menu='login',login=login)
    else:
        user_name='' if not 'user_name' in request.form else request.form['user_name']
        user_pass='' if not 'user_pass' in request.form else request.form['user_pass']
        login=UserPass(user=user_name,password=user_pass)
        user_record=login.login_user()
        if user_record!=None:
            session['user']=user_name
            flash('Succesfully log in,welcome: {}'.format(user_name))
            return redirect(url_for('index'))
        else:
            flash('Failed log in, please try again')
            return render_template('login.html',active_menu='login',login=login)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user',None)
        flash("SUCCESFULLY LOGGED OUT")
    return redirect(url_for("index"))
    
@app.route('/') 
def index(): 
    login=UserPass(session.get('user'))
    login.get_user_info()
    return render_template('index.html') 

@app.route('/notification', methods=['GET', 'POST']) 
def notification(): 

    notification_priorities = NotificationPriorities() 
    notification_priorities.load_priorities() 
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))
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

@app.route('/user_change_status/<action>/<user_name>')
def user_status_change(action,user_name):
    if not 'user' in session:
        return redirect(url_for('login'))
    login=session['user']
    db=get_db()
    if action=='active':
        db.execute('update users set is_active=(is_active+1)%2 where name=? and name<>?'
                ,[user_name,login])
        db.commit()
        flash("CHANGE USER STATUS")
    elif action=='admin':
        db.execute('update users set is_admin=(is_admin+1)%2 where name=? and name<>?'
                   ,[user_name,login])
        db.commit()
        flash("CHANGE ADMIN STATUS")
    return redirect(url_for('users'))

@app.route("/users")
def users():
    db=get_db()
    responses=db.execute('select *from users').fetchall()
    for r in responses:
        print(dict(r))
    sql_statement='select id,name,email,password from users;'
    users=db.execute(sql_statement).fetchall()
    return render_template('users.html',users=users,active_menu='users')

@app.route("/edit_user/<user_name>",methods=["GET","POST"])
def edit_user(user_name):
    if not 'user' in session:
        return redirect(url_for('login'))
    db=get_db()
    cur=db.execute('select name,email from users where name=?',[user_name])
    user=cur.fetchone() 

    if user is None:
        flash(f'No such user: {user}')
        return redirect(url_for('users'))
    if request.method=='GET':
        return render_template('edit_user.html',active_menu='users',user=user)
    else:
        new_email='' if not request.form else request.form['email']
        new_password='' if not request.form else request.form['user_pass']

        if new_email!=user['email']:
            db.execute('update users set email=? where name=?'
                       ,[new_email,user_name])
            db.commit()
            flash('Email has been changed from {} to {}'.format(user['email'],new_email))
        if new_password!='':
            userPass=UserPass(user=user_name,password=new_password)
            db.execute('update users set password=? where name=?',
                       [userPass.hash_password(),user_name])
            db.commit()
            flash('Password has been changed')
        return redirect(url_for('users'))
@app.route("/delete_user/<user_name>",methods=["GET","POST"])
def delete_user(user_name):
    db=get_db()
    if not 'user' in session:
        return redirect(url_for('login'))
    login=session['user']
    sql_command='delete from users where name=? and name<>?'
    
    if login==user_name:
        flash(f"CAN NOT TO DELETE ACTUALLY LOGGED IN USER:\n{login}")
        return redirect(url_for('users'))
    else:
        db.execute(sql_command,[user_name,login])
        db.commit()
        return redirect(url_for('users'))

@app.route("/new_user",methods=["GET","POST"])
def new_user():
    if not 'user' in session:
        return redirect(url_for("login"))
    db=get_db()
    user={}
    message=None
    if request.method=="GET":
        return render_template('new_user.html',active_menu='users',user=user)
    else:
        user['user_name']='' if not 'user_name' in request.form else request.form['user_name']
        user['email']='' if not 'email' in request.form else request.form['email']
        user['user_pass']='' if not 'user_pass' in request.form else request.form['user_pass']
        
        sql_statement_unique_name='select count(*) as cnt from users where name=?'
        record=db.execute(sql_statement_unique_name,[user['user_name']]).fetchone()
        is_name_unique=(record['cnt']==0)
        
        sql_statement_unique_email='select count(*) as cnt from users where email=?'
        record=db.execute(sql_statement_unique_email,[user['email']]).fetchone()
        is_email_unique=(record['cnt']==0)
        
        if user['user_name']=='':
            message='user name can not be empty'
        if user['user_pass']=='':
            message='user password can not be empty'
        if user['email']=='':
            message='user email can not be empty'
        elif not is_name_unique:
            message=f"user with name={user['user_name']} exists"
        elif not is_email_unique:
            message=f"user with email={user['email']} exists" 
        if not message:
            user_pass=UserPass(user=user['user_name'],password=user['user_pass'])
            hash_password=user_pass.hash_password()
            sql_command=f"insert into users(name,email,password,is_active,is_admin) \
                values(?,?,?,True,False)"
            db.execute(sql_command,[user['user_name'],user['email'],hash_password])
            db.commit()
            flash(f"User={user['user_name']} has been created!")
            return redirect(url_for('users'))
        else:
            flash(f"Please, correct an error: {message}")
            return render_template('new_user.html',active_menu='users',user=user)
            
if __name__=="__main__":
    app.run(port=5004)