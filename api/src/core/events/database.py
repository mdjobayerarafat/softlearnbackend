import logging
import logfire
import os
import importlib
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

def import_all_models():
    base_dir = 'src/db'
    base_module_path = 'src.db'

    for root, dirs, files in os.walk(base_dir):
        module_files = [f for f in files if f.endswith('.py') and f != '__init__.py']

        path_diff = os.path.relpath(root, base_dir)
        current_module_base = (
            base_module_path if path_diff == '.'
            else f"{base_module_path}.{path_diff.replace(os.sep, '.')}"
        )

        for file_name in module_files:
            module_name = file_name[:-3]
            full_module_path = f"{current_module_base}.{module_name}"
            importlib.import_module(full_module_path)

# Import all models before creating engine
import_all_models()

# SQLite database file path
SQLITE_DATABASE_URL = "sqlite:///./learnhouse.db"

# Create engine with SQLite
engine = create_engine(
    SQLITE_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create all tables after importing all models
SQLModel.metadata.create_all(engine)
logfire.instrument_sqlalchemy(engine=engine)

async def connect_to_db(app: FastAPI):
    app.db_engine = engine
    logging.info("LearnHouse SQLite database has been started.")
    SQLModel.metadata.create_all(engine)

def get_db_session():
    with Session(engine) as session:
        yield session

async def close_database(app: FastAPI):
    logging.info("LearnHouse database has been shut down.")
    return app