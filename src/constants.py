APP_NAME = "housekeeper"
DB_NAME = APP_NAME + ".db"

CREDENTIALS = "locker"
ACCOUNTANT = "accountant"
TODO = "anti-procrastinator"
FOOD_DIARY = "feeder"
POSITIVE_WORDS = "encourager"
TIMETABLE = "organizer"

PKEY = 'INTEGER PRIMARY KEY AUTOINCREMENT'
DEFAULT_TYPE = 'TEXT NOT NULL'
DB_COLUMNS = {
    CREDENTIALS : {'id': PKEY, 'site': DEFAULT_TYPE, 'username': DEFAULT_TYPE, 'password': DEFAULT_TYPE},
    ACCOUNTANT : {'id': PKEY, 'time': DEFAULT_TYPE, 'description': DEFAULT_TYPE, 'transaction': DEFAULT_TYPE},
    TODO : {'id': PKEY, 'task': DEFAULT_TYPE, 'status': DEFAULT_TYPE},
    FOOD_DIARY : {'id': PKEY, 'date': DEFAULT_TYPE, 'meal': DEFAULT_TYPE, 'description': DEFAULT_TYPE},
    POSITIVE_WORDS : {'id': PKEY, 'word': DEFAULT_TYPE},
    TIMETABLE : {'id': PKEY, 'date': DEFAULT_TYPE, 'time': DEFAULT_TYPE, 'event': DEFAULT_TYPE}
}

# General constants
DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H:%M:%S'