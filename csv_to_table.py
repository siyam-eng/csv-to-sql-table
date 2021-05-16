"""Read assets from given csv file, validate the data and add them to a SQL Table"""

import csv
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from credentials import username, password
from data import CATEGORIES, FIELD_PROPERTIES
from datetime import datetime
from models import Asset
import time
import pandas as pd



username = username
password = password
host = "localhost:3306"
dbname = "csvtotable"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4"
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
my_sess = Session()



# Asset id starts with category short name and has 8 random digits afterwards
def assetid_is_valid(assetid, category_shortname):
    if len(assetid) == 10:
        if assetid.lower().startswith(category_shortname.lower()):
            if assetid[2:].isdigit():
                return "YES"
            return (
                "Failed: Asset id does not contain 8 digits after category short name"
            )
        return "Failed: Asset id does not start with category short name"
    return "Failed: Asset id does not have 10 characters"


# check if asset id is unique
def assetid_is_unique(assetid, db_session, Asset):
    asset = db_session.query(Asset).filter_by(assetId=assetid).first()
    if not asset:
        return "YES"
    return "Failed: Given assetId already exists"


# generate new asset id with the given category short name
def generate_assetid(category_shortname, db_session, Model):
    if category_shortname:
        while True:
            digits = "".join([str(random.randint(0, 9)) for i in range(8)])
            assetid = category_shortname.upper() + digits

            if assetid_is_unique(assetid, db_session, Model):
                return assetid



# Validation function
def validate()



start = time.perf_counter()

end = time.perf_counter()

print(f'It took {end - start} seconds to execute')