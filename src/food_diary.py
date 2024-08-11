from database import Database
from constants import *
from enum import Enum
import datetime as dt
from tabulate import tabulate
import argparse

class Meal(Enum):
    breakfast = 0
    lunch = 1
    dinner = 2
    snacks = 3
    afternoon_tea = 4
    brunch = 5
    drink = 6

    @classmethod
    def list(cls):
        return list(map(lambda e: e.name, cls))

class FoodDiary:
    def __init__(self):
        self.db = Database()

    def add_meal(self, date, meal, description):
        query = f'INSERT INTO {FOOD_DIARY} (date, meal, description) VALUES (?, ?, ?)'
        self.db.execute_query(query, (date, meal, description))

    def amend_meal(self, date, meal, description):
        query = f'''UPDATE {FOOD_DIARY} 
        set description = {description} 
        WHERE date = '{date}' AND meal = {meal}'''
        try:
            self.db.execute_query(query)
        except:
            raise RecordNotFoundException()

    def delete_meal(self, date, meal=None):
        query = f"DELETE FROM {FOOD_DIARY} WHERE date = '{date}'"
        if meal:
            query += f" AND meal = {meal}"
        self.db.execute_query(query)

    def list_meals(self, date=None):
        query = f"SELECT * FROM {FOOD_DIARY}"
        headers = [s.capitalize() for s in list(get_cols(FOOD_DIARY))]
        if date:
            data = self.db.fetch_query(query + " WHERE date = '{date}'")
        else:
            data = self.db.fetch_query(query)
        
        data = [(date, Meal(int(meal)).name, desc) for (date, meal, desc) in data]
        print(tabulate(data, headers=headers, tablefmt='grid'))

def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help='food diary', dest='action'
    )

    date_kwargs = {
        'help': f'date ({DATE_FMT})',
        'type': dt.date.fromisoformat
    }

    meal_kwargs = {
        # pass meal as int to the methods of `Food_diary`
        'type': (lambda s: Meal[s.lower()].value),
        'help': f'meal (one of: {Meal.list()})'
    }

    desc_kwargs = {
        'required': True,
        'help': 'What did you have?'
    }

    # add meals
    add_parser = subparsers.add_parser('add', help='Record a meal')
    add_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    add_parser.add_argument('-m', '--meal', default='snacks', **meal_kwargs)
    add_parser.add_argument('-de', '--description', **desc_kwargs)

    # update meals
    update_parser = subparsers.add_parser('update', help='Amend a meal')
    update_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    update_parser.add_argument('-m', '--meal', required=True, **meal_kwargs)
    update_parser.add_argument('-de', '--description', **desc_kwargs)

    # list meals
    list_parser = subparsers.add_parser('list', help='List meals')
    list_parser.add_argument('-d', '--date', **date_kwargs)

    # delete meals
    del_parser = subparsers.add_parser('delete', help='Delete meal(s)')
    del_parser.add_argument('-d', '--date', default=dt.date.today(), **date_kwargs)
    del_parser.add_argument('-m', '--meal', required=False, **meal_kwargs)

    return subparsers

def handle_cli(args):
    fd = FoodDiary()
    if args.action == 'add':
        fd.add_meal(args.date, args.meal, args.description)
        print(f'Recorded {Meal(args.meal).name} on {args.date}.')
    elif args.action == 'update':
        fd.amend_meal(args.date, args.meal, args.description)
        print(f'Amended {Meal(args.meal).name} on {args.date}.')
    elif args.action == 'delete':
        fd.delete_meal(args.date, meal=args.meal)
        if args.meal:
            print(f'Deleted {Meal(args.meal).name} on {args.date}.')
        else:
            print(f'Deleted all meals on {args.date}.')
    elif args.action == 'list':
        fd.list_meals(args.date)