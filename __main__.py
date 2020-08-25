from classes.game import Person, Colors
from classes.magic import Spell
from classes.inventory import Item
import random

# Black Magic
fire = Spell("Fire", 40, 150, "black")
water = Spell("Water", 15, 50, "black")
air = Spell("Air", 10, 30, "black")
thunder = Spell("Thunder", 30, 110, "black")
blizzard = Spell("Blizzard", 12, 70, "black")

# White Magic
cure = Spell("Cure", 10, 70, "white")
cura = Spell("Cura", 20, 170, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 150 HP", 150)
superpotion = Item("Super Potion", "potion", "Heals 450 HP", 450)
elixer = Item("Elixer", "elixer", "Restores yours HP/MP", 9999)
megaelixer = Item("Mega elixer", "elixer", "Restores party's HP/MP", 9999)
granade = Item("Granade", "attack", "Deals 500 HP", 500)

player_magic = [fire, water, air, thunder, blizzard, cura, cure]
enemy_magic = [fire, water, air]
player_items = [{"item": potion, "quantity": 13}, {"item": hipotion, "quantity": 4},
                {"item": superpotion, "quantity": 6}, {"item": elixer, "quantity": 2},
                {"item": megaelixer, "quantity": 2}, {"item": granade, "quantity": 4}]

# Create People
player1 = Person("Wojtek: ", 480, 460, 440, 634, player_magic, player_items)
player2 = Person("Piotrek:", 480, 362, 240, 234, player_magic, player_items)
player3 = Person("Janek:  ", 480, 601, 140, 134, player_magic, player_items)

enemy1 = Person("Ako: ", 840, 420, 135, 321, [], [])
enemy2 = Person("Paa: ", 340, 540, 335, 223, [], [])
enemy3 = Person("Time:", 1240, 240, 136, 125, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

print("\n" + Colors.FAIL + Colors.BOLD + "Enemy attacks you!" + Colors.ENDC)

while True:
    print("\n"
          "NAME             HP                                 MP"
          )

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        choice = int(choice) - 1

        if choice == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name.replace(":","") + "attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif choice == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(Colors.FAIL + "\nNot enough MP\n" + Colors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(Colors.BLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + Colors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(Colors.BLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + Colors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif choice == 2:
            player.choose_item()
            item_choice = int(input("Choose item:")) - 1

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(Colors.FAIL + "\n" + item.name, "is left..." + Colors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.value)
                print(Colors.GREEN + "\n" + item.name + " heals for", str(item.value), "HP" + Colors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(Colors.GREEN + "\n" + item.name + " fully restores HP/MP" + Colors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.value)

                print(Colors.FAIL + "\n" + item.name + " deals", str(item.value),
                      "points of damage to " + enemies[enemy].name + Colors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(Colors.GREEN + "You win!" + Colors.ENDC)
        break

    # Check if Enemy won
    elif defeated_players == 2:
        print(Colors.FAIL + "Your enemies have defeated you!" + Colors.ENDC)
        break

    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for",
                  enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(Colors.BLUE + spell.name + " heals " + enemy.name + " for", str(magic_dmg),
                      "HP." + Colors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)

                print(Colors.BLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + Colors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
                    defeated_players += 1

            # print("Enemy chose", spell, "damage is", magic_dmg)
    # Check if Enemy won
    if defeated_players == 3:
        print(Colors.FAIL + "Your enemies have defeated you!" + Colors.ENDC)
        break
