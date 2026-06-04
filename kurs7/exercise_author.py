from flask import Flask, url_for, redirect 
app = Flask(__name__) 
@app.route('/not_implemented/<message>') 
def not_implemented(message): 
    return '<h1 style="color:red">{}</h1>'.format(message) 
@app.route('/new_receipt') 
def new_receipt(): 
    return redirect(url_for('not_implemented', message="Function new_receipt is not ready yet")) 
@app.route('/delete_receipt/<name>') 
def delete_receipt(name): 
    return redirect(url_for('not_implemented', message="Function new_receipt is not ready yet"))