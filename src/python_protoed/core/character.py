from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, DefaultDict, Dict, Any, Tuple, Optional
from zope.interface import Interface, implementer, invariant, Attribute
from zope.interface.verify import verifyObject
from .dice import *

MOVE = 1 << 0
ATTACK = 1 << 1
CAST_SPELL = 1 << 2
TAKE_DAMAGE = 1 << 3

from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List, Tuple

class ICombatLogger(Interface):
    """Interface for a combat logger that logs events during combat."""

    log = Attribute("A nested dictionary to store combat events")

    def log_event(event_type: int, message: str, round_number: int, turn_number: int):
        """Logs an event in the combat logger with the given details."""

    def display_log(filter_flags: int):
        """Displays the log based on provided filter flags."""

    @invariant
    def validate_log_structure(self):
        """Invariant to ensure 'log' is a properly structured dictionary."""
        assert isinstance(self.log, dict), "'log' must be a dictionary structure"


@implementer(ICombatLogger)
@dataclass
class ConsoleCombatLogger:
    log: DefaultDict = field(default_factory=lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str))))

    def log_event(self, event_type: int, message: str, round_number: int, turn_number: int):
        self.log[event_type][round_number][turn_number] = message

    def display_log(self, filter_flags: int = 0b1110):
        print("=== Combat Log ===")

        for round_number, turns in sorted(self.log.items()):
            for k, v in turns.items():
                print(round_number, k,v)

        print("=== End of Combat Log ===\n")

@dataclass
class StatBlock:
    stre: int
    con: int
    dex: int
    inte: int
    wis: int
    cha: int

@dataclass
class Combatant:
    hp: int
    ac: int
    attackRoll: int
    damage: int
    name: str
    id: int
    logger: ICombatLogger
    primary: str
    primary_value: int = 0
    pb: int = 0
    dc: int = 0
    statblock: StatBlock = field(default_factory=lambda: StatBlock(stre=10,con=10,dex=10,inte=10,wis=10,cha=10))
    initiative: int = 0


    def __post_init__(self):
        if self.primary == "str":
            self.primary_value = self.statblock.stre
            self.dc = 8 + self.pb + self.statblock.stre
        elif self.primary == "con":
            self.primary_value = self.statblock.con
            self.dc = 8 + self.pb + self.statblock.con
        elif self.primary == "dex":
            self.primary_value = self.statblock.dex
            self.dc = 8 + self.pb + self.statblock.dex
        elif self.primary == "int":
            self.primary_value = self.statblock.inte
            self.dc = 8 + self.pb + self.statblock.inte
        elif self.primary == "wis":
            self.primary_value = self.statblock.wis
            self.dc = 8 + self.pb + self.statblock.wis
        elif self.primary == "cha":
            self.primary_value = self.statblock.cha
            self.dc = 8 + self.pb + self.statblock.cha
        else:
            print("Invalid Primary Stat Name")

    def Attack(self, target: "Combatant"):
        roll_to_hit = roll_d20() + self.attackRoll
        assert self.hp > 0, "Cannot attack when dead"
        assert self.name != target.name, f"{self.name} cannot attack {target.name}"
        if roll_to_hit >= target.ac:
            damage = roll_d8() + self.damage
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} and hits for {damage} damage.")
        else:
            print(f"{self.name} attacks {target.name} but misses")

    def take_damage(self, damage: int):
        self.hp = max(0, self.hp - damage)
        print(f"{self.name} takes {damage} damage, HP is now {self.hp}.")

        if self.hp <= 0:
            print(f"{self.name} has been defeated!")

    def rollInitiative(self):
        self.initiative = roll_d20() + self.statblock.dex
        print(f"{self.name} rolls initiative: {self.initiative}.")

    def isAlive(self):
        return self.hp > 0


@dataclass
class Spell:
    level: int
    damage: int
    name: str
    castTime: int

@dataclass
class AttackSpell:
    spell: Spell
    tag: int = 0

@dataclass
class SaveSpell:
    spell: Spell
    tag: int = 1

@dataclass
class SpellList:
    attack: List[AttackSpell] = field(default_factory=List)
    saves: List[SaveSpell] = field(default_factory=List)



@dataclass
class Mage(Combatant):
    spellList: SpellList = field(init=False)

    def __post_init__(self):
        fire_bolt = AttackSpell(spell=Spell(level=0,damage=10,name="Fire Bolt", castTime=1))
        toll_the_dead = SaveSpell(spell=Spell(level=0,damage=12,name="Toll the Dead", castTime=1))
        ray_of_frost = AttackSpell(spell=Spell(level=0,damage=8,name="Ray of Frost", castTime=1))
        self.spellList = SpellList(attack=[fire_bolt,ray_of_frost], saves=[toll_the_dead])



    def spellAttack(self, target):
        spell = self.random_attack_spell_picker()
        roll_to_hit = roll_d20() + self.primary_value + self.pb
        if roll_to_hit >= target.ac:
            damage = rand(1,spell.spell.damage)
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} with {spell.spell.name} and hits for {damage} damage.")
        else:
            print(f"{self.name} misses against {target.name}. It rolled {roll_to_hit} and {target.name} has {target.ac} AC")


    def random_attack_spell_picker(self) -> AttackSpell:
        index = rand(0,len(self.spellList.attack)-1)
        picked = self.spellList.attack[index]
        return picked

