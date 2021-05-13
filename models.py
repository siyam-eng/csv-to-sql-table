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
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from credentials import username, password
from sqlalchemy.orm import relationship
from datetime import datetime

username = username
password = password
host = "localhost:3306"
dbname = "csvtotable"


# MySQL engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4"
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
my_sess = Session()


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


# Create the table(s)
# Base.metadata.create_all(engine)


# Take the column values and create a new object (row in the table)
def insert_object(session, Model, **kwargs):
    # creating a movie object -> row in the table
    new_obj = Model(**kwargs)
    # adding the row
    session.add(new_obj)
    # commiting the row
    session.commit()

    return new_obj


# asset = my_sess.query(Asset).filter_by(assetId='LA12345678').first()
def insert_categories():
    insert_object(
        
        my_sess,
        AssetCategory,
        assetCategoryName="TELEVISION",
        shortName="TE",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )
    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="SWITCH",
        shortName="SW",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )

    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="BOX",
        shortName="BO",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )
    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="LAPTOP",
        shortName="LA",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )

    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="Lamp",
        shortName="LM",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )

    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="WASHING MACHINE",
        shortName="WA",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )

    insert_object(
        my_sess,
        AssetCategory,
        assetCategoryName="WATCH",
        shortName="WT",
        assetCategoryLogo="Logo",
        editable=1,
        _created=datetime.now(),
        _updated=datetime.now(),
        _etag="Etag for switch",
    )





# # Name,Asset ID,Description,Location,Tags,Status,Category,Metadata,Field1,Field2,Field3,Comments
# insert_object(
#     my_sess,
#     Asset,
#     assetId="SW12345677",
#     assetName="Switch 2",
#     assetDescription="This is a switch",
#     assetLocation="UK",
#     assetTags='switch',
#     assetStatus="ACTIVE",
#     assetMetadata="DOP:17/12/2015",
#     assetCategory_id=2,
#     _created=datetime.now(),
#     _updated=datetime.now(),
#     _etag='laptop e tag',
#     userField1='',
#     userField2='',
#     userField3='',
#     userField4='',

# )

