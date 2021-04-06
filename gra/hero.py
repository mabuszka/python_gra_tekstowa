from gierka.backpack import Backpack
from gierka.items import Item, Armor, Weapon
from gierka.castle import Castle
from gierka.door import Door
from gierka.room import Room

## the class representing the hero of the game
class Hero:
    ## the constructor
    # @param name the name of the hero, given by the user
    # @param hp the current and max health points of the hero
    # @param mana the current and max mana points of the hero
    # @param backpack the object of class Backpack representing the backpack of the hero
    # @param armor the list of the armor that the hero has equipped
    # @param weapon the equpped weapon of the hero
    # @param castle the castle in which the hero is
    # @param max_weight the maximum weight that the hero can carry
    def __init__(self, name, hp = 100, mana = 100, max_weight = 100):
        self.name = name
        self.hp = [hp, hp]
        self.mana = [mana, mana]
        self.backpack = Backpack()
        self.armor = {}
        self.weapon = None
        self.position = 0
        self.castle = None
        self.max_weight = max_weight

    ## the method to set the castle in which the hero is
    # @param castle the castle to be set
    def set_castle(self, castle):
        self.castle = castle

    ## method to change the position of the hero
    # @param room_id the id of the room to which we want to move our hero
    def change_room(self, room_id):
        current_room_id = self.position
        current_room = self.castle.get_room(current_room_id)
        if room_id in current_room.get_neighbours_ids():
            door = current_room.get_door_to_room(room_id)
            if not door.is_locked():
                self.position = room_id

    ## method to list the rooms to which the hero can move from current position
    def get_possible_moves(self):
        current_room = self.castle.get_room(self.position)
        moves = [[k,current_room.get_door_to_room(k).is_locked()] for k in current_room.get_neighbours_ids()]
        return moves

    ## method to get how much weight does the hero carry right now
    def get_carried_weight(self):
        weight = self.backpack.get_weight()
        for k in self.armor:
            if self.armor[k]:
                weight += self.armor[k].get_weight()
        if self.weapon:
            weight += self.weapon.get_weight()
        return weight

    ## method to get current the position of the hero
    def get_position(self):
        return self.position

    ## method to get the name of the hero
    def get_name(self):
        return self.name

    ## method to get teh attack of the hero, if the hero doesn't have any weapon equipped his attack is equal to 25
    def get_attack(self):
        if self.weapon:
            return self.weapon.get_attack()
        return 25


    ## method to get the defence of the hero
    def get_defence(self):
        defence = 1
        for armor_name in self.armor:
            defence += self.armor[armor_name].get_defence()
        return defence

    ## method to lower the health of the hero, used in the battle
    def lower_hp(self, hp):
        if self.hp[0] < hp:
            self.hp[0] = 0
        else:
            self.hp[0] -= hp

    ## method to lower the mana of the hero, used in the battle
    def lower_mana(self, mp):
        if self.mana[0] < mp:
            self.mana[0] = 0
        else:
            self.mana[0] -= mp

    ## method to up the mana of the hero, either by resting in the battle or by potions
    def up_mana(self, mp):
        if self.mana[0] + mp > self.mana[1]:
            self.mana[0] = self.mana[1]
        else:
            self.mana[0] += mp

    ## method to up the health of the hero after using the potion
    def up_hp(self, hp):
        if self.hp[0] + hp > self.hp[1]:
            self.hp[0] = self.hp[1]
        else:
            self.hp[0] += hp



