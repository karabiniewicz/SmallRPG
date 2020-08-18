from classes.game import Person, bcolors


magic = [{"name": "Fire", "cost": 10, "dmg": 50},
         {"name": "Water", "cost": 10, "dmg": 80},
         {"name": "Air", "cost": 10, "dmg": 50},]

player = Person(480, 60, 40, 34, magic)

print(player.generate_spell_damage(0))
print(player.generate_spell_damage(1))