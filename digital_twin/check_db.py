import sqlite3

conn = sqlite3.connect('aeoncosma_data.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [row[0] for row in cursor.fetchall()]
print("Available tables:", tables)

for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f"  {table}: {count} records")

conn.close()
