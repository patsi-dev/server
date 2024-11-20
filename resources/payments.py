# The endpoint to perform CRUD operations for our payments
from flask_restful import Resource, reqparse
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from models import db, Payment


class PaymentResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('payment_id', type=int, required=True,
                        help='Payment Id is required')
    parser.add_argument('invoice_id', type=int, required=True,
                        help='Invoice Id is required')
    parser.add_argument('amount', type=int, required=True,
                        help='Amount is reuired')
    parser.add_argument('payment_date', type=str, required=True,
                        help='Please add the date of payment')
    parser.add_argument('payment_method', type=str, required=True,
                        help='Please include the payment method')

    def post(self):
        # Endpoint to add new payment
        data = PaymentResource.parser.parse_args()

        try:
            payment_date = datetime.strptime(
                data['payment_date'], '%Y-%m-%dT%H:%M:%S')

            new_payment = Payment(payment_id=data['payment_id'],
                                  invoice_id=data['invoice_id'],
                                  payment_date=payment_date,
                                  amount=data['amount'],
                                  payment_method=data['payment_method'])

            db.session.add(new_payment)

            db.session.commit()

            return {'message': 'Payment added successfully', 'status': 'success'}, 201
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def get(self, id=None):

        # Enpoint to fetch payments

        if id == None:
            payments = Payment.query.all()

            all_payments = []

            for payment in payments:
                all_payments.append(payment.to_dict())
            return all_payments
        else:
            payment = Payment.query.filter_by(id=id).first()

            # Validate if the payment even exists
            if payment == None:
                return {'message': 'Payment not found', 'status': 'fail'}, 404
            return payment.to_dict()

    def patch(self, id=None):

        # The endpoint to update the payment details
        data = self.parser.parse_args()

        payment = Payment.query.filter_by(id=id).first()

        if payment == None:
            return {'message': 'Payment not found'}

        else:
            payment_date = datetime.strptime(
                data['payment_date'], '%Y-%m-%dT%H:%M:%S')

            
            payment.payment_id=data['payment_id']
            payment.invoice_id=data['invoice_id']
            payment.payment_date=payment_date
            payment.amount=data['amount']
            payment.payment_method=data['payment_method']
            
            db.session.commit()

            return {'message': 'Payment updated successfully'}

    def delete(self, id=None):

        # Endpoint to delete payment
        payment = Payment.query.filter_by(id=id).first()

        if payment == None:
            return {'message': 'Payment not found'}
        else:
            db.session.delete(payment)

            db.session.commit()

            return {'message': 'Payment deleted'}
