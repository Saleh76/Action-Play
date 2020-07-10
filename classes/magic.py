import random


class Spell:
    def __init__(self, name, cost, damage, cast):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.cast = cast

    def generate_spell_damage(self):
        low = self.damage - 15
        high = self.damage + 15
        return random.randrange(low, high)
