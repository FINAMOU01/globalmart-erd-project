import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(accounts_artisanprofile)")
columns = cursor.fetchall()
print("Columns in accounts_artisanprofile table:")
for row in columns:
    print(f"  {row[1]}: {row[2]}")

print("\nLooking for currency_preference:")
has_currency_pref = any(row[1] == 'currency_preference' for row in columns)
print(f"  Found: {has_currency_pref}")

conn.close()
