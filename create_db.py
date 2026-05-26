import psycopg

conn = psycopg.connect('host=localhost user=postgres password=postgres dbname=postgres')
conn.autocommit = True
cur = conn.cursor()
try:
    cur.execute('CREATE DATABASE grupo63')
    print('Base de datos creada!')
except Exception as e:
    print(f'Error: {e}')
cur.close()
conn.close()
