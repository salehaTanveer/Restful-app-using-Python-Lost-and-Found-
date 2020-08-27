#import libraries
from flask import Flask, render_template

#init app
app = Flask(__name__)


#routes
@app.route('/home')
def welcome():
    return render_template('Home.html')  


#Run Server
if __name__== '__main__':
    app.run(debug=True)