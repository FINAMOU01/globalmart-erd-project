#!/usr/bin/env python
"""Switch database to SQLite"""

settings_path = 'afribazaar/settings.py'
with open(settings_path, 'r') as f:
    content = f.read()

old_db = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'afribazaar_db',
        'USER': 'afribazaar_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""

new_db = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

if old_db in content:
    content = content.replace(old_db, new_db)
    with open(settings_path, 'w') as f:
        f.write(content)
    print("Switched to SQLite")
else:
    print("Database already configured or format different")
