import uuid
import datetime
from src.models.tasks import task_constants
from src.common.database import Database

class Task(object):

    def __init__(self, task_name, description, priority, status_boolean=False, status="Undone", date_created= None, date_updated=None,_id=None, user_id_task_owner=None, completed_by=None):
        self.task_name = task_name
        self.description = description
        self.priority = priority
        self.status_boolean = status_boolean
        self.status = status
        self.date_created = datetime.datetime.utcnow() if date_created is None else date_created
        self.date_updated = datetime.datetime.utcnow() if date_updated is None else date_updated
        self._id = uuid.uuid4().hex if _id is None else _id
        self.user_id_task_owner = user_id_task_owner
        self.completed_by = completed_by

    def find_status_text(self, status_boolean):
        if status_boolean:
            return "Done"
        else:
            return "Undone"

    @classmethod
    def find_task_docs_in_db(cls):
        return [cls(**elem) for elem in Database.find(task_constants.COLLECTION, {})]

    @classmethod
    def find_by_id(cls, task_id):
        return cls(**Database.find_one(task_constants.COLLECTION,{'_id':task_id}))

    def save_to_db(self):
        Database.update(task_constants.COLLECTION, {"_id": self._id}, self.json())

    def delete(self):
        Database.remove(task_constants.COLLECTION, {"_id": self._id})

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
