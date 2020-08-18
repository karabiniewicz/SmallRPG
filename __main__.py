from classes.game import Person, Colors
from classes.magic import Spell

# Black Magic
fire = Spell("Fire", 40, 150, "black")
water = Spell("Water", 15, 50, "black")
air = Spell("Air", 10, 30, "black")
thunder = Spell("Thunder", 30, 110, "black")
blizzard = Spell("Blizzard", 12, 70, "black")

# White Magic
cure = Spell("Cure", 10, 70, "white")
cura = Spell("Cura", 20, 170, "white")

player = Person(480, 60, 40, 34, [fire, water, air, thunder, blizzard, cura, cure])
enemy = Person(740, 40, 35, 25, [])

print(Colors.FAIL + Colors.BOLD + "Enemy attacks you!" + Colors.ENDC)

while True:
    print("########################################")

    player.choose_action()
    choice = input("Choooooooose action:")
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
        enemy.take_damage(magic_dmg)
        print(Colors.BLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + Colors.ENDC)

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
