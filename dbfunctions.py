from flask import Flask, request, jsonify , render_template , flash , session , redirect , url_for , Blueprint , request
from flask_bootstrap import Bootstrap
from model import RegForm , LoginForm , SearchForm , InsertForm
from functools import wraps
from sqlalchemy  import or_
from dbmodels import *


app.secret_key = "secretkey"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:                              #check if session exists
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')                   #else redirect to login
            return redirect(url_for('login'))
    return wrap


#forms and requests


Bootstrap(app)

#redirect default route to login
@app.route('/')
def redirect_url():
    return redirect(url_for('login'))


#register route
@app.route('/register/', methods=['GET', 'POST'])
def registration():
    form = RegForm(request.form)                                                    #request wt-form names RegForm
    if request.method == 'POST' and form.validate_on_submit():                      #validate form using validators defined in model.py
        existing_user = User.query.filter_by(username=form.username.data).first()   #check for existing username
        if existing_user:                                                           #if username ecxists, raise error else register and start session
            return 'user exists'
        else:
            new_user = User(form.username.data, form.password.data)

            db.session.add(new_user)
            db.session.commit()
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('register.html', form=form)


#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)                                                  #request Wt-from named loginForm
    if request.method == 'POST' and form.validate_on_submit():                      #validate form using validators defined in model.py
        existing_user = User.query.filter_by(username=form.username.data).first()   #get username from db
        if existing_user:                                                           #if exists check password else raise warning
            if existing_user.password == form.password.data:
                session['logged_in'] = True
                return redirect(url_for('home'))
            return 'Invalid Password.'
        else:
            return 'Invalid Username.'

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)                                                  #end session
    flash('You are logged out!')
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('Home.html')                                             #render home page
 

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    flash("Search results displayed based on name or location")                 #flash messages to search.html page
    search_results=[]
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search_query = "%{0}%".format(search_value)
        if search_value == "":
            search_results = Product.query.filter(or_(Product.name.like(search_query),Product.location.like(search_query))).all()
            return render_template('search.html', search_results=search_results)
        else:
            search_results = Product.query.filter(Product.name.like(search_query)).all()
            return render_template('search.html',  search_results=search_results)
        flash(search_results)
    return render_template('search.html', search_results=search_results)
 

 # Get Single Product
@app.route('/search/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return redirect(url_for('update_product',id=product.id))

 
# Update a Product
@app.route('/search/<int:id>/update', methods=['POST','GET'])
def update_product(id):

  product = Product.query.get(id)
  form = InsertForm(request.form)
  if form.validate_on_submit():
      product.name=form.name.data
      product.description= form.description.data
      product.location= form.location.data
      product.Date= form.Date.data
      product.Status= form.status.data
      db.session.commit()
      return redirect(url_for('search'))

  form.name.data = product.name
  form.description.data = product.description
  form.location.data = product.location
  form.Date= product.Date
  form.status.data = product.Status

  return render_template('/insert.html', form=form)

# Delete a Product
@app.route('/search/delete/<int:id>', methods=['DELETE','GET'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted: " + product.name)
    return render_template('/search.html',search_results=Product.query.all())


#insert a new product
@app.route('/insert', methods=['GET', 'POST'])
@login_required
def add_item():
    insert_data = InsertForm(request.form)
    if request.method == 'POST' and insert_data.validate_on_submit():
        new_product = Product(insert_data.name.data, insert_data.description.data, insert_data.location.data, insert_data.Date.data, insert_data.status.data)

        db.session.add(new_product)
        db.session.commit()
        flash('Product insert complete. Product name: ' + insert_data.name.data )
    
    return render_template('insert.html',form=insert_data)


#Run Server
if __name__== '__main__':
    app.run(debug=True)