import requests
import json
import sqlite3

# Your QuickNode endpoint URL
url = "https://intensive-broken-mansion.btc.quiknode.pro/cd14386b95837ceba76b5f8b104d86254c0cda19/"

# Function to make a request to the Bitcoin node
def make_request(method, params=None):
    payload = json.dumps({
        "method": method,
        "params": params or [],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()  # Ensure we raise an error for bad HTTP responses
    return response.json()

# Fetch data from Bitcoin node
def fetch_data(block_hash, script_hex):
    block_stats = make_request("getblockstats", [block_hash, ["minfeerate", "avgfeerate"]])
    block = make_request("getblock", [block_hash])
    blockchain_info = make_request("getblockchaininfo")
    block_count = make_request("getblockcount")
    block_header = make_request("getblockheader", [block_hash])
    best_block_hash = make_request("getbestblockhash")
    decoded_script = make_request("decodescript", [script_hex])
    mempool_info = make_request("getmempoolinfo")
    raw_mempool = make_request("getrawmempool", [True])
    
    return {
        "block_stats": block_stats,
        "block": block,
        "blockchain_info": blockchain_info,
        "block_count": block_count,
        "block_header": block_header,
        "best_block_hash": best_block_hash,
        "decoded_script": decoded_script,
        "mempool_info": mempool_info,
        "raw_mempool": raw_mempool
    }

# Structure data for easier handling
def structure_data(data):
    return {
        "block_stats": json.dumps(data["block_stats"]),
        "block": json.dumps(data["block"]),
        "blockchain_info": json.dumps(data["blockchain_info"]),
        "block_count": data["block_count"].get("result", 0),
        "block_header": json.dumps(data["block_header"]),
        "best_block_hash": data["best_block_hash"].get("result", ""),
        "decoded_script": json.dumps(data["decoded_script"]),
        "mempool_info": json.dumps(data["mempool_info"]),
        "raw_mempool": json.dumps(data["raw_mempool"])
    }

# Insert data into SQLite database
def insert_data_into_db(data):
    conn = sqlite3.connect('quantum_btc.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO blocks (
        block_stats,
        block,
        blockchain_info,
        block_count,
        block_header,
        best_block_hash,
        decoded_script,
        mempool_info,
        raw_mempool
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["block_stats"],
        data["block"],
        data["blockchain_info"],
        data["block_count"],
        data["block_header"],
        data["best_block_hash"],
        data["decoded_script"],
        data["mempool_info"],
        data["raw_mempool"]
    ))
    
    conn.commit()
    conn.close()

# Function to format data for the quantum computer
def format_for_quantum_computer(structured_data):
    return {
        "block_stats": json.loads(structured_data["block_stats"]),
        "block_details": json.loads(structured_data["block"]),
        "blockchain_info": json.loads(structured_data["blockchain_info"]),
        "block_count": structured_data["block_count"],
        "block_header": json.loads(structured_data["block_header"]),
        "best_block_hash": structured_data["best_block_hash"],
        "decoded_script": json.loads(structured_data["decoded_script"]),
        "mempool_info": json.loads(structured_data["mempool_info"]),
        "raw_mempool": json.loads(structured_data["raw_mempool"])
    }

# Main function
def main():
    block_hash = "00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"  # Replace with actual block hash
    script_hex = "76a914fe7e0711287688b33b9a5c239336c4700db34e6388ac"  # Replace with actual script hex
    
    data = fetch_data(block_hash, script_hex)
    structured_data = structure_data(data)
    formatted_data = format_for_quantum_computer(structured_data)
    
    # Insert formatted data into the database
    insert_data_into_db(structured_data)
    
    # Output formatted data for verification
    print("Formatted Data for Quantum Computer:", json.dumps(formatted_data, indent=2))

if __name__ == "__main__":
    main()
