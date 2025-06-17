import sqlite3

# Connect to database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("Clearing database...")

# Delete all records
cursor.execute("DELETE FROM tasks")
cursor.execute("DELETE FROM users")

conn.commit()

print("Database cleared!")

# Check results
cursor.execute("SELECT COUNT(*) FROM users")
users_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks")
tasks_count = cursor.fetchone()[0]

print(f"Users remaining: {users_count}")
print(f"Tasks remaining: {tasks_count}")

conn.close() 