from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app=Flask(__name__)   
app.config.from_pyfile('config.cfg')
db=SQLAlchemy(app)

class Vendor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    discount=db.Column(db.Integer)
    active=db.Column(db.Boolean)
    
class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(50))
    lastname=db.Column(db.String(50))
    age=db.Column(db.Integer)
    
class Employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(50))
    lastname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    work_station=db.Column(db.String(20))
    
class TemperatureSensors(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    sensor1=db.Column(db.Float)
    sensor2=db.Column(db.Float)
    sensor3=db.Column(db.Float)
    sensor4=db.Column(db.Float)

class Author(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    Special=db.Column(db.Boolean)
    
class LeakTester1(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    leak_test_value=db.Column(db.Float)
    leak_test_pressure=db.Column(db.Float)
    catalyst_code=db.Column(db.String(24))

@app.route("/")
def index():
    db.create_all()
    return "hello"

if __name__=="__main__":
    app.run()