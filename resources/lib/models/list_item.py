import xbmcgui


class ListItem:
    id = 0
    label = ""
    label2 = None

    def to_list_item(self, addon_base):
        return addon_base, xbmcgui.ListItem(label=self.label), False
