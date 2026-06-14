from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app=Flask(__name__)   
app.config.from_pyfile('config_exercise.cfg')
db=SQLAlchemy(app)

class Author(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    special=db.Column(db.Boolean)

@app.route("/")
def index():
    db.create_all()
    return "hotel sqlalchemy"

if __name__=="__main__":
    app.run()