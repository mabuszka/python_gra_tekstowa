## The class for monsters
# the class represents monsters that the user must fight
class Monster:
    ## the constructor
    # @param type the type of the monster
    # @param position the room that the monster is in
    # @param hp the health of the monster
    # @param id the unique id of the monster
    def __init__(self, id, position, health = 80, type = "monster"):
        self.type = type
        self.position = position
        self.hp = health
        self.id = id

    ## a method to change position of the monster
    # @param self object pointer
    # @param destination the destination to which the moster will be moved
    def change_position(self, destination):
        self.position = destination

    ## a method to lower the health of the monster, used in battle
    # @param hp indicates by how many health points should the monster's hp be lowered
    def lower_hp(self, hp):
        if self.hp < hp:
            self.hp = 0
        else:
            self.hp -= hp

    ## method to up the health of the monster
    # @param hp indicates by how many health points should the monster's hp be upped
    def up_hp(self, hp):
        self.hp += hp
