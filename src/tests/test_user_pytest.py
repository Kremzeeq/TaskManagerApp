from src.common.database import Database
from src.models.users.user_controller import User
import src.models.users.user_errors as UserErrors
from src.common.utils import Utils
import pytest

@pytest.fixture(scope="module") #https://docs.pytest.org/en/latest/fixture.html
# fixture structure allows to share set up and tear down for multiple tests

def init_db():
    Database.initialize()

def remove_test_data(init_db):
    new_user = User("test.test@test.com")
    new_user.delete_many_by_email(new_user.email)

def test_create_new_default_user(init_db):
    new_user = User("test.test@test.com")
    assert new_user.email == "test.test@test.com"

def test_create_new_user_with_email_already_in_db(init_db):
    new_user = User("test.test@test.com")
    new_user.insert_user_in_db()
    email = new_user.email
    user_data = new_user.find_user_data_by_email(email)
    with pytest.raises(UserErrors.UserAccountAlreadyExists):
        new_user.check_user_data_is_not_none(user_data)
    new_user.delete_by_email()

def test_login_with_no_email_in_db(init_db):
    new_user = User("test.test@test.com")
    email = new_user.email
    user_data = new_user.find_user_data_by_email(email)
    with pytest.raises(UserErrors.UserDoesNotExistError):
        new_user.check_user_data_is_none(user_data)

def test_check_poor_email_format(init_db):
    new_user = User("test.com")
    with pytest.raises(UserErrors.InvalidEmailError):
        new_user.check_email_format_valid()

def test_check_poor_password(init_db):
    new_user = User("test.test@test.com",)
    auth_code = Utils.generate_auth_code()
    new_user.password = Utils.hash_password(auth_code)
    with pytest.raises(UserErrors.PoorPasswordError):
        new_user.check_registration_password_same_as_auth_code(auth_code,new_user.password)
    new_user.delete_by_email()
