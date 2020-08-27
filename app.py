#import libraries
from flask import Flask, render_template

#init app
app = Flask(__name__)



#Run Server
if __name__== '__main__':
    app.run(debug=True)