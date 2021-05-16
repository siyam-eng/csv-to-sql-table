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
def validate(row, **kwargs):
    asset = {}

    for field in FIELD_PROPERTIES:
        try:
            # field properties
            csvFieldName = field['fieldName']
            dbFieldName = field['fieldColumnName']
            fieldMandatory = field['fieldMandatory']
            fieldType = field['fieldType']
            foreignTable = field['foreignTable']

            # csv field value
            field_value = row[csvFieldName]

            # check if required value is null
            if (bool(fieldMandatory) and field_value) or not bool(fieldMandatory):
                asset[dbFieldName] = field_value

                # validate enum field
                if fieldType == 'ENUM':
                    enum = kwargs[foreignTable]
                    if field_value in enum:
                        asset[dbFieldName] = field_value
                    # enum validation fails
                    else:
                        asset[dbFieldName] = field_value
                        asset['Error'] = f"This field should have any of these values:- {enum}"

                # validate select field
                if fieldType == 'SELECT':
                    mapping = kwargs[foreignTable]
                    try:
                        asset[dbFieldName] = mapping[field_value]
                    # mapping not present
                    except KeyError as key:
                        asset[dbFieldName] = field_value
                        asset['Error'] = f"The mapping for {key} is not provided"

            # required field not present
            else:
                asset[dbFieldName] = field_value
                asset['Error'] = f"Required field '{csvFieldName}' not present"
        except KeyError as err:
            print(err)
            
    print('error', asset) if asset.get('Error') else print(asset)






start = time.perf_counter()
row = {'custom field 1': 'hello world', 'Description': 'This is the description', 'Status': 'ACTIVE', 'Category': 'LAPTOP'}
validate(row, enum=['ACTIVE', 'INACTIVE'], assetCategories={'LAPTOP': 1})

end = time.perf_counter()

print(f'It took {end - start} seconds to execute')