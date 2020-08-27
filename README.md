# Restful-app-using-Python--Lost-and-Found-
 
 To run the application
 
 1. Clone the repository on your system.
 2. Run the following commands on terminal inside the root folder
    
    $ pip install pipenv

    $ pipenv shell

    $ pip install -r requirements.txt

    $ python

    #inside python run the following

    from app import db

    db.create_all()

    exit()
        
    $ python app.py

# Database
on mysql localhost create a database "LostandFound"
then run the following commands to generate tables

    $ python
    >>> from app import db
    >>> db.create_all()
    >>> exit()


