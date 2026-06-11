from flask import Flask,render_template,flash,url_for,request,flash,g,redirect
from datetime import datetime
import os
import sys
from author import Author
from cantor_offer import CantorOffer
import sqlite3


app=Flask(__name__) 
app.config["SECRET_KEY"]="123goniszty"
path_cantor_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\cantor.db"
path_notifications_db=r"C:\Users\barte\Desktop\python projekty\flask-mobilo-udemy-main\sql_tutorial\data\notifications.db"
app_info={'db_cantor':path_cantor_db
          ,'db_notifications':path_notifications_db}

def get_db():
    if not hasattr(g,'sqlite_db'):
        connection=sqlite3.connect(app_info["db_cantor"])
        connection.row_factory=sqlite3.Row
        g.sqlite_db=connection
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def index():
    return render_template("index.html",time_now=datetime.now(),author=f"@{Author()}",active_menu='home')

@app.route("/exchange",methods=["GET","POST"])
def exchange():
    offer=CantorOffer()
    offer.load_offer()
    
    if request.method=="GET":
        
        return render_template("exchange.html",offer=offer)
    else:
        flash("LOAD OFFER")
        flash("Debug starting exchange in POST mode")
        currency='EUR'

        if 'currency' in request.form:
            currency=request.form['currency']
        
        amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']

        if currency in offer.denies_codes:
            flash(f"Selected currency: {currency} can not be accepted")
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            db=get_db()
            sql_command="insert into transactions(currency,amount,user) values(?,?,?)"
            db.execute(sql_command,[currency,amount,'admin'])
            db.commit()
            print(currency,amount)
            flash(f"Request to exchange {currency} was accepted")        
        
        
        return render_template("exchange_results.html"
                            ,active_menu='exchange'
                            ,currency=currency
                            ,amount=amount
                            ,currency_info=offer.get_by_code(currency))
@app.route("/columns_grid")
def columns_grid():
    return render_template("columns.html")
@app.route("/history")
def history():
    db=get_db()
    query="select *from transactions"
    cur=db.execute(query)
    transactions=cur.fetchall()
    return render_template("history.html",active='history',transactions=transactions)

@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction(transaction_id:int):
    db=get_db()
    sql_statement="delete from transactions where id=?"
    db.execute(sql_statement,[transaction_id])
    db.commit()

    return redirect(url_for('history'))

@app.route("/edit_transaction/<int:transaction_id>"
           ,methods=["GET","POST"])
def edit_transaction(transaction_id:int):
    
    # currency=''
    # amount=''
    # user=''
    # sql_statement="update transactions set currency=?,amount=?,user=?";
    # db.execute(sql_statement(sql_statement)
    #            ,[currency,amount,user])
    offer=CantorOffer()
    offer.load_offer()
    db=get_db()
    if request.method=="GET":
        sql_statement="select id,currency,amount from transactions where id=?;"
        transaction=db.execute(sql_statement,[transaction_id]).fetchone()
        if transaction is None:
            flash(f"Transaction id={transaction_id} no founded at database")
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html'
                                ,transaction=transaction
                                ,offer=offer
                                ,active_menu='history')
        # return render_template("exchange.html",offer=offer)
    else:
        flash("LOAD OFFER")
        flash("Debug starting exchange in POST mode")
        currency='EUR'

        if 'currency' in request.form:
            currency=request.form['currency']
        
        amount='100' 
        
        if 'amount' in request.form:
            amount=request.form['amount']

        if currency in offer.denies_codes:
            flash(f"Selected currency: {currency} can not be accepted")
        elif offer.get_by_code(currency)=='unknown':
            flash(f"Selected currency: {currency} is unknown and can not be accepted")
        else:
            sql_command="update transactions\
                set currency=?\
                ,amount=? \
                ,user=? \
                ,trans_date=?\
                where id=?"
            db.execute(sql_command,[currency,amount,'admin',datetime.utcnow(),transaction_id])
            db.commit()
            print(currency,amount)
            flash("Transaction was updated")        
        return redirect(url_for('history'))
    
if __name__=="__main__":
    app.run(port=5003)