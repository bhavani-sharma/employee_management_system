from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

DATA_DIR = Path(__file__).resolve().parent
DATA_DIR.mkdir(parents=True, exist_ok=True)

_DEFAULT_DATABASE_URL = f"sqlite:///{DATA_DIR / 'employee_management.db'}"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT_DATABASE_URL)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///") and not SQLALCHEMY_DATABASE_URL.startswith("sqlite:////"):
    relative_path = SQLALCHEMY_DATABASE_URL.removeprefix("sqlite:///")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{(DATA_DIR / relative_path).resolve()}"

print(f"DATABASE_URL = {SQLALCHEMY_DATABASE_URL!r}")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)
sess=SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        