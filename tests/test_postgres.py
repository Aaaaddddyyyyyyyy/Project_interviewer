import os

from dotenv import load_dotenv
import psycopg


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")


connection_string = (
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
)


with psycopg.connect(connection_string) as conn:
    print("PostgreSQL connection successful!")

    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print("Database:")
        print(version[0])