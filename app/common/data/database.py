from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)
sess=SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        