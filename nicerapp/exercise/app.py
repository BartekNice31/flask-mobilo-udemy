from flask import Flask,render_template,url_for,flash
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
load_dotenv(r"C:\Users\Bartłomiej\Desktop\python\flask-mobilo-udemy-main\.flaskenv")

app=Flask(__name__)
bootstrap=Bootstrap(app=app)

@app.route("/")
def route():
    return render_template("index.html")

if __name__=="__main__":
    app.run()