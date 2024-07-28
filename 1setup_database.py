import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('quantum_btc.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for storing detailed block data
cursor.execute('''
CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_stats TEXT,
    block TEXT,
    blockchain_info TEXT,
    block_count INTEGER,
    block_header TEXT,
    best_block_hash TEXT,
    decoded_script TEXT,
    mempool_info TEXT,
    raw_mempool TEXT
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
