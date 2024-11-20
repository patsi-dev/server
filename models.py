#Our database schema
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
    contact_details = db.Column(db.String(60),nullable=False)

class Customer(db.Model,SerializerMixin):

    #Table to keep to store the customers information
    __tablename__ = 'customers'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(60),nullable=False,unique=True)
    email = db.Column(db.String(60),nullable=False,unique=True)


class Payment(db.Model,SerializerMixin):

    #table to keep track of payments
    __tablename__ = 'payments'

    id = db.Column(db.Integer,primary_key=True)
    payment_id = db.Column(db.Integer,nullable=False,unique=True)
    invoice_id = db.Column(db.Integer,nullable=False,unique=True)
    payment_date = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    payment_method = db.Column(db.String(60),nullable=False)



