from flask import Flask,redirect,render_template,g,Request,Response
from wtforms import IntegerField,BooleanField,FloatField,StringField,SelectField
from flask_wtf import FlaskForm

class TrainInfo(FlaskForm):
    Train_number=StringField('Train Number')
    Is_delayed=BooleanField('Train Delayed')
    Delay_minutes=IntegerField('Delay minutes')
    Delay_reason=SelectField('Delay reason'
                            ,choices=['None','Weather','Failure','Other'])

app=Flask(__name__)
app.config['SECRET_KEY']='A4c0om^^pl1i1te3d'

@app.route("/",methods=["GET","POST"])
def index():
    form=TrainInfo()
    if form.validate_on_submit():
        return f"""<h1>HELLO</h1>
                <ul>
                    <li>{form.Train_number.label}:{form.Train_number.data}</li>
                    <li>{form.Is_delayed.label}:{form.Is_delayed.data}</li>
                    <li>{form.Delay_minutes.label}:{form.Delay_minutes.data}</li>
                    <li>{form.Delay_reason.label}:{form.Delay_reason.data}</li>
                </ul>
            """
    return render_template('index.html',form=form)

if __name__=='__main__':
    app.run(port=5005)