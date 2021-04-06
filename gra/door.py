## calss representing the door between the rooms of the castle
class Door:
    ## the constructor
    # @param rooms the ids of the two rooms between which the door will be
    # @param colour the colour of the door
    # @param locked indicates whether the door is locked
    def __init__(self, room_id1, room_id2, colour = "brown", locked = False):
        self.rooms = {room_id1, room_id2}
        self.colour = colour
        self.locked = locked

    ## mtehod used to unlock locked doors
    def unlock_door(self):
        if self.locked:
            self.locked = False

    ## method used to get the room between which the door is
    def get_rooms(self):
        return self.rooms

    ## method used to get tho colour of the door
    def get_colour(self):
        return self.colour

    ## mtehod used to get the information on whether the door is locked
    def is_locked(self):
        return self.locked

if __name__ == "__main__":
    d = Door(1,2, "blue", True)
    print(d.get_colour(), d.is_locked(), d.get_rooms())
    d.unlock_door()
    print(d.is_locked())
