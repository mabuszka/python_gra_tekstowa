from gierka.hero import Hero
from gierka.castle import Castle
from gierka.battle import Battle
from gierka.inventory_managment import InventoryManagment
from gierka.items import Weapon, Armor, Item, Potion, Key
from random import choice, random

## @project The rpg text game

## the main class of the project manages all of the game. Interrets input form the user and calls apropriate functions.
# To quit the game the user has to input "q" durring their mian turn.
class Game:
    def __init__(self):
        ## the constructor
        # @param turn the indicator of which turn is it now
        # @param hero the hero of the game
        # @param castle the castle of the game
        # @param running indicates whether the game is running
        # @param command_dictionary the dictionary which holds the commands for the main user turn
        # @param possible_keys the list of possible key items
        # @param possible_armor the list of possible armor items
        # @param possible_weapons the list of possible weapon items
        # @param possible_potions the list of possible potion items
        # @param possible_monsters the list of possible monsters

        self.turn = 0
        self.hero = None
        self.castle = None
        self.running = True
        self.command_dictionary = {1 : "check doors",
                                   2 : "go to room {}",
                                   3 : "fight {}",
                                   4 : "manage items",
                                   5 : "unlock doors",
                                   6 : "open chest"}
        self.possible_keys = [("The big blue key", 3, "blue"),
                              ("The big brown key", 3, "brown"),
                              ("The big green key", 3, "green")]
        self.possible_weapons = [("Sword", 20, 35),
                                 ("Staff", 10, 28),
                                 ("Mace", 25, 40)]
        self.possible_armor = [("Wooden cap", 10, "hat", 3),
                               ("Chainmail", 35, "shirt", 10),
                               ("Old shoes", 5, "shoes", 1)]
        self.possible_potions = [("Big mana potion", 5, "mana", 30),
                                 ("Big health potion", 5, "health", 30)]
        self.possible_monsters = [("Big ogre", 120 ),
                                  ("Slime", 40),
                                  ("Dark hound", 80)]

    ## the method to make a new castle at the satrt of the game
    def make_new_castle(self):
        castle = Castle()
        self.castle = castle
        for i in range(10):
            castle.add_room(i)
        for i in range(9):
            castle.add_door_between_rooms(i, i+1)
        castle.add_door_between_rooms(0,9)

    ## the method to make a new hero at the game, the user gives it it's name
    def make_new_hero(self):
        name = input("Input your hero name:")
        hero = Hero(name=name)
        hero.set_castle(self.castle)
        self.hero = hero

    ## method to get the text version of the input commands from the main turn
    # @param type main type of the command
    # @param additional additional information  needed for some of the inputs
    def command(self, type, additional):
        string = self.command_dictionary[type]
        string = string.format(additional)
        return string

    ## method to interpret the input of the user
    # @param do_command the command inputted by the users
    def interpret_input(self, do_command):
        type, additional = do_command
        if type == 1:
            doors = ["The doors from this room:"]
            for a in self.hero.get_possible_moves():
                colour = self.castle.get_room(self.hero.get_position()).get_door_to_room(a[0]).get_colour()
                doors.append("door to room {} : {}, {}".format(a[0], "locked" if a[1] else "unlocked", colour))
            return "\n".join(doors)
        elif type == 2:
            self.hero.change_room(additional)
            return "You went to room {}".format(additional)
        elif type == 3:
            for monster_id in self.castle.monsters_positions[self.hero.get_position()]:
                if self.castle.monsters[monster_id].type == additional:
                    monster = self.castle.monsters[monster_id]
                    break
            b = Battle(self.hero, monster)
            outcome = b.battle()
            if outcome:
                self.castle.kill_monster(monster_id)
                return "You killed the {}".format(monster.type)
            else:
                self.running = False
                return "You died"
        elif type == 4:
            m = InventoryManagment(self)
            m.manage_inventory()
        elif type == 5:
            return self.door_unlocker()
        elif type == 6:
            return self.chest_manager(self.hero.get_position())

    ## the method to manage actions in regards to the rooms chest
    # @param room_id the id of the room whose chest the user wants to interact with
    def chest_manager(self, room_id):
        print("The item in the chest:")
        item = self.castle.rooms[room_id].chest[0]
        print("{}".format(item.item_name))
        print("Do you want to pick up the item?")
        print("1. Yes")
        print("2. No")
        pick_command = None
        while pick_command not in ["1", "2"]:
            pick_command = input(">>")
            if pick_command not in ["1", "2"]:
                print("Invalid command, try again")
        if pick_command == "2":
            self.castle.rooms[room_id].chest = []
            return "As you close the chest you hear a 'puff' sound"
        elif pick_command == "1":
            weight = item.get_weight()
            print(weight)
            if self.hero.get_carried_weight() + weight <= self.hero.max_weight:
                self.hero.backpack.put_item(item)
                self.castle.rooms[room_id].chest = []
                return "You picked up the item from the chest"
            else:
                return "You are caring too much to pick up this item"

    ## the method to actions to open the door
    def door_unlocker(self):
        locked_doors = []
        i = 1
        for a in self.hero.get_possible_moves():
            door = self.castle.get_room(self.hero.get_position()).get_door_to_room(a[0])
            if door.locked:
                locked_doors.append(door)
                colour = door.get_colour()
                print("{}. door to room {} : {}".format(i, a[0], colour))
                i += 1
        if locked_doors:
            unlock_command = None
            while unlock_command not in [str(k) for k in range(1, len(locked_doors) + 1)]:
                unlock_command = input(">>")
                if unlock_command not in [str(k) for k in range(1, len(locked_doors) + 1)]:
                    print("Invalid command, try again")
            door = locked_doors[int(unlock_command) - 1]
            keys = []
            for item_name in self.hero.backpack.items:
                item_list = self.hero.backpack.items[item_name]
                if item_list:
                    if isinstance(item_list[0], Key):
                        keys.append(item_list[0])
            if door.colour in [key.colour for key in keys]:
                index = [key.colour for key in keys].index(door.colour)
                door.unlock_door()
                self.hero.backpack.get_item(keys[index].item_name)
                return "You unlocked the door!"
            else:
                return "No key from your inventory seems to match the door's lock"
        else:
            return "All the doors from this room are open"

    ## the method to get the possible action options for the user
    def get_options(self):
        options = [(1,-1)]
        hero_position = self.hero.get_position()
        if self.hero.get_possible_moves():
            for k in self.hero.get_possible_moves():
                a = k[0]
                if not self.castle.get_room(hero_position).get_door_to_room(a).is_locked():
                    options.append((2,a))
        if hero_position in self.castle.monsters_positions:
            for m in self.castle.monsters_positions[hero_position]:
                monster_type = self.castle.monsters[m].type
                options.append((3, monster_type))
        options.append((4,-1))
        options.append((5,-1))
        if self.castle.rooms[hero_position].chest:
            options.append((6,-1))

        return options

    ## the method to list the available optin as text for the user
    def list_options(self):
        options = self.get_options()
        options_str = ["{}. ".format(i + 1) + self.command(*options[i]) for i in range(len(options))]
        return options_str

    ## method to coordinate the moving of the monster in the game
    def move_monsters(self):
        for monster in self.castle.monsters:
            self.castle.move_monster(monster)

    ## method which allows the user to play their turn, interpertes the user input and calls apropriate functions
    def make_user_turn(self):
        print("\nTurn:{}".format(self.turn))
        print("What do you want to do {}?".format(self.hero.get_name()))
        print("\n".join(self.list_options()))
        user_command = input(">>")
        if user_command == "q":
            self.running = False
            print("You quit the game")
        if user_command.isnumeric():
            if int(user_command) in range(1, len(self.get_options())+1):
                do_command = self.get_options()[int(user_command) - 1]
                print(self.interpret_input(do_command))
            else:
                print("Wanted to think out of the box? - unfortunately you just wasted a turn... ")
        else:
                print("Wanted to think out of the box? - unfortunately you just wasted a turn... ")

    ## the method used to spawn items in the chests of the rooms
    def spawn_items(self):
        for room_id in self.castle.rooms:
            room = self.castle.rooms[room_id]
            if random() > 0.5 and not room.chest:
                room.add_item_to_chest(self.random_item())

    ## the method used to spawn monster in the castle
    def spawn_monsters(self):
        for room_id in self.castle.rooms:
            room = self.castle.rooms[room_id]
            if random() > 0.7:
                self.castle.spawn_monster_in_room(room_id, *choice(self.possible_monsters))

    ## the mian method used to play the game, it calls all the apropriate functions for the game to run.
    def make_turn(self):
        while self.running:
            self.make_user_turn()
            self.move_monsters()
            self.spawn_monsters()
            self.spawn_items()
            self.turn += 1

    ## the function to select a random item to be put in the chest
    def random_item(self):
        item_type = choice(["armor", "weapon", "potion", "key"])
        if item_type == "armor":
            item = Armor(*choice(self.possible_armor))
        elif item_type == "weapon":
            item = Weapon(*choice(self.possible_weapons))
        elif item_type == "potion":
            item = Potion(*choice(self.possible_potions))
        else:
            item = Key(*choice(self.possible_keys))
        return item





if __name__ == "__main__":
    game = Game()
    game.make_new_castle()
    game.make_new_hero()
    game.hero.backpack.put_item(Weapon("sword", 15, 20))
    game.hero.backpack.put_item(Key("big blue key", 1, "blue"))
    game.hero.backpack.put_item(Key("big brown key", 1, "brown"))
    game.hero.backpack.put_item(Key("big green key", 1, "green"))
    game.castle.spawn_monster_in_room(0, "scary monster", 40)
    game.make_turn()

