# -- coding: UTF-8 --

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# 配置MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# 初始化MySQL
mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html',articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html',id = id)

# 用户注册
class RegisterForm(Form):
    # RegisterForm  http://wtforms.readthedocs.io/en/latest/forms.html#the-form-class
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Flask-MySQLdb API http://flask-mysqldb.readthedocs.io/en/latest/
        cur = mysql.connection.cursor()

        # 查询
        cur.execute('INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)', (name, email, username, password))

        # 提交
        mysql.connection.commit()

        # 关闭
        cur.close()

        flash('You are now registered and can log in.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # 获取字段信息
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        # 获取用户名
        result = cur.execute('SELECT * FROM users WHERE username = %s', [username])

        if result > 0:
            # 获取存储信息
            data = cur.fetchone()
            password = data['password']

            # 对比输入密码
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
            else:
                app.logger.info('PASSWORD NOT MATCHED')
        else:
            app.logger.info('NO USER')
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key='123456'
    app.run()