APP_NAME = "housekeeper"
DB_NAME = APP_NAME + ".db"

CREDENTIALS = "locker"
ACCOUNTANT = "accountant"
TODO = "anti_procrastinator"
FOOD_DIARY = "feeder"
POSITIVE_WORDS = "encourager"
SCHEDULE = "scheduler"

PKEY = 'PRIMARY KEY'
STR = 'TEXT'
INT = 'INTEGER'
DBL = 'REAL'
NONEMPTY = 'NOT NULL'

DB_COLUMNS = {
    CREDENTIALS : {'site': f'{STR} {NONEMPTY}', 'username': f'{STR} {NONEMPTY}', 'password': f'{STR} {NONEMPTY}'},
    ACCOUNTANT : {'date': f'{STR} {NONEMPTY}', 'time': f'{STR} {NONEMPTY}', 'description': STR, 'amount': f'{DBL} {NONEMPTY}'},
    TODO : {'date': f'{STR} {NONEMPTY}', 'task': f'{STR} {NONEMPTY}', 'completed': f'{INT} {NONEMPTY}'},
    FOOD_DIARY : {'date': f'{STR} {NONEMPTY}', 'meal': f'{STR} {NONEMPTY}', 'description': STR},
    POSITIVE_WORDS : {'comment_id': f'{INT} {NONEMPTY}', 'comment': f'{STR} {NONEMPTY}'},
    SCHEDULE : {'date': f'{STR} {NONEMPTY}', 'time': f'{STR} {NONEMPTY}', 'event': f'{STR} {NONEMPTY}'}
}

PRIMARY_KEYS = {
    CREDENTIALS : ('site', 'username'),
    ACCOUNTANT : ('date', 'time'),
    TODO : ('date', 'task'),
    FOOD_DIARY : ('date', 'meal'),
    POSITIVE_WORDS : ('comment_id',),
    SCHEDULE : ('date', 'time')
}

def get_cols(table):
    cols = DB_COLUMNS[table].keys()
    cols.remove('id')
    return cols

def parse_pk(table):
    pk = PRIMARY_KEYS[table]
    return pk[0] if len(pk) == 1 else ', '.join(pk)

# General constants
DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H:%M:%S'