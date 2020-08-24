from classes.game import Person, Colors
from classes.magic import Spell
from classes.inventory import Item

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
player_items = [potion, hipotion, superpotion, elixer, megaelixer, granade]


# Create People
player = Person(480, 60, 40, 34, player_magic, player_items)
enemy = Person(740, 40, 35, 25, [], [])

print("\n" + Colors.FAIL + Colors.BOLD + "Enemy attacks you!" + Colors.ENDC)
while True:
    player.choose_action()
    choice = input("Choose action:")
    choice = int(choice) - 1

    if choice == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
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
            enemy.take_damage(magic_dmg)
            print(Colors.BLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + Colors.ENDC)
    elif choice == 2:
        player.choose_item()
        item_choice = int(input("Choose item:")) - 1

        item = player.items[item_choice]
        if item.type == "potion":
            player.heal(item.prop)
            print(Colors)

    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacked for", enemy_dmg, "points of damage. Your HP:", player.get_hp())

    print("\n Enemy HP:", Colors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + Colors.ENDC)
    print("\n Your HP:", Colors.GREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + Colors.ENDC)

    print("\n Your MP:", Colors.BLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + Colors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(Colors.GREEN + "You win!" + Colors.ENDC)
        break
    elif player.get_hp() == 0:
        print(Colors.FAIL + "You lose!" + Colors.ENDC)
        break
