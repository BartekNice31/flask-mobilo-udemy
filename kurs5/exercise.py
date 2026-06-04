from flask import Flask,request
from dotenv import load_dotenv
import os
import sys
load_dotenv(r".flaskenv")

app=Flask(__name__)
 
app=Flask(__name__)
 
@app.route("/")
def route():
    return "<h1>Hello from main route</h1>"

@app.route('/rate_receipt',methods=["GET","POST"]) 
def rate_receipt(): 
    if request.method=='GET':
        body = ''' 
            <form id="rating" action="/rate_receipt_save" method="POST"> 
                <label for=note>What is your note for the receipt?</label><br> 
                <select id="nore" name="note"> 
                    <option value="5">It is great!</option> 
                    <option value="4">It is very good</option> 
                    <option value="3" selected>It is just good</option> 
                    <option value="2">It was poor</option> 
                    <option value="1">It was horrible!</option> 
                </select><br> 
    
                <label for=comment>Write down your comments:</label><br> 
                <textarea id="comment" name="comment" rows="3" cols="50"> 
                </textarea><br> 
    
                <label for="decision">Would you cook it for your family?</label><br> 
                <input type="checkbox" id="decision" name="decision"><br> 
    
                <input type="submit" value="Share my feedback"> 
            </form> 
        ''' 
        return body 
    else:
        note=3
        if 'note' in request.form: 
            note = request.form['note'] 
        comment='' 
        if 'comment' in request.form: 
            comment = request.form['comment'] 
        decision = False 
        if 'decision' in request.form: 
            decision = True 
 
        body = f'''Your rating was: {note}<br> 
                    Your comment was: {comment}<br> 
                    Your decision was {decision} 
        ''' 
        return body 
 
 
@app.route('/rate_receipt_save', methods=['POST']) 
def rate_receipt_save(): 
 
    note = 3 
    if 'note' in request.form: 
        note = request.form['note'] 
    comment='' 
    if 'comment' in request.form: 
        comment = request.form['comment'] 
    decision = False 
    if 'decision' in request.form: 
        decision = True 
 
    message = f'''Your rating was: {note}<br> 
                  Your comment was: {comment}<br> 
                  Your decision was {decision} 
    ''' 
    return message 

if __name__=="__main__":
    app.run()