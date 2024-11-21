# The enpoint to handle registering and loggin in our users
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models import db, User, ValidationError


class RegisterResource(Resource):

    '''Endpoint to register a new user'''
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str, required=True,
                        help='User name is required')
    parser.add_argument('email', type=str, required=True,
                        help='Email address is reuired')
    parser.add_argument('password', type=str, required=True,
                        help='Password is required')

    def post(self):

        # Logic to handle new user registration
        data = self.parser.parse_args()

        # Checking if the email is already in use
        email = User.query.filter_by(email=data['email']).first()

        if email:
            return {'message': 'Email is already registered', 'status': 'fail'}, 422

        # Checking if username is already in use
        user_name = User.query.filter_by(user_name=data['user_name']).first()

        if user_name:
            return {'message': 'User name already taken', 'status': 'fail'}, 422

        try:

            new_user = User(**data)

            db.session.add(new_user)

            db.session.commit()

            return {'message': 'Registration successful', 'status': 'success', 'user': new_user.to_dict()}, 201

        except ValidationError as e:

            return {'message': str(e), 'status': 'fail'}, 422


class LoginResource(Resource):

    '''Class to handle the login of the user'''
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str, required=True,
                        help='Enter your valid user name')
    parser.add_argument('password', type=str, required=True,
                        help='password is required')

    def post(self):

        # Logic for user login
        data = self.parser.parse_args()

        # Checking if the user  is in the database
        user = User.query.filter_by(user_name=data['user_name']).first()

        if user:
            # We validate the user's credentials

            # Checking if the password belongs to the user
            is_password_match = user.check_password(data['password'])

            if is_password_match:
                user_dict = user.to_dict()

                # If the user is valid we give them an access token
                access_token = create_access_token(identity=user_dict['id'])

                return {
                    'message': 'Login successful',
                    'status': 'success',
                    'user': user_dict,
                    'access_token': access_token
                },201
            else:
                return {'message': 'Invalid username/password', 'status': 'fail'}, 403
        else:
            return {'message': 'Invalid username/password', 'status': 'fail'}, 403
