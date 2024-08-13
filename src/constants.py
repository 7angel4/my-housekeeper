import datetime as dt

APP_NAME = "housekeeper"
DB_NAME = APP_NAME + ".db"

CREDENTIALS = "locker"
ACCOUNTING = "accountant"
TODO = "scheduler"
FOOD_DIARY = "feeder"
POSITIVITY = "encourager"

PKEY = 'PRIMARY KEY'
STR = 'TEXT'
INT = 'INTEGER'
DBL = 'REAL'
NONEMPTY = 'NOT NULL'

DB_COLUMNS = {
    CREDENTIALS : {'site': f'{STR} {NONEMPTY}', 'username': f'{STR} {NONEMPTY}', 'password': f'{STR} {NONEMPTY}'},
    ACCOUNTING : {'datetime': f'{STR} {NONEMPTY}', 'description': STR, 'amount': f'{DBL} {NONEMPTY}'},
    TODO : {'date': f'{STR} {NONEMPTY}', 'task': f'{STR} {NONEMPTY}', 'duration': DBL, 'completed': f'{INT} {NONEMPTY}'},
    FOOD_DIARY : {'date': f'{STR} {NONEMPTY}', 'meal': f'{STR} {NONEMPTY}', 'description': STR},
}

PRIMARY_KEYS = {
    CREDENTIALS : ('site', 'username'),
    ACCOUNTING : ('datetime',),
    TODO : ('date', 'task'),
    FOOD_DIARY : ('date', 'meal'),
}

def get_cols(table):
    return DB_COLUMNS[table].keys()

def parse_pk(table):
    pk = PRIMARY_KEYS[table]
    return pk[0] if len(pk) == 1 else ', '.join(pk)

# General constants
DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H:%M:%S'
DATETIME_FMT = DATE_FMT + ' ' + TIME_FMT

def date_to_str(date):
    return dt.date.strftime(date, DATE_FMT)

def time_to_str(time):
    return dt.time.strftime(time, TIME_FMT)

def datetime_to_str(datetime):
    return dt.datetime.strftime(datetime, DATETIME_FMT)

def combine_datetime_str(date, time):
    return datetime_to_str(dt.datetime.combine(date, time))

def str_to_bool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes'] if s != None else None

class RecordNotFoundException(Exception):
    """
    Exception raised when a queried record is not found
    (e.g. trying to update a non-existent record).
    """
    def __init__(self):
        super().__init__('Record not found')
