from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from .create_db import create_db_if_missing

Base = declarative_base()

load_dotenv()

DB_USER=os.getenv('DB_USER', 'postgres')
DB_PASSWORD=os.getenv('DB_PASSWORD', '4521')
DB_NAME=os.getenv('DB_NAME', 'financial_tracker')
DB_HOST=os.getenv('DB_HOST', 'localhost')
DB_PORT=os.getenv('DB_PORT', '5432')

create_db_if_missing(DB_NAME,DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)


DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as conn:
        print("Successfull connection with database!")
except Exception as e:
    print(f"Coonection error {e}")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
