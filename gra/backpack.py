from gierka.items import Item

## the class representing the backpack of the hero
class Backpack:
    ## the consructor
    # @param weight the weight of all the items in the backpack
    # @param items list of the items in the back pack
    def __init__(self):
        self.items = {}
        self.weight = 0

    ## method to put items into the backpack
    # @param item the item to be put into the backpack
    def put_item(self, item):
        item_name = item.get_item_name()
        if item_name in self.items:
            self.items[item_name].append(item)
        else:
            self.items[item_name] = [item]
        self.weight += item.weight

    ## method used the get the weight of the backpack
    def get_weight(self):
        return self.weight

    ## mey=thod for getting the item from the backpack
    # @param item_name the name of the itme we want to get from the backpack
    def get_item(self, item_name):
        if item_name in self.items and self.items[item_name]:
            item = self.items[item_name][0]
            item_weight = item.get_weight()
            self.items[item_name].remove(item)
            self.weight -= item_weight
            return item

    ## method to check the item from the backpack whithout taking it out of the backpack
    # @param item_name the neme of the item we want to check
    def check_item(self, item_name):
        if item_name in self.items and self.items[item_name]:
            item = self.items[item_name][0]
            return item


