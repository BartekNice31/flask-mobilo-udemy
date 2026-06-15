from flask import Flask,render_template,redirect,g,request
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField,FloatField


class BookWorm(FlaskForm):
    title=StringField('Book title')
    amount=IntegerField('Amount')
    available=BooleanField('Available')
    
class UserRegistration(FlaskForm):
    login=StringField('User name')
    password=StringField('User Password')
    email=StringField('User email') 
    age=IntegerField('User Age')
    
app=Flask(__name__)
app.config['SECRET_KEY']='Acomplited'

@app.route("/",methods=["POST","GET"])
def index():
    bookform=BookWorm()
    if bookform.validate_on_submit():
        return f'''<h1>Hello from flask form</h1>
                    <ul>
                        <li>{bookform.title.label}:{bookform.title.data}</li>
                        <li>{bookform.amount.label}:{bookform.amount.data}</li>
                        <li>{bookform.available.label}:{bookform.available.data}</li>
                    </ul>
                '''
    return render_template('index.html',form=bookform)

@app.route("/user_registration",methods=["GET","POST"])
def user_registration():
    form=UserRegistration()
    if form.validate_on_submit():
        return f"""<h1></h1>
                    <ul>
                        <li>{form.login.label}:{form.login.data}</li>
                        <li>{form.password.label}:{form.password.data}</li>
                        <li>{form.email.label}:{form.email.data}</li>
                        <li>{form.age.label}:{form.age.data}</li>
                    </ul>
                """
    return render_template('user_registration.html',form=form)

if __name__=='__main__':
    app.run(port=5004)