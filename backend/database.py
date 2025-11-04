from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL for SQLite
# The database file will be created in the backend directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat_history.db"

# Create the SQLAlchemy engine
# connect_args is needed only for SQLite to allow multithreading
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class which will be our actual database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Function to create database tables from models
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
