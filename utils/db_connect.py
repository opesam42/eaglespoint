import pymysql
import environ
from eaglespoint.settings import BASE_DIR, env
import os

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

def mysqlconnect():
    conn = pymysql.connect(
        host=env('DB_HOST'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD'),
        database=env('DB_NAME'),
        port=int(env('DB_PORT')),
        # ssl_ca = str(BASE_DIR / 'cert/ca.pem'),
        ssl={'ca': str(BASE_DIR / 'cert/ca.pem')}
    )

    cur = conn.cursor() 
    sql = "SELECT * FROM listing_listings"
    cur.execute(sql) 
    output = cur.fetchall() 
    print(output) 
      
    # To close the connection 
    conn.close() 

mysqlconnect()

