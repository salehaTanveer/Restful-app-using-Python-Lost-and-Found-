from dbconnect import *





#MODEL
class Product(db.Model):
    __searchable__= ['name','description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(200))
    location = db.Column(db.String(200))
    Date = db.Column(db.String(200))
    Status = db.Column(db.String(10))



    def __init__(self,name,description,location,Date,status):
        self.name = name
        self.description = description
        self.location = location
        self.Date = Date
        self.Status = status

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(200))

    def __init__(self,username,password):
        self.username = username
        self.password = password


#model schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description','location', 'Date', 'Status')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username', 'password')

#init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Run Server
if __name__== '__main__':
    app.run(debug=True)