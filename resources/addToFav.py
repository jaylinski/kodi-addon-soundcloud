#!/usr/bin/python
# Micro script for add to favourites context menu functionality
from lib.kodi.myFavourites import MyFavourites
import os
import sys
import xbmc
import json

def run():
    filePath = sys.argv[1]
    item = sys.argv[2]

    if not os.path.exists(filePath):
        xbmc.log("Given file path doesn't exist!", xbmc.LOGERROR)
        sys.exit(1)
    if item is None or item == "":
        xbmc.log("Given item argument is missing to add!", xbmc.LOGERROR)
        sys.exit(1)

    f = open(os.path.join(filePath, MyFavourites.filename))
    data = json.load(f)
    users = data.get("user")
    itemName = item.split(":")[0]
    itemId = long(float(item.split(":")[1]))

    if not isIdExist(users, itemId):
        data["user"].append({
            "name": itemName,
            "id": itemId
        })
        with open(os.path.join(filePath, MyFavourites.filename), 'w') as f:
            json.dump(data, f)

def isIdExist(dictionary, id):
    for d in dictionary:
        if d.get("id") == id:
            return True
    return False

run()
