"""Read assets from given csv file, validate the data and add them to a SQL Table"""

import random

CATEGORIES = {
    1: {"name": "Television", "shortname": "TE"},
    2: {"name": "Switch", "shortname": "SW"},
    3: {"name": "BOX", "shortname": "BO"},
    4: {"name": "LAPTOP", "shortname": "LA"},

}


# Asset id starts with category short name and has 8 random digits afterwards
def assetid_is_valid(category_shortname, asset_id):
    if len(asset_id) == 10:
        if asset_id.lower().startswith(category_shortname.lower()):
            if asset_id[2:].isdigit():
                return True
            return (
                "Failed: Asset id does not contain 8 digits after category short name"
            )
        return "Failed: Asset id does not start with category short name"
    return "Failed: Asset id does not have 10 characters"


# TODO check if asset id is unique
def assetid_is_unique(assetid, db_assetids):
    return True
    pass


# generate new asset id with the given category short name
def generate_assetid(category_shortname, db_assetids):
    while True:
        digits = "".join([str(random.randint(0, 9)) for i in range(8)])
        assetid = category_shortname.upper() + digits

        if assetid_is_unique(assetid, db_assetids):
            return assetid


# if neither asset id nor category is provided flag error
def assetid_and_category_exists(assetid, category):
    # both are present
    if bool(assetid and category):
        return True
    # if asset id is provided and category is not provided flag error
    elif assetid:
        return 'Failed: Asset id is provided but category is not provided'
    # both are absent
    return 'Failed: Asset id and category is not provided'



# print(assetid_is_valid("CU", generate_assetid("cu", set())))

print(assetid_and_category_exists('TV567898', ''))
