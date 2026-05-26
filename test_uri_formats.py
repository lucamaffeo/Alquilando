import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'grupo63')

# Try different URI formats
uris = [
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    f"postgresql+psycopg2:///{DB_NAME}?host={DB_HOST}&port={DB_PORT}&user={DB_USER}&password={DB_PASS}",
]

for i, uri in enumerate(uris):
    print(f"\nTrying URI {i+1}: {uri[:50]}...")
    try:
        engine = create_engine(uri, echo=False, pool_pre_ping=True)
        connection = engine.connect()
        print(f"  SUCCESS!")
        connection.close()
        engine.dispose()
        break
    except Exception as e:
        print(f"  FAILED: {type(e).__name__}: {str(e)[:80]}...")
