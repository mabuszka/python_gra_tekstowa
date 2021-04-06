from gierka.items import Potion, Weapon, Armor

## class to handle the managment of the inventory by the user
class InventoryManagment:
    ## the constructor
    # @param hero the hero of the game
    # @param backpack the backpack of the hero
    def __init__(self, game):
        self.hero = game.hero
        self.backpack = game.hero.backpack

    ## method used to used the Potion items
    # @param item_name the name of the potion to be used
    def drink_potion(self, item_name):
        potion = self.backpack.get_item(item_name)
        potion_type = potion.potion_type
        if potion_type == "mana":
            self.hero.up_mana(potion.bonus)
        else:
            self.hero.up_hp(potion.bonus)
        return "You drank the potion" + "\n" + "{} hp:{}, mp:{}".format(self.hero.get_name(), self.hero.hp, self.hero.mana)

    ## method to thorw items away from the users inventory
    # @param item_name the name of the item to be thrown away
    def throw_item_away(self, item_name):
        self.backpack.get_item(item_name)
        return "You threw away {}".format(item_name)

    ## the method used to equip the armor items from user inventory
    # @param the name of the armor to be equipped
    def equip_armor(self, item_name):
        armor_piece = self.backpack.get_item(item_name)
        armor_type = armor_piece.get_armor_type()
        if not self.hero.armor[armor_type]:
            self.hero.armor[armor_type] = armor_piece
        else:
            old_armor = self.hero.armor[armor_type]
            self.hero.armor[armor_type] = armor_piece
            self.backpack.put_item(old_armor)
        return "You equipped: {}".format(item_name)

    ## the method used to equip the weapon item from user inventory
    # @param the name of the item to be equipped
    def equip_weapon(self, item_name):
        weapon = self.backpack.get_item(item_name)
        if not self.hero.weapon:
            self.hero.weapon = weapon
        else:
            old_weapon = self.hero.weapon
            self.hero.weapon = weapon
            self.backpack.put_item(old_weapon)
        return "You equipped: {}".format(item_name)

    ## the method used to list all of the inventory ites, and information about it, of the user for the user
    def check_inventory(self):
        text = self.list_items_in_backpack()
        text += "\n \n" + self.list_equiped_armor()
        text += "\n \n" + self.list_equiped_weapon()
        text += "\nYour total carried weight {}/{}".format(self.hero.get_carried_weight(), self.hero.max_weight)
        return text


    ## method that lists all of the items being held in the backpack and info about them, used by check_inventory function
    def list_items_in_backpack(self):
        backpack = ["Items in your backpack:"]
        for k in self.backpack.items:
            if self.backpack.items[k]:
                how_many = len(self.backpack.items[k])
                weight = self.backpack.items[k][0].get_weight()
                backpack.append("{} :\n \t weight : {}, how many : {}".format(k, weight, how_many))
        return "\n".join(backpack)

    ## method that lists all of the equipped armor of the users an info about it, used by check_inventory function
    def list_equiped_armor(self):
        armor = ["Your armor:"]
        for k in self.hero.armor:
            piece = self.hero.armor[k]
            if piece:
                armor.append("{} : {}, \n \t defence : {}, weight : {}".format(piece.get_armor_type(), piece.get_item_name(),
                                                                               piece.get_defence(), piece.get_weight()))
        if len(armor) == 1:
            armor.append("You don't have any armor")
        return "\n".join(armor)

    ## method that lists the equipped weapon of the user and info about it, used by check_inventory function
    def list_equiped_weapon(self):
        weapon = ["Your weapon:"]
        piece = self.hero.weapon
        if piece:
            weapon.append("{}, \n \t attack : {}, weight : {}".format(piece.get_item_name(), piece.get_attack(), piece.get_weight()))
        if len(weapon) == 1:
            weapon.append("You don't have a weapon")
        return "\n".join(weapon)

    ## method that creates a list of all the potions currently in the user's backpack, and info about them
    def list_potions(self):
        potions = []
        for item_name, item_list in self.backpack.items.items():
            if item_list:
                if isinstance(item_list[0], Potion):
                    potions.append((item_name, item_list[0].potion_type, item_list[0].bonus))
        return potions

    ## method that creates a list of all the armor pieces currently in the user's backpack, and info about them
    def list_armor(self):
        armor_list = []
        for item_name, item_list in self.backpack.items.items():
            if item_list:
                if isinstance(item_list[0], Armor):
                    armor_list.append((item_name, item_list[0].get_armor_type(), item_list[0].get_defence()))
        return armor_list

    ## method that creates a list of all the weapons currently in the user's backpack, and info about them
    def list_weapon(self):
        weapon_list = []
        for item_name, item_list in self.backpack.items.items():
            if item_list:
                if isinstance(item_list[0], Weapon):
                    weapon_list.append((item_name, item_list[0].get_attack()))
        return weapon_list

    ## the main method of the class. Used by the Game class to allow the user to manage their's inventory. Interprets input form the user and calls appropriate functions.
    def manage_inventory(self):
        manage = True
        while manage:
            print("1. List inventory")
            print("2. Drink potion")
            print("3. Equip armor")
            print("4. Equip weapon")
            print("5. Throw away item")
            print("6. End inventory managment")
            command = None
            while command not in [str(k) for k in range(1,7)]:
                command = input(">>")
                if command not in [str(k) for k in range(1,7)]:
                    print("Invalid command, try again")
            if command == "1":
                print(self.check_inventory())
            elif command == "2":
                potions = self.list_potions()
                if potions:
                    i = 1
                    for potion in potions:
                        print("{}. {} - {} potion, +{}".format(i,*potion))
                        i += 1
                    potion_command = None
                    while potion_command not in [str(k) for k in range(1, len(potions) + 1)]:
                        potion_command = input(">>")
                        if potion_command not in [str(k) for k in range(1, len(potions) + 1)]:
                            print("Invalid command, try again")
                    potion = potions[int(potion_command) - 1][0]
                    print(self.drink_potion(potion))
                else:
                    print("You don't have any potions in your inventory")
            elif command == "3":
                armor = self.list_armor()
                if armor:
                    i = 1
                    for armor_piece in armor:
                        print("{}. {} - {}, defence {}".format(i,*armor_piece))
                        i += 1
                    armor_command = None
                    while armor_command not in [str(k) for k in range(1, len(armor) + 1)]:
                        armor_command = input(">>")
                        if armor_command not in [str(k) for k in range(1, len(armor) + 1)]:
                            print("Invalid command, try again")
                    armor_piece = armor[int(armor_command) - 1][0]
                    print(self.equip_armor(armor_piece))
                else:
                    print("You don't have any armor in your inventory")
            elif command == "4":
                weapon_list = self.list_weapon()
                if weapon_list:
                    i = 1
                    for weapon in weapon_list:
                        print("{}. {} - attack {}".format(i,*weapon))
                        i += 1
                    weapon_command = None
                    while weapon_command not in [str(k) for k in range(1, len(weapon_list) + 1)]:
                        weapon_command = input(">>")
                        if weapon_command not in [str(k) for k in range(1, len(weapon_list) + 1)]:
                            print("Invalid command, try again")
                    weapon = weapon_list[int(weapon_command) - 1][0]
                    print(self.equip_weapon(weapon))
                else:
                    print("You don't have any weapons in your inventory")
            elif command == "5":
                count = 0
                items = []
                for item_name in self.backpack.items:
                    if self.backpack.items[item_name]:
                        items.append(item_name)
                        count += 1
                        print("{}. {}".format(count, item_name))
                throw_command = None
                while throw_command not in [str(k) for k in range(1, count + 1)]:
                    throw_command = input(">>")
                    if int(throw_command) not in range(1, count + 1):
                        print("Invalid command, try again")
                    item_name = items[int(throw_command) - 1]
                    print(self.throw_item_away(item_name))
            else:
                manage = False














