import csv
import unittest
import csv_to_table
import os
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
    DateTime,
    Enum,
)


Base = declarative_base()


class Asset(Base):
    __tablename__ = "asset"

    id = Column(Integer, primary_key=True)
    assetId = Column(String(10), nullable=False, unique=True)
    assetName = Column(String(255), nullable=False)
    assetDescription = Column(Text)
    assetLocation = Column(Text)
    assetTags = Column(Text)
    assetStatus = Column(Enum("ACTIVE", "INACTIVE"), nullable=False)
    _created = Column(DateTime, nullable=False)
    _updated = Column(DateTime, nullable=False)
    assetCategory_id = Column(
        Integer, ForeignKey("assetCategories.id"), nullable=False, index=True
    )
    assetCategory = relationship(
        "AssetCategory",
        primaryjoin="Asset.assetCategory_id == AssetCategory.id",
        backref="assets",
    )
    assetMetadata = Column(Text)
    _etag = Column(String(50))
    userField1 = Column(String(125))
    userField2 = Column(String(125))
    userField3 = Column(String(125))
    userField4 = Column(String(125))
    userField5 = Column(String(125))


class AssetCategory(Base):
    __tablename__ = "assetCategories"

    id = Column(Integer, primary_key=True)
    assetCategoryName = Column(String(255), nullable=False, unique=True)
    assetCategoryLogo = Column(Text, nullable=False)
    editable = Column(Integer, nullable=False, default=1)
    _created = Column(DateTime, nullable=False)
    _updated = Column(DateTime, nullable=False)
    _etag = Column(String(50))
    shortName = Column(String(2), unique=True, nullable=False)


# Take the column values and create a new object (row in the table)
def insert_object(session, Model, **kwargs):
    # creating a movie object -> row in the table
    new_obj = Model(**kwargs)
    # adding the row
    session.add(new_obj)
    # commiting the row
    session.commit()

    return new_obj


# define a function to populate the AssetCategory database table
def insert_categories(db_session, AssetCategory):
    """Populate the AssetCategory table with some categories"""
    categories = [
        {"name": "TELEVISION", "shortname": "TE"},
        {"name": "SWITCH", "shortname": "SW"},
        {"name": "BOX", "shortname": "BO"},
        {"name": "LAPTOP", "shortname": "LA"},
        {"name": "LAMP", "shortname": "LM"},
        {"name": "WASHING MACHINE", "shortname": "WA"},
        {"name": "WATCH", "shortname": "WT"},

    ]

    for category in categories:
        name = category['name']
        shortname = category['shortname']
        insert_object(
            db_session,
            AssetCategory,
            assetCategoryName=name,
            shortName=shortname,
            assetCategoryLogo=f"Logo of {name}",
            editable=1,
            _created=datetime.now(),
            _updated=datetime.now(),
            _etag=f"Etag for {name}",
        )


# populate the asset table of the db
def insert_assets(db_session, Asset):
    """Populate the asset table of the db with dummy data"""
    assets = [
        {'assetId': 'TE87654329', 'assetName': 'LG TV', 'assetCategoryId': 1},
        {'assetId': 'BO12456899', 'assetName': 'BOX', 'assetCategoryId': 3},
        {'assetId': 'LA45689739', 'assetName': 'DELL LAPTOP', 'assetCategoryId': 4},
        {'assetId': 'WA78653299', 'assetName': 'BOSCH WASHING MACHINE', 'assetCategoryId': 6},
        {'assetId': 'TE65987459', 'assetName': 'SONY TV', 'assetCategoryId': 1},
        {'assetId': 'BO12457799', 'assetName': 'BOX 2', 'assetCategoryId': 3},

    ]
    for asset in assets:
        asset_name = asset['assetName']
        insert_object(
            db_session,
            Asset,
            assetId=asset['assetId'],
            assetName=asset_name,
            assetDescription=f"Description for {asset_name}",
            assetLocation="UK",
            assetTags=f'{asset_name.lower()} tag',
            assetStatus="ACTIVE",
            assetMetadata="DOP:17/12/2015",
            assetCategory_id=asset['assetCategoryId'],
            _created=datetime.now(),
            _updated=datetime.now(),
            _etag=f'{asset_name} e tag',
            userField1=f'User Field one for {asset_name}',
            userField2=f'User Field two for {asset_name}',
            userField3=f'User Field three for {asset_name}',
            userField4=f'User Field four for {asset_name}',

        )


# TODO(s)
# 1. set up a on memory sqlite3 database ✔
# 2. fill that database with dummy data ✔
# 3. load a asset.csv file 
# 4. write to a error.csv file
# 5. Delete those files after tests are done


class TestCsvToTable(unittest.TestCase):
    """Test Cases for the module csv_to_table"""

    @classmethod
    def setUpClass(cls) -> None:
        # set up the sqlite3 engine
        cls.engine = create_engine("sqlite+pysqlite:///:memory:")
        # create the session class
        cls.Session = sessionmaker(bind=cls.engine)
        # make a session object
        cls.my_sess = cls.Session()
        # create the tables into the database
        Base.metadata.create_all(cls.engine)
        # insert category data into the table
        insert_categories(cls.my_sess, AssetCategory)
        # insert asset data into the table
        insert_assets(cls.my_sess, Asset)

        # field properties
        cls.field_properties =  [
                            {
                                "id": 1,
                                "fieldName": "custom field 1",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 0,
                                "fieldColumnName": "userField1",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": None,
                                "fieldType": "INPUT",
                                "fieldEditable": 1,
                                "_etag": "",
                                "_updated": "Thu, 13 May 2021 18:33:20 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/1"}
                                },
                            },
                            {
                                "id": 8,
                                "fieldName": "Description",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 1,
                                "fieldColumnName": "assetDescription",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": None,
                                "fieldType": "TEXT",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 06 May 2021 19:50:03 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/8"}
                                },
                            },
                            {
                                "id": 11,
                                "fieldName": "Status",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 1,
                                "fieldColumnName": "assetStatus",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": "enum",
                                "fieldType": "ENUM",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 06 May 2021 19:50:03 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/11"}
                                },
                            },
                            {
                                "id": 12,
                                "fieldName": "Creation Date",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 0,
                                "fieldColumnName": "_created",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": None,
                                "fieldType": "DATE",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 06 May 2021 19:50:03 GMT",
                                "_created": "Thu, 06 May 2021 19:11:00 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/12"}
                                },
                            },
                            {
                                "id": 15,
                                "fieldName": "Category",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 1,
                                "fieldColumnName": "assetCategory_id",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": "assetCategories",
                                "fieldType": "SELECT",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 13 May 2021 18:20:28 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/15"}
                                },
                            },
                            {
                                "id": 15,
                                "fieldName": "User field 1",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 0,
                                "fieldColumnName": "userField1",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": "laptop",
                                "fieldType": "SELECT",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 13 May 2021 18:20:28 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "Asset_field_statu", "href": "asset_field_status/15"}
                                },
                            },
                            {
                                "id": 16,
                                "fieldName": "Asset ID",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 0,
                                "fieldColumnName": "assetId",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": None,
                                "fieldType": "TEXT",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 13 May 2021 18:20:28 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "", "href": ""}
                                },
                            },
                            {
                                "id": 17,
                                "fieldName": "Name",
                                "fieldStatus": "SHOW",
                                "fieldMandatory": 1,
                                "fieldColumnName": "assetName",
                                "fieldEnabled": 1,
                                "fieldOrder": None,
                                "foreignTable": None,
                                "fieldType": "TEXT",
                                "fieldEditable": 0,
                                "_etag": "",
                                "_updated": "Thu, 13 May 2021 18:20:28 GMT",
                                "_created": "Thu, 06 May 2021 18:48:51 GMT",
                                "_links": {
                                    "self": {"title": "", "href": ""}
                                },
                            },
                        ]
        
        cls.asset_categories = {
            "TELEVISION": {"id": 1, "shortName": "TE"},
            "SWITCH": {"id": 2, "shortName": "SW"},
            "BOX": {"id": 3, "shortName": "BO"},
            "LAPTOP": {"id": 4, "shortName": "LA"},
            "LAMP": {"id": 5, "shortName": "LA"},
            "WASHING MACHINE": {"id": 6, "shortName": "WA"},
            "WATCH": {"id": 2, "shortName": "WA"},
        }
        cls.test_asset_csv = 'test_asset.csv'
        cls.test_error_csv = 'test_error.csv'

        # write dummy asset data to a csv file 
        with open(cls.test_asset_csv, 'w') as f:
            test_assets = [
                {'Asset ID': 'TE87601329', 'Name': 'Samsung TV', 'Category': 'TELEVISION'},
                {'Asset ID': 'BO12401899', 'Name': 'BOX', 'Category': 'BOX'},
                {'Asset ID': 'LA45601739', 'Name': 'HP LAPTOP', 'Category': 'LAPTOP'},
                {'Asset ID': 'WA78601299', 'Name': 'NEW WASHING MACHINE', 'Category': 'WASHING MACHINE'},
                {'Asset ID': 'TE65901459', 'Name': 'SONY TV', 'Category': 'TELEVISION'},
                {'Asset ID': 'BO12401799', 'Name': 'NEW BOX', 'Category': 'BOX'},

            ]
            fieldnames = ['Name','Asset ID','Description','Location','Tags','Status','Category','Metadata','custom field 1','Creation Date','User field 1']
            csv_writer = csv.DictWriter(f, fieldnames)
            csv_writer.writeheader()
            for test_asset in test_assets:
                name = test_asset['Name']
                test_asset['Description'] = f'Description of {name}'
                test_asset['Location'] = f'Location of {name}'
                test_asset['Tags'] = f'Tags of {name}'
                test_asset['Status'] = f'Status of {name}'
                test_asset['Metadata'] = f'metadata of {name}'
                test_asset['custom field 1'] = f'custom field 1 of {name}'
                test_asset['Creation Date'] = f''
                test_asset['User field 1'] = f'User field 1 of {name}'

                csv_writer.writerow(test_asset)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_asset_csv):
            os.remove(cls.test_asset_csv)
        if os.path.exists(cls.test_error_csv):
            os.remove(cls.test_error_csv)

    def test_assetid_is_valid(self):
        """Test the assetid_is_valid function with different inputs"""
        self.assertEqual(csv_to_table.assetid_is_valid("LA88223345", "LA"), "YES")
        self.assertEqual(
            csv_to_table.assetid_is_valid("LA8822334", "LA"),
            "Asset id does not have 10 characters",
        )
        self.assertEqual(
            csv_to_table.assetid_is_valid("LP88223345", "LA"),
            "Asset id does not start with category short name",
        )
        self.assertEqual(
            csv_to_table.assetid_is_valid("LA8822334A", "LA"),
            "Asset id does not contain 8 digits after category short name",
        )

    def test_assetid_is_unique(self):
        """Test the assetid_is_unique function with different inputs"""

        self.assertTrue(
            csv_to_table.assetid_is_unique('LA77664455', TestCsvToTable.my_sess, Asset)
        )
        self.assertFalse(
            csv_to_table.assetid_is_unique('BO12457799', TestCsvToTable.my_sess, Asset)
        )

    def test_genrate_assetid(self):
        """Test the assetid_is_unique function with different inputs"""

        # test if the generated value is alphanumeric
        self.assertTrue(
            csv_to_table.generate_assetid('SW', TestCsvToTable.my_sess, Asset).isalnum()
        )
        # test if the generated value has 10 characters
        self.assertTrue(
            len(csv_to_table.generate_assetid('BO', TestCsvToTable.my_sess, Asset)) == 10
        )
        # test if the generated value has starts with the category shortname
        self.assertTrue(
            csv_to_table.generate_assetid('BO', TestCsvToTable.my_sess, Asset).startswith('BO')
        )

    def test_validate(self):
        """Test the validate function"""
        row1 = {"custom field 1": "hello world", 'User field 1': '', 'Description': 'living room tv', 'Status': 'ACTIVE', 'Creation Date': '', 'Category': 'TELEVISION', 'Asset ID': 'TE87654321', 'Name': 'LG TV'}
        output1 = csv_to_table.validate(row1, TestCsvToTable.field_properties, TestCsvToTable.asset_categories, TestCsvToTable.my_sess, Asset, enum=['ACTIVE', 'INACTIVE'], laptop={"": "Mapped -> empty"})
        if not bool(output1['Error']):
            del output1['Error']
        expected1 = {'userField1': 'Mapped -> empty', 'assetDescription': 'living room tv', 'assetStatus': 'ACTIVE', '_created': '', 'assetCategory_id': 1, 'assetId': 'TE87654321', 'assetName': 'LG TV'}
        self.assertEqual(
            output1,
            expected1,
        )

    def test_convert_to_table(self):
        self.assertEqual(csv_to_table.convert_to_table(
        csv_file_path=TestCsvToTable.test_asset_csv,
        error_file_path=TestCsvToTable.test_error_csv,
        field_properties=TestCsvToTable.field_properties,
        asset_categories=TestCsvToTable.asset_categories,
        db_session=TestCsvToTable.my_sess,
        Model=Asset,
        enum=["ACTIVE", "INACTIVE"],
        laptop={"": "Mapped -> empty"}),
    "SUCCESS: convertToSQL function ran without any exceptions")



if __name__ == "__main__":
    unittest.main()
