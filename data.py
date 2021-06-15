from datetime import datetime

def convertToCsv(file, fieldProperty, assetCategory, **kwargs):
    print(kwargs)


fieldPropertyObj = [
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
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/1"
        }
    }
}, {
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
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/8"
        }
    }
}, {
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
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/11"
        }
    }
}, {
    "id": 12,
    "fieldName": "Creation Date",
    "fieldStatus": "SHOW",
    "fieldMandatory": 1,
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
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/12"
        }
    }
}, {
    "id": 15,
    "fieldName": "Category",
    "fieldStatus": "SHOW",
    "fieldMandatory": 1,
    "fieldColumnName": "assetCategory",
    "fieldEnabled": 1,
    "fieldOrder": None,
    "foreignTable": "assetCategories",
    "fieldType": "SELECT",
    "fieldEditable": 0,
    "_etag": "",
    "_updated": "Thu, 13 May 2021 18:20:28 GMT",
    "_created": "Thu, 06 May 2021 18:48:51 GMT",
    "_links": {
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/15"
        }
    }
}, {
    "id": 15,
    "fieldName": "User field 1",
    "fieldStatus": "SHOW",
    "fieldMandatory": 1,
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
        "self": {
            "title": "Asset_field_statu",
            "href": "asset_field_status/15"
        }
    }
},

]
# assetID = {'key1':'value2'}
assetCategory = {
    'TELEVISION': {
        'id': 1,
        'shortName': 'TE'
    },
    'SWITCH': {
        'id': 2,
        'shortName': 'SW'
    },
    'BOX': {
        'id': 3,
        'shortName': 'BO'
    },
    'LAPTOP': {
        'id': 4,
        'shortName': 'LA'
    },
    'LAMP': {
        'id': 5,
        'shortName': 'LA'
    },
    'WASHING MACHINE': {
        'id': 6,
        'shortName': 'WA'
    },
    'WATCH': {
        'id': 2,
        'shortName': 'WA'
    }
}

exampleSelectField1 = {
    'value1': 10,
    'value2': 11,
    'value3': 12,
    'value3': 13,
    'value4': 14
}

statusEnum = ['ACTIVE','INACTIVE']

if __name__ == '__main__':
    convertToCsv(
        '/path/to/csv',
        fieldProperty=fieldPropertyObj,
        assetCategory=assetCategory,
        laptop=exampleSelectField1,
        assetStatus=statusEnum
                )



# final_data.append(
# dict(                        
# assetId=assetId,
# assetName=assetName,
# assetDescription=row["Description"],
# assetLocation=row['Location'],
# assetTags=row["Tags"],
# assetStatus=assetStatus,
# assetCategory_id=assetCategory_id,
# _created=datetime.now(),
# _updated=datetime.now(),
# assetMetadata=row["Metadata"],
# userField1=row["Field1"],
# userField2=row["Field2"],
# userField3=row["Field3"],
# ))


# TODO DIVIDING THE DATA INTO 10 PARTS TO IMPLEMENT THREADING
# with open('asset.csv', 'r') as f:
#     csv_reader = list(csv.DictReader(f))

#     for i in range(10):
#         data_segment = csv_reader[i * 1000 : (i + 1) * 1000]

row = {
    "custom field 1": "hello world",
    'User field 1': "test",
    "Description": "This is the description",
    "Status": "ACTIVE",
    "Category": "LAPTOP",
    "Creation Date": datetime.now(),
}