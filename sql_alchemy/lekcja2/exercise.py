from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app=Flask(__name__) 
path_database_config=r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\sql_alchemy\config_exercise.cfg"  
app.config.from_pyfile(path_database_config)
db=SQLAlchemy(app)

class Author(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    special=db.Column(db.Boolean)

@app.route("/")
def index():
    db.create_all()
    # author=Author(id=3, name='Paul Cezane', special=True )
    # db.session.add(author)
    # db.session.commit()
    return "hotel sqlalchemy"

if __name__=="__main__":
    app.run()