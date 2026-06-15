from flask import Flask,render_template,flash,url_for,request,flash,g,redirect,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import random
import string
import hashlib
import binascii

#app.app_context().push()
app=Flask(__name__) 
path_database_config=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_alchemy\config_cantor.cfg"  
#path_database_config=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_alchemy\config_cantor.cfg"  
app.config.from_pyfile(path_database_config)
db=SQLAlchemy(app)

class Transaction(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    currency=db.Column(db.String(5),)
    amount=db.Column(db.Integer)
    user=db.Column(db.String(30))
    trans_date=db.Column(db.Date())

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.Text)
    is_active=db.Column(db.Boolean())
    is_admin=db.Column(db.Boolean())
    
class Currency:
    def __init__(self,code,name,flag):
        self.code=code
        self.name=name
        self.flag=flag
    def __repr__(self):
        return f"<Currency({self.code})>"
    
class CantorOffer:
    def __init__(self):
        self.currencies=[]
        self.denies_codes=[]
    def load_offer(self):
        self.currencies.append(Currency(code='USD',name='Dollar',flag='flag_usa.png'))
        self.currencies.append(Currency(code='EUR',name='Euro',flag='flag_euro.png'))
        self.currencies.append(Currency(code='JPY',name='Yen',flag='flag_japan.png'))
        self.currencies.append(Currency(code='GBP',name='Pound',flag='flag_england.png'))
        self.denies_codes.append('USD')
    def get_by_code(self,code):
        for currency in self.currencies:
            if currency.code==code:
                return currency
        return Currency(code='unknown',name='unknown',flag='flag_pirat.png')
    
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
        user_record=User.query.filter(User.name==self.user).first()
        if user_record!=None and self.verify_password(user_record.password,self.password):
            return user_record
        else:
            self.user=None
            self.password=None
            return None
    def get_user_info(self):  
        db_user=User.query.filter(User.name==self.user).first()

        if db_user is None:
            self.email=''
            self.is_valid=False
            self.is_admin=False
        elif db_user.is_active!=1:
            self.email=db_user.email
            self.is_valid=False
            self.is_admin=False        
        else:
            self.email=db_user.email
            self.is_valid=True
            self.is_admin=db_user.is_admin
            
@app.route('/init_app')
def init_app():
    db.create_all()
    # check if there are users defined
    # (at least one active admin required)  
    active_admins = User.query.filter(User.is_admin,User.is_active).count()

    if active_admins > 0:
        flash('Application is already set-up. Nothing to do')
        return redirect(url_for('index')) 
    
    user_pass = UserPass()
    user_pass.get_random_user_password()
    # class User(db.Model):
    #     id=db.Column(db.Integer,primary_key=True)
    #     name=db.Column(db.String(100))
    #     email=db.Column(db.String(100))
    #     password=db.Column(db.Text)
    #     is_active=db.Column(db.Boolean())
    #     is_admin=db.Column(db.Boolean())
    new_admin=User(id=1,name=user_pass.user
                ,email='noone@nowhere.no'
                ,password=user_pass.hash_password()
                ,is_active=True,is_admin=True)
    db.session.add(new_admin)
    db.session.commit()

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
    if login.is_valid and not login.is_valid:
        flash("Logged as user")
    if login.is_admin and login.is_valid:
        flash("Logged as admin")

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
        session.pop("user",None)
        flash("Succesfully log out")
    return redirect(url_for("login"))

@app.route("/")
def index():
    login=UserPass(session.get('user'))
    login.get_user_info()

    return render_template("index.html",time_now=datetime.now()
                           ,author="@BARTEK_N",active_menu='home',login=login)
    
@app.route("/exchange",methods=["GET","POST"])
def exchange():
    offer=CantorOffer()
    offer.load_offer()
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))
    if request.method=="GET":
        
        return render_template("exchange.html",offer=offer,login=login)
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
            # class Transaction(db.Model):
            #     id=db.Column(db.Integer,primary_key=True)
            #     currency=db.Column(db.String(5),)
            #     amount=db.Column(db.Integer)
            #     user=db.Column(db.String(30))
            #     trans_date=db.Column(db.Date())
            new_transaction=Transaction(currency=currency
                                        ,amount=amount
                                        ,user=session['user']
                                        ,trans_date=datetime.utcnow().date()
                                        #,trans_date=datetime.utcnow()
                                        )
            db.session.add(new_transaction)
            db.session.commit()
            print(currency,amount)
            flash(f"Request to exchange {currency} was accepted")        
        
        
        return render_template("exchange_results.html"
                            ,active_menu='exchange'
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency)
                            ,login=login)

@app.route("/columns_grid")
def columns_grid():
    return render_template("columns.html")
@app.route("/history")
def history():
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))
 
    transactions=Transaction.query.all()
    return render_template("history.html",active='history',transactions=transactions,login=login)

@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction(transaction_id:int):
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login')) 
    
    transaction_to_delete=Transaction.query.filter(Transaction.id==transaction_id).first()
    db.session.delete(transaction_to_delete)
    db.session.commit()

    return redirect(url_for('history'))

@app.route("/edit_transaction/<int:transaction_id>"
        ,methods=["GET","POST"])
def edit_transaction(transaction_id:int):
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login')) 
    offer=CantorOffer()
    offer.load_offer() 
    
    if request.method=="GET":
        transaction_to_edit=Transaction.query.filter(Transaction.id==transaction_id).first()
        if transaction_to_edit is None:
            flash(f"Transaction id={transaction_id} no founded at database")
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html'
                                ,transaction=transaction_to_edit
                                ,offer=offer
                                ,active_menu='history'
                                ,login=login) 
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
        
            print(currency,amount)
            flash("Transaction was updated")     
        transaction_to_edit.currency=currency
        transaction_to_edit.amount=amount
        transaction_to_edit.user=session['login']
        transaction_to_edit.trans_date=datetime.utcnow().date()
        db.session.commit()   
        return redirect(url_for('history'))
    
@app.route("/users")
def users():
    login=UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))
    if login.is_valid:
        if not login.is_admin:
            flash('Please,log as admin')
            return redirect(url_for('login'))
    
    users=User.query.all()
    return render_template('users.html',active_menu='users',users=users,login=login)  

@app.route("/user_status_change/<action>/<user_name>")
def user_status_change(action,user_name): 
    login=UserPass(session.get("user"))
    login.get_user_info()
    if not login.is_admin and not login.is_valid:
        flash("Please, log as admin")
        return redirect(url_for('login')) 
    active_user=User.query.filter(User.name==login).first()
    if action=='active':
        # db.execute('update users set is_active=(is_active+1)%2 where name=? and name<>?'
        #            ,[user_name,login.user])
        if active_user.name==user_name and active_user.name!=login.user:
            active_user.is_active=(active_user.is_active+1)%2
            db.session.commit()
            print("change user status")
            flash("change user status") 
        print('no changes')
    elif action=='admin':
        if active_user.name==user_name and active_user.name!=login.user:
            active_user.is_active=(active_user.is_admin+1)%2
            db.session.commit()
            print("Change admin status")
            flash("Change admin status")
        # db.execute('update users set is_admin=(is_admin + 1) % 2 where name=? and name<>?'
        #            ,[user_name,login.user])
        print('no changes')
    return redirect(url_for('users'))

@app.route("/edit_user/<user_name>",methods=["GET","POST"])
def edit_user(user_name):
    login=UserPass(session.get("user"))
    login.get_user_info()
    if not login.is_admin and not login.is_valid:
        flash("Please, log as admin")
        return redirect(url_for('login')) 
    user=User.query.filter(User.name==user_name).first()
    message=None
    if user is None:
        flash(f"no such user: {user_name}")
    if request.method=='GET':
        return render_template('edit_user.html',active_menu='users',user=user)
    else:
        login=session['user']
        new_email='' if not 'email' in request.form else request.form['email']
        new_password='' if not 'user_pass' in request.form else request.form['user_pass']

        if new_email!=user.email:
            # db.execute('update users set email=? where name=?',[new_email,user_name])
            user.email=new_email
            db.session.commit()
            flash(f'Changing email to {new_email}')
        if new_password!='':
            userPass=UserPass(user=user_name,password=new_password)
            # db.execute('update users set password=? where name=?'
            #         ,[userPass.hash_password(),user_name])
            user.password=new_password
            db.session.commit()
            flash('Password has been changed') 
        return redirect(url_for('users'))
    
@app.route("/delete_user/<user_name>")
def delete_user(user_name):
    login=UserPass(session.get("user"))
    if not login.is_admin and not login.is_valid:
        flash("Please, log as admin")
        return redirect(url_for('login')) 

    is_admin=False
    # record=db.execute('select *from users where name=?',[user_name]).fetchone()
    record=User.filter.query(User.name==user_name).first()
    if record.is_admin==1:
        flash(f'Can not to remove admin user {user_name}')
        return redirect(url_for("users"))
    else:
        if user_name==login:
            flash(f'Can not to remove actually logged in user: {login}')
            return redirect(url_for("users"))
        else:
            db.session.delete(record)
            db.session.commit()
        return redirect(url_for("users"))
    
@app.route("/new_user",methods=["GET","POST"])
def new_user():
    login=UserPass(session.get("user"))
    login.get_user_info()
    if not login.is_admin and not login.is_valid:
        flash("Please, log as admin")
        return redirect(url_for('login')) 
    message=None
    user={}
    if request.method=='GET':
        return render_template('new_user.html',active_menu="users",user=user,login=login)
    else:
        user['user_name']='' if 'user_name' not in request.form else request.form['user_name']
        user['email']='' if 'email' not in request.form else request.form['email']
        user['user_pass']='' if 'user_pass' not in request.form else request.form['user_pass']
        
        # sql_statement='select count(*) as cnt from users where user=?'
        # record=db.execute('select count(*) as cnt from users where name=?',[user['user_name']]).fetchone()
        # is_user_name_unique=(record['cnt']==0)
        
        record=User.query.filter(User.name==user['user_name']).count()
        is_user_name_unique=(record==0)
        
        # sql_statement='select count(*) as cnt from users where email=?'
        # record=db.execute('select count(*) as cnt from users where email=?',[user['email']]).fetchone()
        record=User.query.filter(User.email==user['email']).count()
        is_user_email_unique=(record==0)
        
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
            # sql_command="insert into users (name,email,password,is_active,is_admin) \
            #     values(?,?,?,True,False)"
            # db.execute(sql_command,[user['user_name'],user['email'],password_hash])
            # db.commit()
            new_user=User(name=user['user_name']
                        ,email=user['email']
                        ,password=password_hash
                        ,is_active=True
                        ,is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User: {user['user_name']} has been created")
            return redirect(url_for('users'))
        else:
            flash(f"Correct an error: {message}")
            return render_template('new_user.html',active_menu='users',user=user,login=login)
if __name__=="__main__":
    app.run(port=5003)