from sqlalchemy import text

from app.database.engine import engine


def init_database():

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )
