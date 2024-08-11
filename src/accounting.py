from database import Database
from tabulate import tabulate
from constants import *
import datetime as dt
import argparse


def date_to_str(date):
    return dt.date.strftime(date, DATE_FMT)

def time_to_str(time):
    return dt.time.strftime(time, TIME_FMT)

def datetime_to_str(datetime):
    return dt.datetime.strftime(datetime, DATETIME_FMT)

def combine_datetime_str(date, time):
    return datetime_to_str(dt.datetime.combine(date, time))

class Accountant:
    def __init__(self):
        self.db = Database()

    def add_transaction(self, datetime, description, amount):
        query = f'INSERT INTO {ACCOUNTING} (datetime, description, amount) VALUES (?, ?, ?)'
        self.db.execute_query(query, (datetime, description, amount))

    def delete_transaction(self, date, time=None):
        query = f'DELETE FROM {ACCOUNTING} WHERE '
        if time:
            query += f"datetime = '{combine_datetime_str(date, time)}'"
        else:
            query += f"date(datetime) = '{date_to_str(date)}'"
        self.db.execute_query(query)
    
    def update_transaction(self, datetime, description=None, amount=None):
        if description and amount:
            self.db.execute_query(f"UPDATE {ACCOUNTING} SET description = '{description}', amount = {amount} WHERE datetime = '{datetime_to_str(datetime)}'")
        elif description:
            self.db.execute_query(f"UPDATE {ACCOUNTING} SET description = '{description}' WHERE datetime = '{datetime_to_str(datetime)}'")
        elif amount:
            self.db.execute_query(f"UPDATE {ACCOUNTING} SET amount = {amount} WHERE datetime = '{datetime_to_str(datetime)}'")

    def list_transactions(self, date, time=None, list_all=False):
        query = f'''SELECT *
        FROM {ACCOUNTING}
        WHERE date(datetime) = '{date_to_str(date)}'
        '''
        # tabulate transactions
        data = self.db.fetch_query(query)
        if not time and list_all:
            headers = [s.capitalize() for s in list(get_cols(ACCOUNTING))]
            print(tabulate(data, headers=headers, tablefmt='grid'))

        # aggregate
        expenses = sum([entry[2] for entry in data if entry[2] < 0])
        income = sum([entry[2] for entry in data if entry[2] >= 0])
        net = income + expenses
        print(f"{'Expenditure':9s}: {expenses:05.02f}")
        print(f"{'Income':9s}: {income:05.02f}")
        print(f"{'Net gain':9s}: {net:05.02f}") 


def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help='accounting', dest='action'
    )

    date_kwargs = {
        'default': dt.date.today(),
        'help': f'date ({DATE_FMT})',
        'type': dt.date.fromisoformat
    }

    time_kwargs = {
        'help': f'time ({TIME_FMT})',
        'type': dt.time.fromisoformat
    }

    # add transaction
    add_parser = subparsers.add_parser('add', help='Record a new transaction')
    add_parser.add_argument('-d', '--date', **date_kwargs)
    add_parser.add_argument('-t', '--time', default=dt.datetime.now(), **time_kwargs)
    add_parser.add_argument('-de', '--description', required=False, help='description')
    add_parser.add_argument('-v', '--amount', required=True, help='transaction amount')

    # update transaction
    update_parser = subparsers.add_parser('update', help='Update a transaction')
    update_parser.add_argument('-d', '--date', **date_kwargs)
    update_parser.add_argument('-t', '--time', default=dt.datetime.now(), **time_kwargs)
    update_parser.add_argument('-de', '--description', required=False, help='new description')
    update_parser.add_argument('-v', '--amount', required=False, help='new transaction amount')

    # list transactions
    list_parser = subparsers.add_parser('list', help='List transactions')
    list_parser.add_argument('-d', '--date', **date_kwargs)
    list_parser.add_argument('-t', '--time', required=False, **time_kwargs)
    list_parser.add_argument('-a', '--all', action=argparse.BooleanOptionalAction, help='boolean flag: whether to list all transactions')

    # delete transaction
    del_parser = subparsers.add_parser('delete', help='Delete transaction(s)')
    del_parser.add_argument('-d', '--date', **date_kwargs)
    del_parser.add_argument('-t', '--time', default=dt.datetime.now(), **time_kwargs)
    del_parser.add_argument('-a', '--all', action=argparse.BooleanOptionalAction, help='boolean flag: whether to delete all transactions on the given date')

    return subparsers

def handle_cli(args):
    accountant = Accountant()
    if args.action == 'add':
        accountant.add_transaction(dt.datetime.combine(args.date, args.time), args.description, args.amount)
    elif args.action == 'update':
        accountant.update_transaction(dt.datetime.combine(args.date, args.time), args.description, args.amount)
    elif args.action == 'delete':
        time = None if args.all else args.time
        accountant.delete_transaction(args.date, time=time)
    elif args.action == 'list':
        accountant.list_transactions(args.date, time=args.time, list_all=args.all)
   

