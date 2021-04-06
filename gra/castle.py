from gierka.room import Room
from gierka.door import Door
from gierka.monster import Monster
from random import choice, choices

## class representing the castle in which the hero is having his adventure
class Castle():
    ## the constructor
    # @param rooms holds the pairs room_id (the id of the room): Room (an object of class Room)
    # @param monsters holds the pairs monster_id (the id of the monster): Monster (an object of class Monster)
    # @param monsters_positions holds the pairs position (id of the room) : list of monsters (a list containing the ids of the monsters that are in this room)
    def __init__(self):
        self.rooms = {}
        self.monsters = {}
        self.monsters_positions = {}

    ## method to add a new room to the castle
    # creates a Room object with given room_id
    # @param room_id the id which will be given to the new room
    def add_room(self, room_id):
        if room_id not in self.rooms:
            room = Room(room_id)
            self.rooms[room_id] = room

    ## method to add a door between two rooms
    # Ads a door between to rooms given their ids
    # @param room1_id id of the first room
    # @param room2_id id of the second room
    # @param door either None (default) in which case a new Door object will be created, or a Door object to be used
    def add_door_between_rooms(self, room1_id, room2_id, door = None):
        if door is None:
            door = Door(room1_id, room2_id, Castle.random_colour(), Castle.random_lock())
        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room2_id].add_door(room1_id, door)
            self.rooms[room1_id].add_door(room2_id, door)

    ## static method to make a Door object
    # @param room1_id id of the first room
    # @param room2_id id of the second room
    # @param colour the colour of the door
    # @param locked indicates whether the door should be locked or not
    @staticmethod
    def make_door(room1_id, room2_id, colour, locked):
        return Door(room1_id, room2_id, colour, locked)

    ## method to get a Room object given the room's id
    # @param room_id the id of the room
    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]

    ## method to spawn a moster in given room
    # @param room_id the id of the room in which the monster will be spawned
    # @param monster_type the type of the monster that will be spawned, the default value is "monster"
    # @param monster_health the health of the spawned monster, indicates how many health points will it have
    def spawn_monster_in_room(self, room_id, monster_type = "monster", monster_health = 80):
        id = self.get_new_monster_id()
        self.monsters[id] = Monster(id = id, position = room_id, type = monster_type, health=monster_health)
        if room_id in self.monsters_positions:
            self.monsters_positions[room_id].append(id)
        else:
            self.monsters_positions[room_id] = [id]


    ## method to get an id for new monster.
    # The method guarantees the the ids of the monsters will be unique
    def get_new_monster_id(self):
        i = 0
        while True:
            if i in self.monsters:
                i += 1
                continue
            return i

    ## the method to delete mosters
    # method used to delete the monster that the user killed in the battle
    # @param monster_id the id of the monster that will be deleted
    def kill_monster(self, monster_id):
        position = self.monsters[monster_id].position
        self.monsters.pop(monster_id)
        self.monsters_positions[position].remove(monster_id)

    ## helper method for moving mosters between rooms
    # used by move_monster function
    # @param monster_id id of the monster that will be moved
    # @param room_id the if of the room that the monster will be moved into
    def _move_monster(self, monster_id, room_id):
        current_room = self.monsters[monster_id].position
        self.monsters[monster_id].change_position(room_id)
        self.monsters_positions[current_room].remove(monster_id)
        if room_id in self.monsters_positions:
            self.monsters_positions[room_id].append(monster_id)
        else:
            self.monsters_positions[room_id] = [monster_id]

    ## method to move the monster around the castle
    # uses _move_monster function, chooses the destination from all of the possible ones at random
    # @param monster_id the id of the monster that should be moved
    def move_monster(self, monster_id):
        possible_moves = self.get_monster_possible_moves(monster_id)
        if possible_moves:
            move = choice(possible_moves)
            self._move_monster(monster_id, move)

    ## method to return the possible moves of given monster
    # @param monster_id the id of the monster that we want to know the possible moves of
    def get_monster_possible_moves(self, monster_id):
        current_room = self.get_room(self.monsters[monster_id].position)
        moves = []
        for k in current_room.get_neighbours_ids():
            if not current_room.get_door_to_room(k).is_locked():
                moves.append(k)
        return moves

    ## static method to choose a random colour for the doors
    @staticmethod
    def random_colour():
        return choice(["blue", "brown", "green"])

    ## static method to choose at random whether the door should be locke or not
    @staticmethod
    def random_lock():
        return choices([False, True], cum_weights = [1, 2])[0]


if __name__ == "__main__":
    c = Castle()
    for i in range(10):
        c.add_room(i)
    for i in range(9):
        c.add_door_between_rooms(i, i+1)
    # for i in range(9):
    #     print(c.rooms[i].get_door_to_room(i+1).get_rooms())
    c.add_door_between_rooms(0,9, Door(0,2))
    # print(c.rooms[0].get_neighbours_ids())
    for i in range(3):
        c.spawn_monster_in_room(i, "monster")
    print(c.monsters.items())
    print([(k[1], k[1].position) for k in c.monsters.items()])
    print(c.monsters_positions)
    c.move_monster(1)
    print([(k[1], k[1].position) for k in c.monsters.items()])
    print(c.monsters_positions)

