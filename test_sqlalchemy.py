import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'grupo63')

uri = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"URI: {uri}")
print(f"URI bytes: {uri.encode('utf-8')}")
print(f"Position 96: {repr(uri[96] if len(uri) > 96 else 'N/A')}")

try:
    engine = create_engine(uri)
    connection = engine.connect()
    print("SQLAlchemy connection successful!")
    connection.close()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
