"""Read assets from given csv file, validate the data and add them to a SQL Table"""

import csv
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from credentials import username, password
from convertCsv import fieldPropertyObj, assetCategory
from datetime import datetime
from models import Asset
import time


username = username
password = password
host = "localhost:3306"
dbname = "csvtotable"

# GLOBAL VARIABLES
VALID_ASSETS = []
INVALID_ASSETS = []
VALIDATED_ASSETIDS = set()

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4",
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
my_sess = Session()


# Asset id starts with category short name and has 8 random digits afterwards
def assetid_is_valid(assetid, category_shortname):
    """Check the validity of an assetId"""
    if len(assetid) == 10:
        if assetid.lower().startswith(category_shortname.lower()):
            if assetid[2:].isdigit():
                return "YES"
            return "Asset id does not contain 8 digits after category short name"
        return "Asset id does not start with category short name"
    return "Asset id does not have 10 characters"


# check if asset id is unique
def assetid_is_unique(assetid, db_session, Asset):
    """Check the uniqueness of an assetId"""
    asset = db_session.query(Asset).filter_by(assetId=assetid).first()

    return (not bool(asset)) and (assetid not in VALIDATED_ASSETIDS)


# generate new asset id with the given category short name
def generate_assetid(category_shortname, db_session, Model):
    """Generate a new unique assetId using the given category short name and db session and model"""
    if category_shortname:
        while True:
            digits = "".join([str(random.randint(0, 9)) for _ in range(8)])
            assetid = category_shortname.upper() + digits

            if assetid_is_unique(assetid, db_session, Model):
                return assetid


# Validation function
def validate(row : dict, field_properties: dict, asset_categories: dict, db_session, Model, **kwargs) -> dict:
    """Apply all validation rules to the given row"""
    asset = {}
    asset["Error"] = []
    field_value = None
    category_shortname = None
    category_id = None

    for field in field_properties:
        # field properties
        csvFieldName = field["fieldName"]
        dbFieldName = field["fieldColumnName"]
        fieldMandatory = field["fieldMandatory"]
        fieldType = field["fieldType"]
        foreignTable = field["foreignTable"]

        # csv field value
        try:
            field_value = row[csvFieldName]
        except KeyError as key:
            asset[dbFieldName] = field_value
            asset["Error"].append(f"Column {key} not given is csv file")

        # check if required value is null
        if (bool(fieldMandatory) and field_value) or not bool(fieldMandatory):
            asset[dbFieldName] = field_value

            # validate enum field
            if fieldType == "ENUM":
                enum = kwargs[foreignTable]
                if field_value in enum:
                    asset[dbFieldName] = field_value
                # enum validation fails
                else:
                    asset[dbFieldName] = field_value
                    asset["Error"].append(
                        f"This field should have any of these values:- {enum}"
                    )

            # validate select field
            if fieldType == "SELECT":
                # rules are same except for assetCategories
                if foreignTable != "assetCategories":
                    mapping = kwargs[foreignTable]
                    try:
                        asset[dbFieldName] = mapping[field_value]
                    # mapping not present
                    except KeyError as key:
                        asset[dbFieldName] = field_value
                        asset["Error"].append(
                            f"The mapping for {key} -> {foreignTable} is not provided"
                        )

                # if foreignTable is assetCategories validate assetCategory
                else:
                    # check if mapping is provided for the csv given category
                    try:
                        category = asset_categories[field_value]
                        try:
                            category_shortname = category["shortName"]
                            category_id = category["id"]
                            asset[dbFieldName] = category_id
                        except KeyError as key:
                            asset[dbFieldName] = category_id
                            asset["Error"].append(
                                f"KeyError in validating assetCategory: {key}"
                            )
                    # mapping not provided for csv given category
                    except KeyError:
                        asset[dbFieldName] = category_id
                        asset["Error"].append(
                            f"Mapping for {field_value} is not provided"
                        )

            # Validate assetId
            if dbFieldName == "assetId":
                # check if category_shortname exists
                if category_shortname:
                    assetId = field_value
                    # check if assetId exists
                    if assetId:
                        # check the validity of the given assetId
                        validity = assetid_is_valid(assetId, category_shortname)
                        if validity == "YES":
                            # check uniqueness of assetId
                            if assetid_is_unique(assetId, db_session, Model):
                                asset[dbFieldName] = assetId
                            # flag error if assetId is not unique
                            else:
                                asset[dbFieldName] = assetId
                                asset["Error"].append(
                                    f"assetId <{assetId}> is not unique"
                                )
                        # flag error if asset id is not valid
                        else:
                            asset[dbFieldName] = assetId
                            asset["Error"].append(
                                f"assetId <{assetId}> is not valid: {validity}"
                            )
                    # generate new assetId if it is not present
                    else:
                        assetId = generate_assetid(
                            category_shortname, db_session, Model
                        )
                        asset[dbFieldName] = assetId

        # required field not present
        else:
            asset[dbFieldName] = field_value
            asset["Error"].append(f"Required field '{csvFieldName}' not present")


    return asset


def validate_and_store(
    rows, field_properties, asset_categories, db_session, Model, **kwargs
):
    """Take all the rows from the csv file, validate them,
    save the valid and invalid rows to two different global variables"""
    for row in rows:
        asset = validate(
            row=row,
            field_properties=field_properties,
            asset_categories=asset_categories,
            db_session=db_session,
            Model=Model,
            **kwargs,
        )

        # save valid and invalid assets in different lists
        if asset["Error"]:
            INVALID_ASSETS.append(asset)
        else:
            del asset["Error"]
            asset["_created"] = datetime.now()
            asset["_updated"] = datetime.now()
            VALID_ASSETS.append(asset)
            VALIDATED_ASSETIDS.add(asset["assetId"])


def write_errors(field_properties, error_file_path):
    """Write the invalid rows to a error.csv file"""
    with open(error_file_path, "w") as f:
        fieldnames = [field["fieldName"] for field in field_properties]
        fieldnames.append("Error")
        csv_writer = csv.DictWriter(f, fieldnames)
        csv_writer.writeheader()

        header_mapping = {
            field["fieldColumnName"]: field["fieldName"] for field in field_properties
        }
        header_mapping["Error"] = "Error"

        for row in INVALID_ASSETS:
            new_row = {header_mapping[key]: value for key, value in row.items()}
            csv_writer.writerow(new_row)


# Combine all functions required to get the expected output
def convert_to_table(
    csv_file_path, error_file_path, field_properties, asset_categories, db_session, Model, **kwargs
):
    """Run all functions to convert the given csv file into an sql table"""
    try:
        with open(csv_file_path, "r") as f:
            csv_reader = csv.DictReader(f)
            validate_and_store(
                csv_reader,
                field_properties,
                asset_categories,
                db_session,
                Model,
                **kwargs,
            )
        # write the errors to 'errors.csv' file
        write_errors(field_properties, error_file_path)
        # save bulk data to sql from list
        engine.execute(Asset.__table__.insert(), VALID_ASSETS) if VALID_ASSETS else 0

        return {
            'status': 'Success',
            'valid_assets': len(VALID_ASSETS),
            'error_file_path': error_file_path
        }
    except Exception as exception:
        return {
            'status': 'Failed',
            'Exception Details': str(exception),
        }

if __name__ == '__main__':
    start = time.perf_counter()
    result = convert_to_table(
        csv_file_path="asset.csv",
        error_file_path='error.csv',
        field_properties=fieldPropertyObj,
        asset_categories=assetCategory,
        db_session=my_sess,
        Model=Asset,
        enum=["ACTIVE", "INACTIVE"],
        laptop={"": "Mapped -> empty"},
    )
    print(result)
    end = time.perf_counter()

    print(f"It took {end - start} seconds to execute")
