import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

print(f"User: {DB_USER}")
print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"Pass len: {len(DB_PASS)}")
print(f"Pass bytes: {DB_PASS.encode('utf-8')}")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database='postgres',
        user=DB_USER,
        password=DB_PASS,
        port=int(DB_PORT)
    )
    print("Conexion exitosa!")
    conn.close()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
