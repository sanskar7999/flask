
from flask import Flask , render_template, request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail                                             


with open("app.json" , 'r') as c:
    params = json.load(c)['params']
local_server = True


app = Flask(__name__)
app.config.update(

    MAIL_SERVER = "smtp.gmail.com" ,
    MAIL_PORT = '465',
    MAIL_URL_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_password']
)
mail = Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)
class Marja(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    mag = db.Column(db.String(120), unique=True, nullable=False)
    Date = db.Column(db.String(120), unique=True, nullable=True)
    
@app.route('/')
def home():
    return render_template("index.html" , params = params)

@app.route('/post')
def postt():
    return render_template('post.html', params = params)

@app.route('/about')
def about():
    return render_template('about.html' ,params = params)

@app.route('/contact'  , methods = ['GET'  , 'POST'])
def contact():
    if (request.method=='POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        mag = request.form.get('mag')
        email = request.form.get('email')
        print(name)
        print(phone)
        print(mag)
        print(email)
        print()
    

        entry = Marja(name = name, phone = phone ,Date = datetime.now() ,mag = mag , email = email)

        db.session.add(entry)
        db.session.commit()
        mail.send_message('NEW MESSAG FROM' )
    return render_template('contact.html', params = params)


app.run(debug = True)