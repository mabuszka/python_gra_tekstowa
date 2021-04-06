
## the main class describing the items
class Item:
    ## the constructor
    # @param item_name the name of the item
    # @param weight the weight of the item
    def __init__(self, item_name, weight):
        self.item_name = item_name
        self.weight = weight

    ## method to get the name of the item
    def get_item_name(self):
        return self.item_name

    ## method to get the weight of the item
    def get_weight(self):
        return self.weight


## class describing the key items
class Key(Item):
    ## the constructor
    # @param colour the colour of the key, to open the door the key has to have the same colour as the door
    def __init__(self, item_name, weight, colour):
        super().__init__(item_name, weight)
        self.colour = colour


## class describing the armor items
class Armor(Item):
    ## the constructor
    # @param aromor_type the type of the armor
    # @param defence the bonus defence the armor gives to the hero
    def __init__(self, item_name, weight, armor_type, defence):
        super().__init__(item_name, weight)
        self.armor_type = armor_type
        self.defence = defence

    ## method to get the type of the armor
    def get_armor_type(self):
        return self.armor_type

    ## method to get the defence of the armor
    def get_defence(self):
        return self.defence

## class describing the weapon items
class Weapon(Item):
    ## the constructor
    # @param attack the attack that the hero will have if he equips this weapon
    def __init__(self, item_name, weight, attack):
        super().__init__(item_name, weight)
        self.attack = attack

    ## method to get the attack
    def get_attack(self):
        return self.attack

## class describing the potion items
class Potion(Item):
    ## the constructor
    # @param potion_type whether the potion helps regain mana or health
    # @param bonus how much of mana/health can the potion help the hero regain
    def __init__(self, item_name, weight, potion_type, bonus):
        super().__init__(item_name, weight)
        self.bonus = bonus
        self.potion_type = potion_type



