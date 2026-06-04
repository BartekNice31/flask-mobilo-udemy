from flask import Flask,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r"C:\Users\barte\Desktop\python projekty\flask mobilo udemy\.flaskenv")

app=Flask(__name__)

@app.route("/")
def route(): 
    color='black'
    if 'color' in request.args:
        color=request.args['color']
    style='normal'
    if 'style' in request.args:
        style=request.args['style'] 

    print('-'*30)
    print("Received arguments:")
    for arg in request.args:
        print(f"key:{arg}")
        print(f"value={request.args[arg]}")
        print('-'*30)

    return f'<h1 style="color: {color};font-style:{style};">\
        Hello world</h1>'

@app.route("/index")
def index():
    print(request.query_string) 
    print('-'*30)
    color='black'
    if 'color' in request.args:
        color=request.args['color']
    style='normal'
    if 'style' in request.args:
        style=request.args['style'] 
    print(color)
    print(style)

    print('-'*30)
    print("Received arguments:")
    for arg in request.args:
        print(arg)

    return f'<h1 style="color: {color};font-style:{style};">\
        Hello world</h1>'
@app.route("/colors_styles")
def colors_styles():
    print(request.query_string)
    print('-'*30)
    color='black'
    if 'color' in request.args:
        color=request.args['color']
    style='normal'
    if 'style' in request.args:
        style=request.args['style']
    if color=='black' and style=='normal':
        return f"<h1>No changes</h1>"
    if color!='black' and style=='normal':
        return f"<h1>Changes in color</h1>"
    if color!='black' and style!='normal':
        return f"<h1>Changes in color and in style</h1>"
    if color=='black' and style!='normal':
        return f"<h1>Changes in style</h1>"
if __name__=="__main__":
    app.run()