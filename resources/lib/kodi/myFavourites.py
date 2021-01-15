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

