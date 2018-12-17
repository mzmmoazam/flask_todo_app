
from .database import database


class Todo():
    def __init__(self):
        self.db = database(database='todo',tablename ="todo")
        self.tasks = [ task for task in self.db]
        self.query = "select * from {0} where {1} {2} "
        self.due_date = self.db.due_date
        self.overdue = self.db.overdue
        self.finished = self.db.finished

    def insert(self,task,due_by,status):
        self.db.insert({"task":task,"due_by":due_by,"status" :status})
        self._update_list()

    def update(self,id,task,due_by,status):
        self.db.update({"id":id,"task":task,"due_by":due_by,"status" :status})
        self._update_list()

    def api(self,api_id,date=None):
        return self.db.api(api_id,date)

    def __iter__(self):
        for task in self.tasks:
            yield task

    def _update_list(self):
        self.tasks = [task for task in self.db]
