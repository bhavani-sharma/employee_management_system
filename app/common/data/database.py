from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 


engine = create_engine("sqlite:///./employee_management.db", connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)
sess=SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        