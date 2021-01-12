import random
from enum import Enum


class Alignment(Enum):
    CHAOTIC_EVIL = 0,
    CHAOTIC_NEUTRAL = 1,
    CHAOTIC_GOOD = 2,
    NEUTRAL_EVIL = 3,
    TRUE_NEUTRAL = 4,
    NEUTRAL_GOOD = 5,
    LAWFUL_EVIL = 6,
    LAWFUL_NEUTRAL = 7,
    LAWFUL_GOOD = 8,
    NONE = 9

class DamageType(Enum):
    PIERCE = 0,
    BLUDGEON = 1,
    SLASH = 2

def die_roll(die_formula):
    """
    Simulates a die roll.
    Can receive a string containing the die size and quantity of dice to roll:
        - 2d6 will roll two 1d6 and add both.
        - 1d6 will only roll a die...
        - 3d12 would roll 3 12 sided dice and add the roll.
    :param die_formula: How many dice of x side to roll
    :return: the dice sum
    """
    die_formula.lower()

    # Find the letter d index...
    dice_index = die_formula.find('d')
    if dice_index == -1:
        raise Exception("La formule pour définir le dé est incorrect. Utilisez, par exemple, 1d6 ou 10D10")

    # Do we have only 1 d? If not, raise exception
    number_of_letters = sum(ch.isalpha() for ch in die_formula)
    if number_of_letters > 1:
        raise Exception("La formule pour définir le dé est incorrect. Utilisez, par exemple, 1d6 ou 10D10")

    number_of_dice = int(die_formula[0:dice_index])
    die_size = int(die_formula[dice_index+1:])
    die_sum = 0

    for x in range(number_of_dice):
        die_sum += random.randint(1, die_size)

    return die_sum

class NPC:
    """
    Super class for all NPC's and player. Contains the basic stats for a character in D&D.
    """
    def __init__(self, strength, dex, con, intelligence, wis, cha):
        self.strength = strength
        self.dexterity = dex
        self.constitution = con
        self.intelligence = intelligence
        self.wisdom = wis
        self.charisma = cha

        self.race = ""
        self.species = ""
        self.hit_point = 0
        self.alignment = Alignment.NONE
        self.profession = ""

class Kobold(NPC):
    def __init__(self, profession):
        super().__init__(
            strength = die_roll("3d6") - 2,
            dex = die_roll("3d6") + 2,
            con = die_roll("3d6") - 1,
            intelligence = die_roll("3d6") - 1,
            wis = die_roll("3d6") - 2,
            cha = die_roll("3d6") - 1
        )
        self.race = "Kobold"
        self.species = "Humanoid"
        self.hit_point = die_roll("2d6") - 2
        self.alignment = Alignment.LAWFUL_EVIL
        self.profession = profession  # On ne peut pas mettre le nom class comme attribut.

    def attack(self, ranged=False):
        """
        TODO: Should use damage type as range attacks are pierce versus bludgeon for the sling.
        :param ranged: Are we attacking with a ranged weapon?
        :return: Tuple (DamageType, damage done)
        """
        if not ranged:
            return DamageType.PIERCE, die_roll("1d4") + 2
        else:
            return DamageType.BLUDGEON, die_roll("1d4") + 2

kobold_warrior = Kobold("Warrior")
kobold_inventor = Kobold("Inventor")

damage = kobold_warrior.attack()
print(f"Kobold warrior hits the player for {damage[1]} point(s) of damage. Damage was {damage[0]}")

print(f"The constitution score of the kobold {kobold_warrior.profession} is {kobold_warrior.constitution}")
print(f"The constitution score of the kobold {kobold_inventor.profession} is {kobold_inventor.constitution}")