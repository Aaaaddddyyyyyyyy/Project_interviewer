import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver


load_dotenv()


connection_string = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}


pool = ConnectionPool(
    conninfo=connection_string,
    kwargs=connection_kwargs,
    max_size=10,
)


checkpointer = PostgresSaver(pool)