from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.storage_config import storage_config


DATABASE_PATH = storage_config.database_path()
DATABASE_URL = URL.create(
    "sqlite",
    database=str(DATABASE_PATH),
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)
