import unittest
from gierka.items import Item, Potion, Weapon, Armor
from gierka.castle import Castle
from gierka.hero import Hero
from gierka.backpack import Backpack
from gierka.room import Room
from gierka.door import Door
from gierka.monster import Monster
from gierka.battle import Battle


class MyTestCase(unittest.TestCase):

    def test_armor(self):
        armor = Armor("armor name", 10, "hat", 20)
        self.assertEqual(armor.item_name, "armor name")
        self.assertEqual(armor.get_defence(), 20)
        self.assertEqual(armor.get_weight(), 10)
        self.assertEqual(armor.armor_type, "hat")

    def test_weapon(self):
        w = Weapon("weapon name", 10, 20)
        self.assertEqual(w.get_weight(),10)
        self.assertEqual(w.item_name,"weapon name")
        self.assertEqual(w.get_attack(),20)

    def test_potion(self):
        p = Potion("potion", 5, "mana", 15)
        self.assertEqual(p.item_name, "potion")
        self.assertEqual(p.get_weight(),5)
        self.assertEqual(p.potion_type, "mana")
        self.assertEqual(p.bonus, 15)

    def test_door(self):
        d = Door(1,2, "blue", True)
        self.assertEqual(d.get_colour(), "blue")
        self.assertEqual(d.is_locked(), True)
        self.assertEqual(d.get_rooms(), {1,2})
        d.unlock_door()
        self.assertEqual(d.is_locked(), False)

    def test_backpack(self):
        b = Backpack()
        self.assertEqual(b.get_weight(), 0)
        item = Item("test", 100)
        b.put_item(item)
        self.assertEqual(b.get_weight(), 100)
        self.assertEqual(b.items["test"], [item])
        self.assertEqual(b.get_item("test"), item)
        self.assertEqual(b.get_weight(),0)

    def test_monster(self):
        m = Monster(1, 10, 100, "test monster")
        self.assertEqual(m.position, 10)
        m.change_position(20)
        self.assertEqual(m.position, 20)
        self.assertEqual(m.hp, 100)
        m.lower_hp(20)
        self.assertEqual(m.hp, 80)
        m.up_hp(10)
        self.assertEqual(m.hp, 90)
        m.lower_hp(200)
        self.assertEqual(m.hp, 0)
        self.assertEqual(m.type, "test monster")

    def test_room(self):
        r1 = Room(1)
        r2 = Room(2)
        self.assertEqual(r1.get_id(),1)
        self.assertNotEqual(r1, r2)
        d = Door(1,2, "blue", True)
        r1.add_door(2, d)
        self.assertIn(2,r1.get_neighbours_ids())
        self.assertEqual(r1.get_door_to_room(2), d)
        item = Item("test item", 20)
        self.assertEqual(r1.chest,[])
        r1.add_item_to_chest(item)
        self.assertEqual(r1.chest, [item])

    def test_hero(self):
        h = Hero("test")
        c = Castle()
        c.add_room(0)
        c.add_room(10)
        c.add_door_between_rooms(0,10, Door(0, 10, "blue", False))
        h.set_castle(c)
        self.assertEqual(h.get_name(), "test")
        self.assertEqual(h.hp, [100,100])
        h.lower_hp(20)
        self.assertEqual(h.hp, [80, 100])
        h.lower_mana(10)
        self.assertEqual(h.mana, [90,100])
        h.up_hp(30)
        h.up_mana(20)
        self.assertEqual(h.hp, [100,100])
        self.assertEqual(h.mana, [100, 100])
        self.assertEqual(h.get_position(), 0)
        h.change_room(10)
        self.assertEqual(h.get_position(), 10)
        self.assertEqual(h.get_attack(), 25)
        self.assertEqual(h.get_possible_moves(), [[0, False]])

    def test_battle(self):
        h = Hero("test")
        m = Monster(1, 10, 100, "test monster")
        b = Battle(h, m)
        b.monster_attack()
        self.assertEqual(h.hp, [60, 100])
        b.hero_attack()
        self.assertEqual(m.hp, 75)
        self.assertEqual(h.mana, [80, 100])







if __name__ == '__main__':
    unittest.main()
