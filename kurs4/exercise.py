from flask import Flask,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello from main route</h1>"

@app.route('/cook/<string:receipt>/<int:step>') 
def cook(receipt, step): 
    font_size=20
    if 'font-size' in request.args:
        font_size=request.args['font-size']
    body = f'''<h1 style="font-size:{font_size}">\
        In the receipt {receipt} \
        you are on step {step}</H1>''' 
    return  body 

@app.route("/opinions_form")
def opinions_form():
    body='''
    <form id="opinions_form" action="/opinions_form_process" method="POST">
    <label for="note">What is your note for the receipt?</label>
    <select id="note" name="note">
        <option value="It was good">It was good</option>
        <option value="It was not good">It was not good</option>
        <option value="It was very bad">It was very bad</option>
        <option value="It was tasty">It was tasty</option>
    </select><br>
    <label for="comments">Write down your comments</label>
    <input type="text" id="comment" name="comment" value="Write your comments"><br>
    <label for="check_opinion">Would you like cook it for your family?
    <input type="checkbox" id="check_opinion" name="check_opinion"><br>
    </label>
    <input type="submit" value="Share my feedback">
    </form>
    '''
    return body

@app.route("/opinions_form_process"
        ,methods=["POST"])
def opinions_form_process():
    note=""
    comment=""
    check_opinion=""

    if 'note' in request.form:
        note=request.form['note']
    if 'comment' in request.form:
        comment=request.form['comment']
    if 'check_opinion' in request.form:
        check_opinion=request.form['check_opinion']
    
    if check_opinion=="on":
        check_opinion="YES"
    else:
        check_opinion="NO"

    body=f"<h1>Your opinions</h1>\
        <p>note: {note}</p> <p>comment: {comment}</p>\
            <p>Would you like cook it for your family?{check_opinion}</p>"
    return body
if __name__=="__main__":
    app.run()