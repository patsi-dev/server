#Our database schema
import re
from sqlalchemy.orm import validates
from flask_bcrpyt import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

convention = {
      "ix": 'ix_%(column_0_label)s',
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s"
              }

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class ValidationError(Exception):
    
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)
        
        
class User(db.Model,SerializerMixin):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(60),nullable=False)
    email = db.Column(db.String(60),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    
    #Validating the email of the user before we save it to the database
    @validates('email')
    def validate_email(self,key,email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Please enter a valid email address.')
        return email
    
     # Function to check  the strength of the password
    @validates('password')
    def password_strength(self, key, password):
        # Regular expressions for uppercase, lowercase, and numeric characters
        if len(password) < 8:
            raise ValidationError(
                'Password is too short, it should be at least 8 characters.')
        if not re.search('[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter.')
        if not re.search('[a-z]', password):
            raise ValidationError(
                'Password must contain at least one lowercase letter.')
        if not re.search('[0-9]', password):
            raise ValidationError('Password must contain at least one number.')

        # Hashing the password before doing the validation
        return generate_password_hash(password).decode('utf-8')

    # Function to check password
    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

class Vehicle(db.Model,SerializerMixin):
    
    #Table to store the vehicles in our database in our database
    __tablename__ = 'vehicles'

    id  = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(256),nullable=False)
    model = db.Column(db.String(60),nullable=False)
    make = db.Column(db.String(60),nullable=False)
    year = db.Column(db.String(60),nullable=False)
    price =db.Column(db.String,nullable=False)
    color = db.Column(db.Text,nullable=False)
    mileage = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(256),nullable=False)

class Employee(db.Model,SerializerMixin):

    #Table to keep store the employees data
    __tablename__ = 'employees'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    position = db.Column(db.String(60),nullable=False)
    contact_details = db.Column(db.String(60),nullable=False,unique=True)

class Customer(db.Model,SerializerMixin):

    #Table to keep to store the customers information
    __tablename__ = 'customers'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(15),nullable=False,unique=True)
    email = db.Column(db.String(80),nullable=False,unique=True)

    #We need to validate the email 
    @validates('email')
    def validate_email(self,key,email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Please enter a valid email address.')
        return email
    
    #Validating the phone number too
    @validates('phone')
    def validate_phone(self, key, phone_number):
        if not re.match(r"^0[0-9]{9}$", phone_number):
            raise ValidationError('Phone number must be a 10-digit number starting with 0')
        return phone_number

class Payment(db.Model,SerializerMixin):

    #table to keep track of payments
    __tablename__ = 'payments'

    id = db.Column(db.Integer,primary_key=True)
    payment_id = db.Column(db.Integer,nullable=False,unique=True)
    invoice_id = db.Column(db.Integer,nullable=False,unique=True)
    payment_date = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    payment_method = db.Column(db.String(60),nullable=False)



