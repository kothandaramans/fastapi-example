from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

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

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Database connection was failed')
#         print('Error: ', error)
#         time.sleep(2)