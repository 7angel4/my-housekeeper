APP_NAME = "housekeeper"
DB_NAME = APP_NAME + ".db"

CREDENTIALS = "locker"
ACCOUNTING = "accountant"
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
    ACCOUNTING : {'datetime': f'{STR} {NONEMPTY}', 'description': STR, 'amount': f'{DBL} {NONEMPTY}'},
    TODO : {'date': f'{STR} {NONEMPTY}', 'task': f'{STR} {NONEMPTY}', 'completed': f'{INT} {NONEMPTY}'},
    FOOD_DIARY : {'date': f'{STR} {NONEMPTY}', 'meal': f'{STR} {NONEMPTY}', 'description': STR},
    POSITIVE_WORDS : {'comment_id': f'{INT} {NONEMPTY}', 'comment': f'{STR} {NONEMPTY}'},
    SCHEDULE : {'datetime': f'{STR} {NONEMPTY}', 'event': f'{STR} {NONEMPTY}'}
}

PRIMARY_KEYS = {
    CREDENTIALS : ('site', 'username'),
    ACCOUNTING : ('datetime',),
    TODO : ('date', 'task'),
    FOOD_DIARY : ('date', 'meal'),
    POSITIVE_WORDS : ('comment_id',),
    SCHEDULE : ('datetime',)
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

# Exceptions
class UnknownCommandException(Exception):
    """
    Exception raised for an unknown command.
    """
    def __init__(self):
        super().__init__('Unknown command')