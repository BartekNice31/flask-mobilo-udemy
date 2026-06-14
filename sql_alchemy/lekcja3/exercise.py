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
    
    def __repr__(self):
        return f"Author: {self.id} {self.name} {self.special}"
    def __str__(self):
        return f"Author: {self.id} {self.name} {self.special}"
@app.route("/")
def index():
    db.create_all()
    # author4=Author(id=4, name='Paul Cezane', special=False )
    # author5=Author(id=5, name='Andy Warhol')
    # author6=Author(id=6, name='Frida Kahlo')
    # db.session.add(author4)
    # db.session.add(author5)
    # db.session.add(author6)
    # db.session.commit()
    authors=Author.query.all()
    result=''
    for author in authors:
        result=result+str(author)+"<br>"
    return f"hotel sqlalchemy<br>{result}"

if __name__=="__main__":
    app.run()