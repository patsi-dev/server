#The endpoint to perform CRUD operations for our payments
from flask_restful import Resource,reqparse

from models import db,Payment

class PaymentResource(Resource):

    parser =reqparse.RequestParser()
    parser.add_argument('payment_id', type=int,required=True, help='Payment Id is required')
    parser.add_argument('invoice_id', type=int,required=True, help='Invoice Id is required')
    parser.add_argument('amount', type=int,required=True, help='Amount is reuired')
    parser.add_argument('payment_date', type=int, required=True,help='Please add the date of payment')
    parser.add_argument('payment_method', type=str, required=True,help='Please include the payment method')

    def post(self):
        #Endpoint to add new payment
        data = PaymentResource.parser.parse_args()

        new_payment = Payment(**data)

        db.session.add(new_payment)

        db.session.commit()

        return {'message':'Payment added successfully','status':'success'},201
    
    def get(self,id=None):

        #Enpoint to fetch payments

        if id == None:
            payments = Payment.query.all()

            all_payments = []

            for payment in payments:
                all_payments.append(payment.to_dict())
            return payments
        else:
            payment = Payment.query.filter_by(id=id).first()

            #Validate if the payment even exists
            if payment == None:
                return {'message':'Payment not found','status':'fail'},404
            return payment.to_dict()
        
    
    def patch(self,id=None):

        #The endpoint to update the payment details
        data = self.parser.parse_args()

        payment = Payment.query.filter_by(id=id).first()

        if payment == None:
            return {'message':'Payment not found'}
        
        for key in data.keys():
            setattr(payment,key,data[key])
        
        db.session.commit()

        return {'message':'Payment updated successfully'}
    

    def delete(self,id=None):

        #Endpoint to delete payment
        payment = Payment.query.filter_by(id=id).first()

        if payment == None:
            return {'message':'Payment not found'}
        else:
            db.session.delete(payment)

            db.session.commit()

            return {'message':'Payment deleted'}
        
