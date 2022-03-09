from sqlalchemy import create_engine  # Copied imports  from fastapi sqlalchemy docs.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from time import sleep
import psycopg2 #Library to connect to postgres
from .config import settings

#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = 'postgresql://zgziodukncnnof:bb1176f2961766e2d5edf439b0889f1cbb52288983ea073e94ef387ddb3e5d59@ec2-18-215-8-186.compute-1.amazonaws.com:5432/dfhqvfedeess9u'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Setting connection with DataBase
# PS: thats only for reference --> kautad nüüd ju hoopiki sqlalchemyt db sessioniks. Ülal

#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password123', cursor_factory = RealDictCursor)#CursorFactory minig library teema, no matter::prg pole password
#        cursor = conn.cursor()
#        print("DataBase Connection Was a Huge and Massive Success!")
#        break
#    except Exception as error:
#        print("Connecting to database failed")
#        print("error was: ", error)
#        sleep(3)
