import os
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager


#Importing our endpoints
from resources.home import HomeResource
from resources.vehicles import VehicleResource
from resources.payments import PaymentResource

from models import db

#Initializing our flask application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

#Connecting our app to extensions
api = Api(app)

#For Cross Origins Resources in the client side
CORS(app)

#For handling flask migrations
migrate = Migrate(app,db)

#Connecting our app to the database
db.init_app(app)

#For the jwt
jwt = JWTManager(app)

#For hashing the password
bcrpt = Bcrypt(app)


api.add_resource(HomeResource,'/')
api.add_resource(VehicleResource,'/vehicles','/vehicles/<int:id>')
api.add_resource(PaymentResource,'/payments','/payments/<int:id>')