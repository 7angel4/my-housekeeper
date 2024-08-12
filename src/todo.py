from database import Database
from constants import *
from tabulate import tabulate
from argparse import BooleanOptionalAction

class Todo:
    def __init__(self):
        self.db = Database()

    def add_task(self, task, date=dt.date.today(), duration=None, completed=False):
        query = f'INSERT INTO {TODO} (date, task, duration, completed) VALUES (?, ?, ?, ?)'
        self.db.execute_query(query, (date_to_str(date), task, duration, completed))

    def update_task(self, date=dt.date.today(), task=None, completed=True):
        query = f"UPDATE {TODO} SET completed = {completed} WHERE date = '{date}'"
        if task:
            query += f" AND task = '{task}'"
        try:
            self.db.execute_query(query)
        except:
            raise RecordNotFoundException()

    def delete_task(self, date=dt.date.today(), task=None):
        query = f"DELETE FROM {TODO} WHERE date = '{date}'"
        if task:
            query += f" AND task = '{task}'"
        self.db.execute_query(query)

    def list_completed_tasks(self, date, headers, completed=True):
        query = f"SELECT {', '.join(headers)} FROM {TODO} WHERE date = '{date}' AND completed = {completed}"
        data = self.db.fetch_query(query)
        if data:
            print(f"Showing to-do's on {date}.")
            print(tabulate(data, headers=headers, tablefmt='grid'))
        else:
            print(f"No todo's on {date}.")

    def list_tasks(self, date=dt.date.today(), completed=None, print_dur=False):
        headers = ['task']
        if print_dur:
            headers.append('duration')
        
        completed = str_to_bool(completed)
        if completed == True or completed == None:
            print("Completed:")
            self.list_completed_tasks(date, headers, completed=True)
        if completed == False or completed == None:
            print('Incomplete:')
            self.list_completed_tasks(date, headers, completed=False)


def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help='actions on todo list', dest='action'
    )

    date_kwargs = {
        'help': f'date ({DATE_FMT})',
        'type': dt.date.fromisoformat
    }

    # add tasks
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    add_parser.add_argument('-t', '--task', required=True, help='to-do')
    add_parser.add_argument('-du', '--duration', required=False, help='estimated duration of task (in hours)')

    # complete task
    update_parser = subparsers.add_parser('complete', help='Complete a task')
    update_parser.add_argument('-d', '--date', **date_kwargs)
    update_parser.add_argument('-t', '--task', required=False, help='to-do (if no value passed, default to complete all tasks)')
    update_parser.add_argument('-u', '--undo', action=BooleanOptionalAction, help='boolean flag: undo a task')

    # list tasks
    list_parser = subparsers.add_parser('list', help='List task(s)')
    list_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    list_parser.add_argument('-c', '--completed', default=None, help='if true, show completed tasks only; if false, show incomplete tasks only; else, show both')
    list_parser.add_argument('-pd', '--print-dur', action=BooleanOptionalAction, help='boolean flag: print estimated durations of the tasks too')

    # delete tasks
    del_parser = subparsers.add_parser('delete', help='Delete a task')
    del_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    del_parser.add_argument('-t', '--task', required=False, help='to-do')

    return subparsers

def handle_cli(args):
    todo = Todo()
    if args.action == 'add':
        todo.add_task(args.task, date=args.date, duration=args.duration)
        print(f'Added task on {args.date}.')
    elif args.action == 'complete':
        completed = (not args.undo)
        todo.update_task(date=args.date, task=args.task, completed=completed)
        if completed:
            print(f'Task completed: {args.task}.')
        else:
            print(f'Task undone: {args.task}.')
    elif args.action == 'list':
        todo.list_tasks(date=args.date, completed=args.completed, print_dur=args.print_dur)
    elif args.action == 'delete':
        todo.delete_task(date=args.date, task=args.task)
        print(f"Deleted task(s) on {args.date}.")
   
