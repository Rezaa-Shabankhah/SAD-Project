DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "university_association",
        "USER": "root",
        "PASSWORD": "12345",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
