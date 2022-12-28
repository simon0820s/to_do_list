from flask import Flask, flash,make_response,redirect,request,render_template,session,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired
import unittest
app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']='SUPER SECRETO'

todos=['Comer','Dormir','Programar']

class LoginForm(FlaskForm):
    name=StringField('User name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Send')

@app.cli.command()
def test():
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.errorhandler(500)
def didnt_completed(error):
    return render_template('500.html',error=error)


@app.route('/')
def index():
    user_ip=request.remote_addr
    response=make_response(redirect('/hello'))
    session['user_ip']=user_ip
    return response

@app.route('/hello',methods=['GET','POST'])
def hello():
    user_ip=session.get('user_ip')
    login_form=LoginForm()
    name=session.get('name')
    context={
        'user_ip':user_ip,
        'todos':todos,
        'login_form':login_form,
        'name':name
    }
    
    if login_form.validate_on_submit():
        name=login_form.name.data
        session['name']=name
        flash('User name registered!!')
        return redirect(url_for('index'))


    return render_template('hello.html',**context)