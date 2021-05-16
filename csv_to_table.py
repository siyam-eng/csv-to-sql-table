"""Read assets from given csv file, validate the data and add them to a SQL Table"""

import csv
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import insert
from credentials import username, password
from datetime import datetime
from models import Asset
import time

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


CATEGORIES = {
    1: {"name": "Television", "shortname": "TE"},
    2: {"name": "Switch", "shortname": "SW"},
    3: {"name": "BOX", "shortname": "BO"},
    4: {"name": "LAPTOP", "shortname": "LA"},
    5: {"name": "LAMP", "shortname": "LM"},
    6: {"name": "WASHING MACHINE", "shortname": "WA"},
    7: {"name": "WATCH", "shortname": "WT"},
}



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
def generate_assetid(category_shortname, db_session):
    if category_shortname:
        while True:
            digits = "".join([str(random.randint(0, 9)) for i in range(8)])
            assetid = category_shortname.upper() + digits

            if assetid_is_unique(assetid, db_session):
                return assetid


# if neither asset id nor category is provided flag error
def assetid_and_category_exists(assetid, category):
    # both are present
    if bool(assetid and category):
        return "YES"
    # if asset id is provided and category is not provided flag error
    elif assetid:
        return "Failed: Asset id is provided but category is not provided"
    # both are absent
    return "Failed: Asset id and category is not provided"



def insert_asset(session, Model, **kwargs):
    # creating a movie object -> row in the table
    new_asset = Model(**kwargs)
    # adding the row
    session.add(new_asset)
    # commiting the row
    session.commit()

    return new_asset


# Open the file to work with
def main():
    with open("asset.csv", "r") as f:
        csv_reader = csv.DictReader(f)

        with open('error.csv', 'w') as f:
            field_names = ['Name','Asset ID','Description','Location','Tags','Status','Category','Metadata','Field1','Field2','Field3','Comments', None]
            csv_writer = csv.DictWriter(f, field_names)
            csv_writer.writeheader()

            for row in csv_reader:

                # Retrieve the data
                assetId = row["Asset ID"]  # not nullable
                assetName = row["Name"]   # not nullable
                assetDescription = row["Description"]
                assetLocation = row['Location']
                assetTags = row["Tags"]
                assetStatus = row["Status"]  # not nullable
                assetCategory_id = row["Category"]  # not nullable
                assetMetadata = row["Metadata"]
                userField1 = row["Field1"]
                userField2 = row["Field2"]
                userField3 = row["Field3"]

                # TODO flag error if not nullable fields are null
                if assetId and assetName and assetStatus and assetCategory_id:

                    # check if categoryId is in the given categories
                    if assetCategory_id and assetCategory_id.isdigit() and int(assetCategory_id) in CATEGORIES:
                        category_shortname = CATEGORIES[int(assetCategory_id)]["shortname"]
                    
                        # generate an asset id if it does not exists
                        assetId = generate_assetid(category_shortname, my_sess) if not assetId else assetId

                        # check existence
                        if (existence := assetid_and_category_exists(assetId, assetCategory_id)) == "YES":
                                # check the validity of the assetId
                                if (validity := assetid_is_valid(assetId, category_shortname)) == "YES":
                                    # check the uniqueness of assetId
                                    if (uniqueness := assetid_is_unique(assetId, my_sess, Asset)) == "YES":
                                        # add the asset to database
                                        insert_asset(
                                            my_sess,
                                            Asset,
                                            assetId=assetId,
                                            assetName=assetName,
                                            assetDescription=assetDescription,
                                            assetLocation=assetLocation,
                                            assetTags=assetTags,
                                            assetStatus=assetStatus,
                                            assetMetadata=assetMetadata,
                                            assetCategory_id=assetCategory_id,
                                            _created=datetime.now(),
                                            _updated=datetime.now(),
                                            userField1=userField1,
                                            userField2=userField2,
                                            userField3=userField3,
                                        )
                                    else:
                                        row['Comments'] = uniqueness
                                        csv_writer.writerow(row)
                                else:
                                    row['Comments'] = validity
                                    csv_writer.writerow(row)
                        else:
                            row['Comments'] = existence
                            csv_writer.writerow(row)

                    else:
                        row['Comments'] = 'Failed: Category Id not in category mapping'
                        csv_writer.writerow(row)

                # Error messages if one of the required fields are not available
                elif not assetId:
                    row['Comments'] = 'Failed: The Field "assetId" is required'
                    csv_writer.writerow(row)
                elif not assetName:
                    row['Comments'] = 'Failed: The Field "assetName" is required'
                    csv_writer.writerow(row)
                elif not assetStatus:
                    row['Comments'] = 'Failed: The Field "assetStatus" is required'
                    csv_writer.writerow(row)
                elif not assetCategory_id:
                    row['Comments'] = 'Failed: The Field "assetCategory_id" is required'
                    csv_writer.writerow(row)



start = time.perf_counter()
main()
end = time.perf_counter()

print(f'It took {end - start} seconds to execute')