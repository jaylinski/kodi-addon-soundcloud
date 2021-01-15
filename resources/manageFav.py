#!/usr/bin/python
# Micro script for add to favourites context menu functionality
# manageFav.py filePath [add|remove]:[user|track] itemName:itemId
# TODO: this might need to be implemented as a script plugin as an addon dependency
from lib.kodi.myFavourites import MyFavourites
import os
import sys
import xbmc
import json

def run():
    args = sys.argv[1:]
    filePath = args[0]
    command = args[1]
    item = args[2]

    if not os.path.exists(filePath):
        xbmc.log("Given file path doesn't exist!", xbmc.LOGERROR)
        sys.exit(1)
    if item is None or item == "":
        xbmc.log("Given item argument is missing to add!", xbmc.LOGERROR)
        sys.exit(1)
    if command.split(":")[0] not in ("add", "remove"):
        sys.exit(1)

    itemName = item.split(":")[0]
    itemId = item.split(":")[1]
    elemtype = command.split(":")[1].strip()
    command = command.split(":")[0].strip()

    if command=="add":
        f = open(os.path.join(filePath, MyFavourites.filename))
        data = json.load(f)
        collection = data.get(elemtype)

        if not isIdExist(collection, itemId):
            if collection is None:
                items = []
                data[elemtype] = items
            data[elemtype].append({
                "name": itemName,
                "id": itemId
            })
            with open(os.path.join(filePath, MyFavourites.filename), 'w') as f:
                json.dump(data, f)
    else:
        f = open(os.path.join(filePath, MyFavourites.filename))
        data = json.load(f)
        collection = data.get(elemtype)
        for elem in collection:
            if elem.get("id") == itemId:
                data[elemtype].remove(elem)
                break
        with open(os.path.join(filePath, MyFavourites.filename), "w") as f:
            json.dump(data, f)


def isIdExist(dictionary, id):
    if dictionary is not None:
        for d in dictionary:
            if d.get("id") == id:
                return True
        return False
    else:
        return False

run()
