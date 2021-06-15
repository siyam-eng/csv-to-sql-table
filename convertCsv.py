from datetime import datetime


def convertToCsv(file, fieldProperty, assetCategory, **kwargs):
    print(kwargs)


fieldPropertyObj = [
    {
        "id": 1,
        "fieldName": "Custom field 1",
        "fieldStatus": "SHOW",
        "fieldMandatory": 1,
        "fieldColumnName": "userField1",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
    },
    {
        "id": 2,
        "fieldName": "Custom field 2",
        "fieldStatus": "SHOW",
        "fieldMandatory": 0,
        "fieldColumnName": "userField2",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": None,
        "fieldType": "INPUT",
    },
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
    },
    {
        "id": 15,
        "fieldName": "Category",
        "fieldStatus": "SHOW",
        "fieldMandatory": 1,
        "fieldColumnName": "assetCategory_id",
        "fieldEnabled": 1,
        "fieldOrder": None,
        "foreignTable": "assetCategory",
        "fieldType": "SELECT",
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
    "Room": {"id": 9, "shortName": "RO"},
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

# import hashlib
# from json import dumps
# from copy import deepcopy
# def document_etag(value, ignore_fields=None):
#     """Computes and returns a valid ETag for the input value.
#     :param value: the value to compute the ETag with.
#     :param ignore_fields: ignore_fields list of fields to skip to
#                           compute the ETag value.
#     .. versionchanged:: 0.5.4
#        Use json_encoder_class. See #624.
#     .. versionchanged:: 0.0.4
#        Using bson.json_util.dumps over str(value) to make etag computation
#        consistent between different runs and/or server instances (#16).
#     """
#     if ignore_fields:

#         def filter_ignore_fields(d, fields):
#             # recursive function to remove the fields that they are in d,
#             # field is a list of fields to skip or dotted fields to look up
#             # to nested keys such as  ["foo", "dict.bar", "dict.joe"]
#             for field in fields:
#                 key, _, value = field.partition(".")
#                 if value and key in d:
#                     filter_ignore_fields(d[key], [value])
#                 elif field in d:
#                     d.pop(field)
#                 else:
#                     # not required fields can be not present
#                     pass

#         value_ = deepcopy(value)
#         filter_ignore_fields(value_, ignore_fields)
#     else:
#         value_ = value

#     h = hashlib.sha1()
#     json_encoder = app.data.json_encoder_class()
#     h.update(
#         dumps(value_, sort_keys=True, default=json_encoder.default).encode("utf-8")
#     )
#     return h.hexdigest()


if __name__ == "__main__":
    convertToCsv(
        "/path/to/csv",
        fieldProperty=fieldPropertyObj,
        assetCategory=assetCategory,
        laptop=exampleSelectField1,
        assetStatus=statusEnum,
    )
