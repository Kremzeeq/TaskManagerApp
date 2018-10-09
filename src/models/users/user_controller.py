from src.common.database import Database
import src.models.users.user_constants as UserConstants
import src.models.users.user_errors as UserErrors
import uuid
import requests
from src.common.utils import Utils

class User(object):
    def __init__(self, email, password= None, _id = None, active=False):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def check_email_valid(self):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email":self.email})
        if user_data is not None:
            raise UserErrors.UserAccountAlreadyExists("The email you used to register already exists")
        elif Utils.email_is_valid(self.email) == False:
            raise UserErrors.InvalidEmailError("Please ensure email is provided in the right format")
        else:
            return True

    def send_auth_code_email(self):
        auth_code = Utils.generate_auth_code()
        self.password = Utils.hash_password(auth_code)
        self.insert_user_in_db()
        return requests.post(UserConstants.URL,
                             auth=("api", UserConstants.API_KEY),
                             data={
                                    "from": UserConstants.FROM,
                                    "to": self.email,
                                    "subject": "Task Manager App",
                                    "text": 'Welcome to Task Manager App! \n\n'
                                     'Task Manager helps you keep track of tasks '
                                     'Please click here visit ({}) and enter your authorisation code on the registration page: \n\n'
                                     '{}'.format(UserConstants.AUTH_URL, auth_code)
                                    })

    def insert_user_in_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def update_user_in_db(self):
        Database.update(UserConstants.COLLECTION,{"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "active": self.active,
    }

    @staticmethod
    def authenticate_user(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserDoesNotExistError("Your user account does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectAuthCodeCode("Your authentication code was incorrect")
        return True

    def find_user_by_email(email):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        return user_data['_id']

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.PoorPasswordError("Please ensure to enter a secure password")
        user_data = User(email, password, _id=user_data['_id'])
        user_data.active = True
        user_data.password = Utils.hash_password(password)
        user_data.update_user_in_db()
        return True

    @staticmethod
    def validate_user_login(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserDoesNotExistError("Your user account does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was incorrect")
        return True
