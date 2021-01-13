#!/usr/bin/python
# Micro script for add to favourites context menu functionality
# manageFav.py filePath add|remove itemName:itemId
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
    if command not in ("add", "remove"):
        sys.exit(1)

    itemName = item.split(":")[0]
    itemId = long(float(item.split(":")[1]))

    if command=="add":
        f = open(os.path.join(filePath, MyFavourites.filename))
        data = json.load(f)
        users = data.get("user")

        if not isIdExist(users, itemId):
            data["user"].append({
                "name": itemName,
                "id": itemId
            })
            with open(os.path.join(filePath, MyFavourites.filename), 'w') as f:
                json.dump(data, f)
    else:
        f = open(os.path.join(filePath, MyFavourites.filename))
        data = json.load(f)
        users = data.get("user")
        for user in users:
            if user.get("id") == itemId:
                data["user"].remove(user)
                break
        with open(os.path.join(filePath, MyFavourites.filename), "w") as f:
            json.dump(data, f)


def isIdExist(dictionary, id):
    for d in dictionary:
        if d.get("id") == id:
            return True
    return False

run()
