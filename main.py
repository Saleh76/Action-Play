# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:21:32 2020

@author: saleh
"""

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Black magic
fire = Spell("Fire", 15, 150, "black")
water = Spell("Water", 12, 120, "black")
air = Spell("Air", 10, 100, "black")
thunder = Spell("Thunder", 22, 300, "black")
blizzard = Spell("Blizzard", 20, 250, "black")
meteor = Spell("Meteor", 25, 350, "black")

# White magic
cure = Spell("Cure", 10, 100, "white")
cura = Spell("Cura", 15, 150, "white")

# Enemy Magic
magma = Spell("Magma", 15, 150, "black")
storm = Spell("Storm", 12, 120, "black")
#pitch = Spell("Pitch", 20, 200, "white")


# Item's
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals for 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals for 200 HP", 200)
elixir = Item("Elixir", "elixir", "Fully restore HP/MP of one", 9999)
megaelixir = Item("Mega-Elixir", "elixir", "Fully restore HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, water, air, thunder,
                 blizzard, meteor, cure, cura]
enemy_spells = [magma, storm]

player_items = [{"item": potion, "quantity": 10},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 1},
                {"item": elixir, "quantity": 2},
                {"item": megaelixir, "quantity": 1},
                {"item": grenade, "quantity": 1}]

# Characters
player1 = Person("Player 1", 600, 70, 60, 35, player_spells, player_items)
player2 = Person("Player 2", 800, 85, 80, 50, player_spells, player_items)
players = [player1, player2]

enemy1 = Person("Valor Murgholis", 1000, 65, 45, 25, enemy_spells, [])
enemy2 = Person("Xut", 1500, 80, 75, 35, enemy_spells, [])
enemies = [enemy1, enemy2]

running = True

print(bcolors.FAIL + bcolors.BOLD + "\nAn enemy attacks!\n" + bcolors.ENDC)

for enemy in enemies:
    enemy.get_enemy_stat()

while running:
    print("\n")
    print("\t  NAME")
    for player in players:
        player.get_stats()
    # Choose player
    for player in players:
        print("\n")
        player.choose_action()
        choice = input("Choose actions: ")
        index = int(choice) - 1

        # print("\n")

        # Attacks
        if index == 0:
            damage = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(damage)
            print("\n" + bcolors.OKBLUE + player.name + bcolors.ENDC + " attack " + bcolors.FAIL + enemies[enemy].name + bcolors.ENDC + " for", damage, "points of damage.")
            if enemies[enemy].get_hp() == 0:
                print("\n", bcolors.FAIL + enemies[enemy].name + bcolors.ENDC + " is Dead!!")
                del enemies[enemy]
            if len(enemies) == 0:
                # print(bcolors.OKGREEN + "YOO WIN!!" + bcolors.ENDC)
                running = False
        # Magic
        elif index == 1:
            # Choices from magic
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough magic point\n" + bcolors.ENDC)
                continue

            player.reduced_mp(spell.cost)

            # White magic
            if spell.cast == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals", str(magic_dmg), "points of health." + bcolors.ENDC)
            # Black magic
            elif spell.cast == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + bcolors.ENDC + bcolors.FAIL + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name + bcolors.ENDC + " is Dead!!")
                    del enemies[enemy]
                if len(enemies) == 0:
                    # print(bcolors.OKGREEN + "YOO WIN!!" + bcolors.ENDC)
                    running = False

        # Items
        elif index == 2:
            # Choices from items
            player.choose_item()
            item_choice = int(input("Chose item:")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\nNo more " + item.name, ".\n" + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            # Potion
            if item.kind == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals", str(item.prop), "points of health." + bcolors.ENDC)
            # Elixir
            elif item.kind == "elixir":
                if item.name == "Mega-Elixir":
                    for player in players:
                        player.hp = player.maxhp
                        player.mp = player.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "Fully restore HP/MP" + bcolors.ENDC)
            # Attack
            elif item.kind == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + bcolors.ENDC + bcolors.FAIL + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name + bcolors.ENDC + " is Dead!!")
                    del enemies[enemy]

                if len(enemies) == 0:
                    # print(bcolors.OKGREEN + "YOO WIN!!" + bcolors.ENDC)
                    running = False
    # Enemy Attack
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == len(enemies) and defeated_players == len(players):
        print(bcolors.FAIL + "\nIT'S A DRAW." + bcolors.ENDC)
        running = False
    elif defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "\nYOO WIN!!" + bcolors.ENDC)
        running = False
    elif defeated_players == len(players):
        print(bcolors.FAIL + "\nYOU LOOSE!!" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        #enemy_choice = random.randrange(0, len(enemies))
        print("\n")
        #if enemy_choice == 0:
        target = random.randrange(0, len(players))
        enemy_dmg = enemy.generate_damage()
        players[target].take_damage(enemy_dmg)
        print(bcolors.FAIL + str(enemy.name) + bcolors.ENDC + " attacks " + bcolors.OKBLUE + str(players[target].name) + bcolors.ENDC + " for", enemy_dmg, "damage.")
            # print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg, "damage.")
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stat()


    print("\n")
    print("-----------------------------------------------")
    # Results

