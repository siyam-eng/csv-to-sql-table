from sqlalchemy import create_engine, Column, String, Integer, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from credentials import username, password


username = username
password = password
host = 'localhost:3306'
dbname = 'world'


# MySQL engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4")
Session = sessionmaker(bind=engine)
my_sess = Session()
Base = declarative_base()