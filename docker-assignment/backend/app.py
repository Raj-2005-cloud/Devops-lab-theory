from fastapi import FastAPI
import psycopg2
import os
import time

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


def get_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except Exception as e:
            print("Database not ready, retrying in 5 seconds...")
            time.sleep(5)


@app.on_event("startup")
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        name TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/user")
def insert_user(name: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(name) VALUES(%s)",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "user inserted"}


@app.get("/users")
def get_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return data
from fastapi.responses import FileResponse

@app.get("/")
def frontend():
    return FileResponse("index.html")
