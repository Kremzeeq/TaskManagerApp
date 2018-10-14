from src.models.tasks.task_controller import Task
import src.models.tasks.task_errors as TaskErrors
from src.models.users.user_controller import User
from src.common.database import Database
import pytest

@pytest.fixture(scope="module") #https://docs.pytest.org/en/latest/fixture.html
# fixture structure allows to share set up and tear down for multiple tests
def init_db():
    Database.initialize()

def remove_test_data(init_db):
    new_user = User("test.test@test.com")
    new_user.delete_many_by_email(new_user.email)
    new_task = Task("Test task name", "Test Description", "High")
    new_task.delete_many_by_task_name(new_task.task_name)
    new_task.delete()

def test_create_new_default_task(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    assert new_task.task_name == "Test task name"
    assert new_task.description == "Test Description"
    assert new_task.priority == "High"

def test_create_new_task_with_poor_id(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    new_task._id = str(123)
    with pytest.raises(TaskErrors.InvalidTaskID):
        new_task.check_task_id_length()

def test_create_new_task_with_incorrect_priority_category(init_db):
    new_task = Task("Test task name", "Test Description", priority="Amber")
    with pytest.raises(TaskErrors.InvalidTaskPriorityCategory):
        new_task.check_priority_category()

def test_create_new_task_with_incorrect_boolean(init_db):
    new_task = Task("Test task name", "Test Description", "High","True")
    with pytest.raises(TaskErrors.InvalidTaskStatusBoolean):
        new_task.check_status_boolean()

def test_create_new_task_with_dates(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    assert new_task.date_created != None
    assert new_task.date_updated != None

def test_create_new_task_with_undone_status(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    assert new_task.status == "Undone"

def test_update_new_task_with_completed_by_empty_and_true_status_boolean(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    new_task.status_boolean = True
    new_task.completed_by = ""
    with pytest.raises(TaskErrors.TaskCompletedByNotSpecified):
        new_task.check_completed_by_empty_and_true_status_boolean()

def test_update_new_task_with_completed_by_not_empty_and_false_status_boolean(init_db):
    new_task = Task("Test task name", "Test Description", "High")
    new_task.status_boolean = False
    new_task.completed_by = "hello"
    with pytest.raises(TaskErrors.StatusBooleanNotUpdated):
        new_task.check_completed_by_not_empty_and_false_status_boolean()

def test_check_user_id_task_owner_is_not_valid(init_db):
    new_user = User("test.test@test.com")
    new_user.insert_user_in_db()
    email = new_user.email
    user_data = new_user.find_user_data_by_email(email)
    new_user_id = user_data['_id']
    new_task = Task("Test task name", "Test Description", "High",user_id_task_owner=new_user_id)
    new_task.save_to_db()
    new_user.delete_by_email()
    with pytest.raises(TaskErrors.TaskOwnerIdIsNoLongerValid):
        new_task.check_user_id_task_owner_is_not_valid(new_user_id)
    new_task.delete()