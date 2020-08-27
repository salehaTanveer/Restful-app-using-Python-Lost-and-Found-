#import libraries
from flask import Flask, render_template
from dbmodels import *

#init app
app = Flask(__name__)


#routes
@app.route('/home')
def home():
    return render_template('Home.html')  


@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/insert')
def insert():
    return render_template('insert.html') 

@app.route('/search')
def search():
    return render_template('search.html') 


#Run Server
if __name__== '__main__':
    app.run(debug=True)