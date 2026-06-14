from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app=Flask(__name__) 
path_database_config=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_alchemy\config.cfg"  
app.config.from_pyfile(path_database_config)
db=SQLAlchemy(app)


    
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
    
    def __repr__(self):
        return f"Leaktester1 {self.id} {self.leak_test_value} {self.leak_test_pressure} {self.catalyst_code}"
    
    def __str__(self):
        return f"Leaktester1 {self.id} {self.leak_test_value} {self.leak_test_pressure} {self.catalyst_code}"
    
class Vendor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    discount=db.Column(db.Integer)
    active=db.Column(db.Boolean)
    
    def __repr__(self):
        return f"Vendor {self.id}/{self.name}"
    
    def __str__(self):
        return f"Vendor {self.id}/{self.name}/{self.discount}/{self.active}"
    
@app.route("/")
def index():
    # class Vendor(db.Model):
    #     id=db.Column(db.Integer,primary_key=True)
    #     name=db.Column(db.String(50))
    #     discount=db.Column(db.Integer)
    #     active=db.Column(db.Boolean)
    # db.create_all()
    # # v1=Vendor(id=1,name="Microsoft",discount=0,active=True) 
    # # db.session.add(v1) 
    # v2=Vendor(id=2,name="Samsung",discount=5,active=True)
    # db.session.add(v2)
    # db.session.commit()
    db.create_all()
    vendors=Vendor.query.all() 
    result=''
    for vendor in vendors: 
        # result=result+repr(vendor)+"<br>"
        result=result+str(vendor)+"<br>"
    return f"Hello<br>{result}"

if __name__=="__main__":
    app.run()