class TaskError(Exception):
    def __init__(self,message):
        self.message = message

class InvalidTaskPriorityCategory(TaskError):
    pass

class InvalidTaskStatusBoolean(TaskError):
    pass

class TaskCompletedByNotSpecified(TaskError):
    pass

class InvalidTaskID(TaskError):
    pass

class TaskOwnerIdIsNoLongerValid(TaskError):
    pass

class StatusBooleanNotUpdated(TaskError):
    pass
