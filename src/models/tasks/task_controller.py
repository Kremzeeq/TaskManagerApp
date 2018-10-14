import uuid
import datetime
import  src.models.tasks.task_constants as TaskConstants
from src.common.database import Database
import src.models.tasks.task_errors as TaskErrors
import src.models.users.user_constants as UserConstants

class Task(object):

    def __init__(self, task_name, description, priority, status_boolean=False, status=None, date_created= None, date_updated=None,_id=None, user_id_task_owner=None, completed_by=None):
        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.status_boolean = status_boolean
        self.status = TaskConstants.STATUS_TEXT_CATEGORIES[0] if status is None else status
        self.date_created = datetime.datetime.utcnow() if date_created is None else date_created
        self.date_updated = datetime.datetime.utcnow() if date_updated is None else date_updated
        self._id = uuid.uuid4().hex if _id is None else _id
        self.user_id_task_owner = user_id_task_owner
        self.completed_by = completed_by

    def check_task_id_length(self):
        length_of_hex_string = 32
        if len(self._id) != length_of_hex_string:
            raise TaskErrors.InvalidTaskID("Please ensure valid task id is provided")

    def find_status_text(self,status_boolean):
        status_text_categories = TaskConstants.STATUS_TEXT_CATEGORIES
        if status_boolean:
            self.status = status_text_categories[1]
        else:
            self.status = status_text_categories[0]

    def find_status_boolean(self, status_boolean_in_form):
        if status_boolean_in_form == None:
            self.status_boolean = False
        elif len(self.completed_by) > 0 and status_boolean_in_form == "1":
            self.status_boolean = True

    def check_completed_by_empty_and_true_status_boolean(self):
        if self.status_boolean == True and (self.completed_by == None or self.completed_by == "None"
                                            or self.completed_by == ""):
            raise TaskErrors.TaskCompletedByNotSpecified("Please ensure to specify who completed the task")

    def check_completed_by_not_empty_and_false_status_boolean(self):
        if self.status_boolean == False and len(self.completed_by) > 0:
            raise TaskErrors.StatusBooleanNotUpdated("Please tick the status for the task if it was completed")

    def check_status_boolean(self):
        if self.status_boolean == True or self.status_boolean == False:
            return True
        else:
            raise TaskErrors.InvalidTaskStatusBoolean("Please ensure a boolean value is provided for status_boolean")

    def check_priority_category(self):
        priority_categories = TaskConstants.PRIORITY_CATEGORIES
        if self.priority in priority_categories:
            return True
        else:
            raise TaskErrors.InvalidTaskPriorityCategory("Please ensure correct priority category is specified")

    @classmethod
    def check_user_id_task_owner_is_not_valid(cls, user_id_task_owner):
        user_data = Database.find_one(UserConstants.COLLECTION, {"_id": user_id_task_owner})
        if user_data is None:
            raise TaskErrors.TaskOwnerIdIsNoLongerValid(
                "The task owner user account for the task no longer exists. Contact administrator")

    @classmethod
    def find_task_docs_in_db(cls):
        return [cls(**elem) for elem in Database.find(TaskConstants.COLLECTION, {})]

    @classmethod
    def find_by_id(cls, task_id):
        return cls(**Database.find_one(TaskConstants.COLLECTION,{'_id':task_id}))

    def save_to_db(self):
        Database.update(TaskConstants.COLLECTION, {"_id": self._id}, self.json())

    def delete(self):
        Database.remove(TaskConstants.COLLECTION, {"_id": self._id})

    @staticmethod
    def delete_many_by_task_name(task_name):
        Database.delete_many(UserConstants.COLLECTION, {"task_name": task_name})

    def json(self):
        return {
            "_id": self._id,
            "task_name": self.task_name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "status_boolean": self.status_boolean,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "user_id_task_owner": self.user_id_task_owner,
            "completed_by":self.completed_by
        }
