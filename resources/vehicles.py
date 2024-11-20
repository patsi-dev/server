#Our endpoint for performing the CRUD operations
from flask_restful import Resource,reqparse

#Importing the db and the vehicle class
from models import db,Vehicle

class VehicleResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('image',type=str,required=True,help='Please input the car iamge')
    parser.add_argument('make',type=str,required=True,help='Please input the car make')
    parser.add_argument('model',type=str,required=True,help='Please input the car model')
    parser.add_argument('year',type=str,required=True,help='Please input the car year')
    parser.add_argument('price',type=str,required=True,help='Please input the car price')
    parser.add_argument('color',type=str,required=True,help='Please input the car color')
    parser.add_argument('mileage',type=str,required=True,help='Please input car mileage')
    parser.add_argument('description',type=str,required=True,help='Please input the car description')


    def post(self):

        #The endpoint to add new cars to the database
        data = VehicleResource.parser.parse_args()

        new_car = Vehicle(**data)

        db.session.add(new_car)

        db.session.commit()

        return {'message':'New car added','status':'success'},201
    
    def get(self,id=None):
        #The endpoint responsible for getting the cars from the database

        if id == None:
            cars = Vehicle.query.all()

            all_cars = []

            for car in cars:
                all_cars.append(car.to_dict())
            return all_cars
        else:
            #Fetching a single car
            car = Vehicle.query.filter_by(id=id).first()

            if car == None:
                return {'message':'No car found','status':'fail'},404
            return car.to_dict()
        
    def patch(self,id):
        #Enpoint to update the cars in the database
        data = self.parser.parse_args()

        #Check if the car exists before updating the car
        car = Vehicle.query.filter_by(id=id).first()

        if car == None:
            return {'message':'Car not found','status':'fail'},404
        
        for key in data.keys():
            setattr(car,key,data[key])

        db.session.commit()
        return {'message':'Car updated successfully'}
    
    def delete(self,id):
        #Enpoint to delete a car
        car = Vehicle.query.filter_by(id=id).first()

        #We must verify if the car instance even exists in our database
        if car == None:
            return {'message':'Car not found'}
        else:
            #Deleting the car instance from our database
            db.session.delete(car)
            
            #Persisting the changes to our database
            db.session.commit()
        return {'message':'Car deleted successfully'}