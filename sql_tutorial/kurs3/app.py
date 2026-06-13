from flask import Flask,render_template,flash,url_for,request,flash,g,redirect,session
from datetime import datetime
import os
import sys
from author import Author
from cantor_offer import CantorOffer
import sqlite3

import random
import string
import hashlib
import binascii
#from user import User,UserPass

#wygenerowany przez ten dziwny kod użytkownik/hasło:
#User igo with password qdz has been created

app=Flask(__name__) 
app.config["SECRET_KEY"]="123goniszty"
# path_cantor_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
# path_notifications_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
path_cantor_db=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
path_notifications_db=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
app_info={'db_cantor':path_cantor_db
        ,'db_notifications':path_notifications_db}

def get_db():
    if not hasattr(g,'sqlite_db'):
        connection=sqlite3.connect(app_info["db_cantor"])
        connection.row_factory=sqlite3.Row
        g.sqlite_db=connection
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

class User:
    def __init__(self,user='',password=''):
        self.user=user
        self.password=password
    def hash_password(self):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
class UserPass:
    def __init__(self,user='',password=''):
        self.user=user
        self.password=password
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
        db=get_db()#'select id, name, email, password, is_active, is_admin from users where name=?'
        sql_statement='select id,name,email,password,is_active,is_admin from users where name=?'
        user_record=db.execute(sql_statement,[self.user]).fetchone()
        if user_record!=None and self.verify_password(user_record['password'],self.password):
            return user_record
        else:
            self.user=None
            self.password=None
            return None

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
    if request.method=='GET':
        return render_template('login.html',active_menu='login')
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
            return render_template('login.html')
        
@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop("user",None)
        flash("Succesfully log out")
    return redirect(url_for("login"))
    
@app.route("/")
def index():
    return render_template("index.html",time_now=datetime.now(),author=f"@{Author()}",active_menu='home')

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    offer=CantorOffer()
    offer.load_offer()
    
    if request.method=="GET":
        
        return render_template("exchange.html",offer=offer)
    else:
        flash("LOAD OFFER")
        flash("Debug starting exchange in POST mode")
        currency='EUR'

        if 'currency' in request.form:
            currency=request.form['currency']
        
        amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']

        if currency in offer.denies_codes:
            flash(f"Selected currency: {currency} can not be accepted")
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            db=get_db()
            sql_command="insert into transactions(currency,amount,user) values(?,?,?)"
            db.execute(sql_command,[currency,amount,'admin'])
            db.commit()
            print(currency,amount)
            flash(f"Request to exchange {currency} was accepted")        
        
        
        return render_template("exchange_results.html"
                            ,active_menu='exchange'
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency))
@app.route("/columns_grid")
def columns_grid():
    return render_template("columns.html")
@app.route("/history")
def history():
    db=get_db()
    query="select *from transactions"
    cur=db.execute(query)
    transactions=cur.fetchall()
    return render_template("history.html",active='history',transactions=transactions)

@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction(transaction_id:int):
    db=get_db()
    sql_statement="delete from transactions where id=?"
    db.execute(sql_statement,[transaction_id])
    db.commit()

    return redirect(url_for('history'))

@app.route("/edit_transaction/<int:transaction_id>"
        ,methods=["GET","POST"])
def edit_transaction(transaction_id:int):
    
    # currency=''
    # amount=''
    # user=''
    # sql_statement="update transactions set currency=?,amount=?,user=?";
    # db.execute(sql_statement(sql_statement)
    #            ,[currency,amount,user])
    offer=CantorOffer()
    offer.load_offer()
    db=get_db()
    if request.method=="GET":
        sql_statement="select id,currency,amount from transactions where id=?;"
        transaction=db.execute(sql_statement,[transaction_id]).fetchone()
        if transaction is None:
            flash(f"Transaction id={transaction_id} no founded at database")
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html'
                                ,transaction=transaction
                                ,offer=offer
                                ,active_menu='history')
        # return render_template("exchange.html",offer=offer)
    else:
        flash("LOAD OFFER")
        flash("Debug starting exchange in POST mode")
        currency='EUR'

        if 'currency' in request.form:
            currency=request.form['currency']
        
        amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']

        if currency in offer.denies_codes:
            flash(f"Selected currency: {currency} can not be accepted")
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            sql_command="update transactions\
                set currency=?\
                ,amount=? \
                ,user=? \
                ,trans_date=?\
                where id=?"
            db.execute(sql_command,[currency,amount,'admin',datetime.utcnow(),transaction_id])
            db.commit()
            print(currency,amount)
            flash("Transaction was updated")        
        return redirect(url_for('history'))

@app.route("/users")
def users():
    db=get_db()
    sql_statement='select id,name,email,is_active,is_admin from users'
    responses=db.execute(sql_statement).fetchall()
    for response in responses:
        print(f"User id: {response['id']}")
        print(f"User name: {response['name']}")
        print(f"User email: {response['email']}")
        print(f"User is_active: {response['is_active']}")
        print(f"User is_admin: {response['is_admin']}")
        print('-'*30)
    users=db.execute(sql_statement).fetchall()
    return render_template('users.html',active_menu='users',users=users)  

@app.route("/user_status_change/<action>/<user_name>")
def user_status_change(action,user_name):
    return "not implemented"

@app.route("/edit_user/<user_name>")
def edit_user(user_name):
    return "not implemented"

@app.route("/delete_user/<user_name>")
def delete_user(user_name):
    if not 'user' in session:
        return redirect("login")
    login=session['user']
    db=get_db()
    sql_command="delete from users where name=? and name<>?"
    db.execute(sql_command,[user_name,login])
    db.commit()
    return redirect(url_for("users"))
    
@app.route("/new_user",methods=["GET","POST"])
def new_user():
    if not 'user' in session:
        return redirect(url_for('login'))
    login=session['user']
    db=get_db()
    message=None
    user={}
    if request.method=='GET':
        return render_template('new_user.html',active_menu="users",user=user)
    else:
        user['user_name']='' if 'user_name' not in request.form else request.form['user_name']
        user['email']='' if 'email' not in request.form else request.form['email']
        user['user_pass']='' if 'user_pass' not in request.form else request.form['user_pass']
        
        sql_statement='select count(*) as cnt from users where user=?'
        record=db.execute('select count(*) as cnt from users where name=?',[user['user_name']]).fetchone()
        is_user_name_unique=(record['cnt']==0)
        
        sql_statement='select count(*) as cnt from users where email=?'
        record=db.execute('select count(*) as cnt from users where email=?',[user['email']]).fetchone()
        is_user_email_unique=(record['cnt']==0)
        
        is_correct=False
        if user['user_name']=='':
            message='user name can not be empty' 
        elif user['user_pass']=='':
            message='user password can not be empty' 
        elif user['email']=='':
            message='user email can not be empty' 
        elif not is_user_name_unique:
            message=f"user with name: {user['user_name']} exists"
        elif not is_user_email_unique:
            message=f"user with email: {user['email']} exists"
            
        if not message:
            is_correct=True
        if is_correct:
            user_pass=UserPass(user=user['user_name'],password=user['user_pass'])
            password_hash=user_pass.hash_password()
            sql_command="insert into users (name,email,password,is_active,is_admin) \
                values(?,?,?,True,False)"
            db.execute(sql_command,[user['user_name'],user['email'],password_hash])
            db.commit()
            flash(f"User: {user['user_name']} has been created")
            return redirect(url_for('users'))
        else:
            flash(f"Correct an error: {message}")
            return render_template('new_user.html',active_menu='users',user=user)
if __name__=="__main__":
    app.run(port=5003)