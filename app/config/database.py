from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()  # Load environment variables from .env file

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DEV_DATABASE")

if DATABASE_URL is None:
    raise ValueError("DEV_DATABASE environment variable is not set. Please check your .env file.")

engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for SQL query logging
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()