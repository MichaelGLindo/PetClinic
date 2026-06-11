import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration (matches application.properties)
DB_USER = "root"
DB_PASSWORD = "Admin123*"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "veterinaria"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
BASE_URL_WITHOUT_DB = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"

# Auto-create database if not exists
try:
    temp_engine = create_engine(BASE_URL_WITHOUT_DB)
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()
    temp_engine.dispose()
except Exception as e:
    print(f"Warning: Could not check/create database '{DB_NAME}' automatically: {e}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
