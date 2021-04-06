from gierka.door import Door

## class representing the room of the castle
class Room:
    ## the constructor
    # @param hero_in_room indcates whether the hero is in ths room
    # @param id the id of the room
    # @param neighbours holds the ids of the room neghbouring rooms an the door that lead between them
    # @param chest can be either empty or contain an item
    def __init__(self, id):
        self.hero_in_room = False
        self.id = id
        self.neighbours = {}
        self.chest = []

    ## method for adding the door between this room and another one
    # @param nb_id the id of the room we want to add the door to
    # @param door the Door object representing the door between the rooms
    def add_door(self, nb_id, door):
        self.neighbours[nb_id] = door

    ## method to get the id of the room
    def get_id(self):
        return self.id

    ## method to know whether the hero is in this room
    def hero_present(self):
        return self.hero_in_room

    ## method to get the ids of the rooms neighbours
    def get_neighbours_ids(self):
        return self.neighbours.keys()

    ## method to get the door leading from this room to another
    # @param room_id the id of the other room
    def get_door_to_room(self, room_id):
        return self.neighbours[room_id]

    ## method to ad an item to the chest of this room
    # @param item item to add to the chest
    def add_item_to_chest(self, item):
        self.chest = [item]


if __name__ == "__main__":
    r1 = Room(1)
    r2 = Room(2)
    d = Door(1,2, "blue", True)
    r1.add_door(2, d)
    r1.get_door_to_room(2).unlock_door()
    print(r1.get_door_to_room(2).is_locked())

