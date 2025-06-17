import sqlite3

# Connect to database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("=== DATABASE CONTENTS ===")

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"Tables found: {len(tables)}")
for table in tables:
    print(f"- {table[0]}")

# View each table
for table_name in [t[0] for t in tables]:
    print(f"\n=== TABLE: {table_name} ===")
    
    # Get table structure
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print("Columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Get data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f"Records: {len(rows)}")
    
    if rows:
        column_names = [col[1] for col in columns]
        print("Data:")
        for i, row in enumerate(rows, 1):
            print(f"  Record {i}:")
            for j, value in enumerate(row):
                col_name = column_names[j]
                if col_name == 'password_hash':
                    print(f"    {col_name}: [ENCRYPTED]")
                else:
                    print(f"    {col_name}: {value}")

conn.close()
print("\n=== DONE ===") 