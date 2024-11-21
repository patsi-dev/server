# Endpoint for performing the CRUD  operations on the customers
from flask_restful import Resource, reqparse

from models import db, Customer,ValidationError


class CustomerResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='Name of the customer is required')
    parser.add_argument('address', type=str, required=True,
                        help='Address of the customer is required')
    parser.add_argument('email', type=str, required=True,
                        help='Email address of the customer is required')
    parser.add_argument('phone', type=str, required=True,
                        help='Enter the phone number of the customer')

    def post(self):

        # Endpoint to allow adding new data of the customer to the database

        data = CustomerResource.parser.parse_args()

        # Checking if the phone already exists in our database
        phone = Customer.query.filter_by(phone=data['phone']).first()
        if phone:
            return {'message': 'Phone number already in use', 'status': 'fail'}, 422

        # Checking if the email already exists in our database
        email = Customer.query.filter_by(email=data['email']).first()
        if email:
            return {'message': 'Email already exists', 'status': 'fail'}, 422

        try:
            new_customer = Customer(**data)

            db.session.add(new_customer)

            db.session.commit()

            return {'message': 'Customer details added '}
        #Handling exception error to make sure correct details are passed
        except ValidationError as e:
            return {'message':str(e),'status':'fail'},422

    def get(self, id=None):

        # Logic for fetching customers

        # If no id is given fetch all the customers in the database
        if id == None:

            customers = Customer.query.all()

            all_customers = []

            for customer in customers:
                all_customers.append(customer.to_dict())
            return all_customers
        else:
            customer = Customer.query.filter_by(id=id).first()

            # Checking if the customer with the passed id even exists
            if customer == None:
                return {'message': 'Customer not found', 'status': 'fail'}, 404
            return customer.to_dict()

    def patch(self, id):

        data = self.parser.parse_args()

        customer = Customer.query.filter_by(id=id).first()

        if customer == None:
            return {'message': 'Customer not found'}, 404

        for key in data.keys():
            setattr(customer, key, data[key])

        return {'message': 'Customer information updated'}

    def delete(self, id=None):

        customer = Customer.query.filter_by(id=id).first()
        if customer == None:
            return {'message': 'Customer not found'}, 404

        else:

            db.session.delete(customer)

            db.session.commit()

            return {'message': 'Customer deleted successfully'}
