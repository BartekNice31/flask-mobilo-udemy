from flask import Flask
from datetime import datetime
print(__name__)
app=Flask(__name__)
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Bartłomiej\Desktop\python\flask mobilo udemy\kurs1\.flaskenv")

@app.route("/")
def index():
    return "<h1>HELLO WORLD!!</h1>"

@app.route("/about")
def about():
    a=10
    b=0
    return "<h1>We are programmers</h1>{}".format(a/b)

@app.route("/zero_divission_error")
def zero_divission_error():
    a=10
    b=5
    return "<h1>Zero divission error : {}</h1>".format(a/b)

@app.route("/time_of_creating_page")
def time_creating_page():
    time_now = datetime.now().strftime('%H:%M:%S')
    return "<h1>Czas tworzenia strony: {} </h1>".format(time_now)

@app.route("/links")
def get_links():
    return "<a href={}>UDEMY</a> <a href={}>GOOGLE</a>".format("https://www.udemy.com/"
                                                            ,"https://www.google.com/")
    # return "<h1>{}</h1><h2>{}</h2>".format("https://www.udemy.com/"
    #                                     ,"www.google.com")
@app.route("/links_v2")
def links_v2():
    body = '''<a href="http://www.google.com" target="_blank">Google</a> <br /> <a href="http://www.bing.com" target="_blank">Default search engine to find Google</a>'''
    return body

@app.route("/cantor/<currency>/<amount>")
def cantor():
    pass

if __name__=="__main__":
    app.run()