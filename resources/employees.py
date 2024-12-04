# Endpoint for performing CRUD operations on the employees on our database
from flask_restful import Resource, reqparse

from models import db, Employee


class EmployeeResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='Name of the employee is required')
    parser.add_argument('position', type=str, required=True,
                        help='Position of the employee is required')
    parser.add_argument('contacts', type=str, required=True,
                        help='Contact details of the employee is required')
    parser.add_argument('id_no', type=str, required=True,
                        help='National ID number required')

    def post(self):
        '''Endpoint for adding new employees to the db'''

        data = EmployeeResource.parser.parse_args()

        # We need to verify that the contact details of the employee already exists
        contacts = Employee.query.filter_by(
            contacts=data['contacts']).first()

        if contacts:
            return {'message': 'Contact details in use', 'status': 'fail'}, 422

        # Verifying if the id number is already in use
        id_number = Employee.query.filter_by(id_no=data['id_no']).first()
        if id_number:
            return {'message': 'Id number already exists', 'status': 'faail'}, 422
        new_employee = Employee(**data)

        db.session.add(new_employee)

        db.session.commit()

        return {'message': 'New employee added'}

    def get(self, id=None):

        if id == None:
            employees = Employee.query.all()

            all_employees = []

            for employee in employees:
                all_employees.append(employee.to_dict())

            return all_employees

        else:
            employee = Employee.query.filter_by(id=id).first()

            if employee == None:
                return {'message': 'Employee not found'}, 404
            return employee.to_dict()

    def patch(self, id):
        '''Endpoint to update the employees information in the database'''

        data = self.parser.parse_args()

        employee_details = Employee.query.filter_by(id=id).first()

        if employee_details == None:
            return {'message': 'Employee not found'}, 404

        for key in data.keys():
            setattr(employee_details, key, data[key])

        db.session.commit()

        return {'message': 'Employee details updated successfully'}

    def delete(self, id):
        '''Logic for deleting the employees'''

        if id == None:
            return {'message': 'Employee not found'}
        else:
            employee = Employee.query.filter_by(id=id).first()
           
            db.session.delete(employee)

            db.session.commit()
            # print(employee.name)
            return {'message': f'{employee.name} deleted successully'}
