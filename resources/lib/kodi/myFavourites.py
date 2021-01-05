class MyFavourites:

    filename = "myFavourites.json"

    def __init__(self, vfs):
        self.vfs = vfs

    def get(self, elemtype):
        # get favourites
        favs = self.vfs.get_json_as_obj(self.filename)
        if elemtype not in favs:
            return None
        return favs.get(elemtype)

    def add(self, elemtype, elem):
        #add favs
        favs = self.vfs.get_json_as_obj(self.filename)
        if elemtype == "user":
            favs["user"].append(elem)
        else:
            favs["track"].append(elem)
        self.vfs.save_obj_to_json(self.filename, favs)

