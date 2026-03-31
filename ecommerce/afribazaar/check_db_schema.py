#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check table schema
cursor.execute("PRAGMA table_info(accounts_artisanprofile)")
columns = cursor.fetchall()

print("Columns in accounts_artisanprofile table:")
print("=" * 60)
for col in columns:
    cid, name, type_, notnull, dflt_value, pk = col
    print(f"{name:20} {type_:10} (null:{notnull}, pk:{pk})")

conn.close()
