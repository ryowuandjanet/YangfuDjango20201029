from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'YfcaseDjango',        #此例為posts
        'USER': 'ryowu',                #此例為user
        'PASSWORD': 'leo140814',     #此例為自己設定的密碼
        'HOST': '127.0.0.1',        #此例為localhost
        'PORT': '5432',                 #此例為5432
    }
}
