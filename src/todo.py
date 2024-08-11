from database import Database
from constants import *
from tabulate import tabulate

class Todo:
    def __init__(self):
        self.db = Database()

    def add_task(self, task, date=dt.date.today(), completed=False):
        query = f'INSERT INTO {TODO} (date, task, completed) VALUES (?, ?, ?)'
        self.db.execute_query(query, (date_to_str(date), task, completed))

    def complete_task(self, task, date=dt.date.today()):
        query = f"UPDATE {TODO} SET completed = {True} WHERE date = '{date}' AND task = '{task}'"
        try:
            self.db.execute_query(query)
        except:
            raise RecordNotFoundException()

    def delete_task(self, date=dt.date.today(), task=None):
        query = f"DELETE FROM {TODO} WHERE date = '{date}'"
        if task:
            query += f" AND task = '{task}'"
        self.db.execute_query(query)

    def list_tasks(self, date=dt.date.today(), completed=None):
        query = f'SELECT task FROM {TODO}'
        completed_tasks = self.db.fetch_query(query + ' WHERE completed = {True}')
        incomplete_tasks = self.db.fetch_query(query + ' WHERE completed = {False}')
        headers = ['task']
        if completed == True:
            print(tabulate(completed_tasks, headers=headers, tablefmt='grid'))
        elif completed == False:
            print(tabulate(incomplete_tasks, headers=headers, tablefmt='grid'))
        else:
            data = zip(incomplete_tasks, completed_tasks)
            print(tabulate(data, headers=['incomplete', 'completed'], tablefmt='grid'))