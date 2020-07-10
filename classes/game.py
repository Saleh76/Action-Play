# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 19:55:20 2020

@author: saleh
"""
import random


# from classes.magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, damage):
        self.hp += damage
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduced_mp(self, cost):
        self.mp -= cost

    def get_stats(self):
        hp_bar = ""
        mp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 50 / 2
        mp_bar_ticks = (self.mp / self.maxmp) * 50 / 4

        # Health bar
        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            hp_decr = 9 - len(hp_string)

            while hp_decr > 0:
                current_hp += " "
                hp_decr -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        # Magic bar
        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 9:
            mp_decr = 9 - len(mp_string)

            while mp_decr > 0:
                current_mp += " "
                mp_decr -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        # Print HP/MP Stats
        print(bcolors.BOLD + "\t" + self.name + bcolors.ENDC + "\n" +
              "HP " + current_hp + bcolors.OKGREEN + " |" + hp_bar + "|\n" + bcolors.ENDC +
              "MP " + current_mp + bcolors.OKBLUE + " |" + mp_bar + "|" + bcolors.ENDC)
        # print("\n")

    def get_enemy_stat(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 50 / 2

        # Health bar
        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            hp_decr = 9 - len(hp_string)

            while hp_decr > 0:
                current_hp += " "
                hp_decr -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(bcolors.BOLD + "\t" + self.name + bcolors.ENDC + "\n" +
              "HP " + current_hp + bcolors.FAIL + " |" + hp_bar + "|\n" + bcolors.ENDC)

    def choose_target(self, enemies):
        i = 1

        print("\n" + bcolors.FAIL + bcolors.BOLD + "Target:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("   " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("Choose enemy:")) - 1
        return choice


    def choose_action(self):
        i = 1
        print(bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "Actions" + bcolors.ENDC)
        for item in self.actions:
            print("   " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "Magic" + bcolors.ENDC)
        for spell in self.magic:
            print("   " + str(i) + ".", spell.name, "(cost : ", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "Items" + bcolors.ENDC)
        for item in self.items:
            print("   " + str(i) + ".", item["item"].name, "\t:",
                  item["item"].description + "  (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_spell_damage()

        # pct = self.hp/self.maxhp * 100

        if self.mp < spell.cost:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg

