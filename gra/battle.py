from gierka.hero import Hero
from gierka.monster import Monster
from random import randrange

## the class to manage the battle between the hero and the monster
class Battle:
    ## the constructor
    # @param hero the hero of the game
    # @param the moster that the hero is fighting right now
    def __init__(self, hero, monster):
        self.hero = hero
        self.monster = monster

    ## method taht defines the turn of the monster in the battle. Makes random choices and calls aproptiate functions.
    def monster_turn(self):
        move = randrange(0,2)
        if move == 1:
            self.monster_attack()
        else:
            self.monster_heal()

    ## the method to define the attack of the monster
    def monster_attack(self):
        defence = self.hero.get_defence()
        damage = 40
        if defence > 1:
            damage = damage / (defence / 2)
        self.hero.lower_hp(damage)
        print("The {} attacked!".format(self.monster.type))

    ## the method to define the attack of the hero
    def hero_attack(self):
        self.monster.lower_hp(self.hero.get_attack())
        self.hero.lower_mana(20)

    ## the method that defines the rest option for the hero in the battle, allowing them to regain  mana
    def hero_rest(self):
        self.hero.up_mana(10)

    ## the method that allows the monster to regain health
    def monster_heal(self):
        self.monster.up_hp(5)
        print("The {} healed itself".format(self.monster.type))

    ## method that defines the turn of the hero in the battle, interpretes the input from the user and calls appropriate funstions
    def hero_turn(self):
        print("{} hp:{}, mp:{}".format(self.hero.get_name(), self.hero.hp, self.hero.mana))
        print("{} hp:{}".format(self.monster.type, self.monster.hp))
        print("What do you want to do?")
        print("1. attack (20 mana)")
        print("2. rest (recover 10 mana)")
        command = None
        while command not in ("1", "2"):
            command = input(">>")
            if command not in ("1", "2"):
                print("Invalid command")
        if command == "1":
            if self.hero.mana[0] >= 20:
                self.hero_attack()
            else:
                print("You don't have enough mana...")
        elif command == "2":
            self.hero_rest()

    ## the mian method of the class calls the functions describing the turns of the hero and the monster until the winer is decided and return the result of the battle
    def battle(self):
        while self.monster.hp > 0 and self.hero.hp[0] > 0:
            self.hero_turn()
            if self.monster.hp > 0:
                self.monster_turn()
        return self.monster.hp <= 0





if __name__ == "__main__":
    h = Hero("test")
    m = Monster(1,2)
    b = Battle(h,m)
    b.battle()
