from database import Database
from constants import *
from enum import Enum
from datetime import datetime

class Meal(Enum):
    breakfast = 0
    lunch = 1
    dinner = 2
    snacks = 3
    afternoon_tea = 4
    brunch = 5
    drink = 6

class FoodDiary:
    def __init__(self):
        self.db = Database()

    def _add(self, date, meal, description):
        query = f'INSERT INTO {FOOD_DIARY} (date, meal, description) VALUES (?, ?, ?)'
        self.db.execute_query(query, (date, Meal[meal.lower()], description))

    def add_meal(self, meal, description):
        date = datetime.today().strftime(DATE_FMT)
        self._add(date, meal, description)

    def amend(self, date, meal, description):
        query = f'''UPDATE {FOOD_DIARY} 
        set description = {description} 
        WHERE date = '{date}' AND meal = {Meal[meal.lower()]}'''
        self.db.execute_query(query)

    def summarize(self, date):
        query = f"SELECT (meal, description) FROM {FOOD_DIARY} WHERE date = '{date}'"
        for meal, description in self.db.fetch_query(query):
            print(f'{Meal(meal).name}: {description}')
