from datetime import datetime


def convertToCsv(file, fieldProperty, assetCategory, **kwargs):
    print(kwargs)


fieldPropertyObj = [

    {
        "id": 6,
        "fieldName": "Asset ID",
        "fieldStatus": "SHOW",
        "fieldMandatory": 1,
        "fieldColumnName": "assetId",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 6, 19, 50, 3),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
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
        "_updated": datetime(2021, 5, 19, 17, 40, 6),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },
    {
        "id": 7,
        "fieldName": "Name",
        "fieldStatus": "SHOW",
        "fieldMandatory": 1,
        "fieldColumnName": "assetName",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 6, 19, 50, 3),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },
    {
        "id": 8,
        "fieldName": "Description",
        "fieldStatus": "SHOW",
        "fieldMandatory": 0,
        "fieldColumnName": "assetDescription",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "TEXT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 20, 10, 29, 34),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },
    {
        "id": 9,
        "fieldName": "Location",
        "fieldStatus": "SHOW",
        "fieldMandatory": 0,
        "fieldColumnName": "assetLocation",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 20, 10, 29, 37),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },
    {
        "id": 10,
        "fieldName": "Tags",
        "fieldStatus": "SHOW",
        "fieldMandatory": 0,
        "fieldColumnName": "assetTags",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 20, 10, 29, 39),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
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
        "_updated": datetime(2021, 5, 6, 19, 50, 3),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },

    {
        "id": 16,
        "fieldName": "Metadata",
        "fieldStatus": "SHOW",
        "fieldMandatory": 0,
        "fieldColumnName": "assetMetadata",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
        "fieldEditable": 0,
        "_etag": "",
        "_updated": datetime(2021, 5, 20, 10, 29, 56),
        "_created": datetime(2021, 5, 6, 18, 48, 51),
    },
]
# assetID = {'key1':'value2'}
assetCategory = {
    "TELEVISION": {"id": 1, "shortName": "TE"},
    "SWITCH": {"id": 2, "shortName": "SW"},
    "BOX": {"id": 3, "shortName": "BO"},
    "LAPTOP": {"id": 4, "shortName": "LA"},
    "LAMP": {"id": 5, "shortName": "LA"},
    "WASHING MACHINE": {"id": 6, "shortName": "WA"},
    "WATCH": {"id": 2, "shortName": "WA"},
    'Room': {'id': 9, 'shortName': 'RO'}
}

exampleSelectField1 = {
    "value1": 10,
    "value2": 11,
    "value3": 12,
    "value3": 13,
    "value4": 14,
}

statusEnum = ["ACTIVE", "INACTIVE"]

row = {
    "custom field 1": "hello world",
    "User field 1": "test",
    "Description": "This is the description of laptop",
    "Status": "ACTIVE",
    "Category": "LAPTOP",
    "Creation Date": datetime.now(),
    "Asset ID": "LA82097729",
}


if __name__ == "__main__":
    convertToCsv(
        "/path/to/csv",
        fieldProperty=fieldPropertyObj,
        assetCategory=assetCategory,
        laptop=exampleSelectField1,
        assetStatus=statusEnum,
    )
