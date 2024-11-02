from dataclasses import dataclass, field
from typing import List, Callable
from .dice import zig_roll as roll
from .weap_funcs import *
import random

STR = 1 << 0
CON = 1 << 1
DEX = 1 << 2
INT = 1 << 3
WIS = 1 << 4
CHA = 1 << 5

QUARTERSTAFF = 1 << 0
QSTAFF_MAST = 1 << 1
DAGGER = 1 << 2
DAGGER_MAST = 1 << 3
SCIMITAR = 1 << 4
LONGSWORD = 1 << 5

@dataclass
class AttackResult:
    hit: bool
    damage: int

@dataclass
class Conditions:
    prone: int = 0

@dataclass
class Stats:
    stre: int = 0
    con: int = 0
    dex: int = 0
    inte: int = 0
    wis: int = 0
    cha: int = 0

@dataclass
class Combatant:
    hp: int
    ac: int
    attackRoll: int
    damage_mod: int
    name: str
    id: int
    primary: int
    weapon_type: int
    current_attacks: int = field(init=False)
    heroic_insp: bool = True
    shield_bash: bool = False
    studied_attacks_up: bool = False
    action_surge_up: bool = True
    attacks: int = 1
    weapon: Callable[['Combatant', int], int] = field(init=False)
    pb: int = 2
    conditions: Conditions = field(init=False)
    statblock: Stats = field(default_factory=Stats)
    save_type: Stats = field(default_factory=Stats)
    initiative: int = 0
    primary_value: int = field(init=False)
    dc: int = field(init=False)
    has_shillelagh: bool = False  # Tracks if Shillelagh has been cast

    def __post_init__(self):
        self.primary_value = self.get_primary_value()
        self.dc = 8 + self.pb + self.primary_value
        self.conditions = Conditions()
        self.current_attacks = self.attacks
        weapon_func_map = {
            DAGGER: dagger_basic,
            QUARTERSTAFF: qstaff_basic,
            DAGGER_MAST: dagger_mastery,
            QSTAFF_MAST: qstaff_mastery,
        }
        weapon_function = weapon_func_map.get(self.weapon_type)
        if not weapon_function:
            raise ValueError("Invalid weapon type provided")
        object.__setattr__(self, 'weapon', weapon_function)

    def get_primary_value(self) -> int:
        if self.primary == STR:
            return self.statblock.stre
        elif self.primary == CON:
            return self.statblock.con
        elif self.primary == DEX:
            return self.statblock.dex
        elif self.primary == INT:
            return self.statblock.inte
        elif self.primary == WIS:
            return self.statblock.wis
        elif self.primary == CHA:
            return self.statblock.cha
        else:
            raise ValueError("Invalid primary attribute")

    def perform_attack(self, target: "Combatant", advantage: bool = False, use_shillelagh: bool = False) -> AttackResult:
        """Perform a single attack roll, with optional advantage and critical handling."""
        crit = False
        rolled_to_hit = 0

        if advantage:
            print(f"{self.name} attacks with advantage!")
            first_roll = roll(1, 20)
            second_roll = roll(1, 20)
            rolled_to_hit = max(first_roll + self.attackRoll, second_roll + self.attackRoll)
            crit = first_roll > 19 or second_roll > 19
        else:
            regular_roll = roll(1, 20)
            rolled_to_hit = regular_roll + self.attackRoll
            crit = regular_roll > 19

        # Check if attack hits
        if rolled_to_hit >= target.ac:
            # Use Shillelagh weapon damage if applied
            damage_dealt = self.shillelagh_damage(target, crit) if use_shillelagh else self.weapon(target=target, dmg=self.damage_mod, dc=self.dc, crit=crit, two_handed=False)
            print(f"{self.name} did {damage_dealt} dmg to {target.name}")
            return AttackResult(hit=True, damage=damage_dealt)
        else:
            print(f"{self.name} attacks {target.name} but misses")
            return AttackResult(hit=False, damage=0)

    def shillelagh_damage(self, target, crit=False) -> int:
        """Calculate Shillelagh-enhanced damage based on level scaling."""
        level = self.get_level()  # Assume this method exists or implement character level tracking
        if level >= 17:
            base =  roll(2, 6) + self.damage_mod
            if crit:
                base += roll(2, 6)
            target.hp -= base
            return base
        elif level >= 11:
            base = roll(1, 12) + self.damage_mod
            if crit:
                base += roll(1,12)
            target.hp -= base
            return base
        elif level >= 5:
            base = roll(1, 10) + self.damage_mod
            if crit:
                base+= roll(1,10)
            target.hp -= base
            return base
        else:
            base = roll(1, 8) + self.damage_mod
            if crit:
                base+= roll(1,8)
            target.hp -= base
            return base

    def champion_tactic(self, target: "Combatant", first_round=False) -> int:
        dmg_total = 0
        self.current_attacks = self.attacks  # Set the regular attack count

        # If it's the first round, use Action Surge to get another set of attacks
        if first_round and self.action_surge_up:
            print(f"{self.name} uses Action Surge for additional attacks!")
            self.action_surge_up = False  # Mark Action Surge as used
            self.reset_attacks()  # Reset attacks for the additional action
            dmg_total += self.champion_tactic(target, first_round=False)  # Recursive call for Action Surge attacks

        while self.current_attacks > 0:
            print(f"{self.name} has {self.current_attacks} attacks remaining.")
            
            # Perform the attack with advantage if conditions are met
            advantage = self.heroic_insp or self.studied_attacks_up or target.conditions.prone
            attack_result = self.perform_attack(target, advantage=advantage)
            self.current_attacks -= 1  # Decrement attacks after each attempt

            # Check for hit or miss outcomes
            if not attack_result.hit:
                if self.heroic_insp:
                    print(f"{self.name} uses Heroic Inspiration to reroll!")
                    self.heroic_insp = False
                    attack_result = self.perform_attack(target)  # Reroll without advantage

                if not attack_result.hit:
                    self.studied_attacks_up = True  # Set Studied Attacks for next turn

                # Attempt Shield Bash if target is not prone and we haven't used it yet
                if not target.conditions.prone and not self.shield_bash:
                    self.attempt_shield_bash(target)
            else:
                # Reset Studied Attacks if we hit
                self.studied_attacks_up = False

            # Accumulate damage
            dmg_total += attack_result.damage

        return dmg_total


    def cast_shillelagh(self):
        print(f"{self.name} casts Shillelagh on their weapon.")
        self.has_shillelagh = True

    def attempt_reaction_attack(self, target: "Combatant"):
        """Attempt reaction attack with probabilities for Sentinel + PAM or PAM alone."""
        reaction_roll = random.randint(1, 100)
        if reaction_roll <= 25:
            print(f"{self.name} attempts a PAM reaction attack!")
            return self.perform_attack(target, use_shillelagh=False)
        elif reaction_roll <= 75:
            print(f"{self.name} attempts a Sentinel + PAM reaction attack!")
            return self.perform_attack(target, use_shillelagh=False)
        else:
            print(f"{self.name} does not perform a reaction attack.")
            return None

    def attempt_shield_bash(self, target: "Combatant"):
        print(f"{self.name} attempts a Shield Bash to knock {target.name} prone!")
        self.shield_bash = True
        if not target.save(effect="Shield Bash", dc=self.dc, save_type="str"):
            target.conditions.prone = 1
            print(f"{target.name} is now prone!")
        else:
            print(f"{target.name} resisted the Shield Bash!")

    def save(self, effect, dc: int, save_type: str) -> bool:
        modifier = getattr(self.save_type, save_type, 0)
        roll_result = roll(1, 20) + modifier
        if roll_result >= dc:
            print(f"{self.name} rolled {roll_result}, needed {dc} and saved against {effect}")
            return True
        print(f"{self.name} rolled {roll_result}, needed {dc} and failed against {effect}")
        return False

    def isAlive(self) -> bool:
        return self.hp > 0

    def clear_conditions(self):
        self.conditions.prone = 0

    def reset_attacks(self):
        self.current_attacks = self.attacks

    def get_level(self) -> int:
        return 17

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
        roll_to_hit = roll(1,20) + self.primary_value + self.pb
        if roll_to_hit >= target.ac:
            damage = roll(1,spell.spell.damage)
            target.take_damage(damage)
            print(f"{self.name} attacks {target.name} with {spell.spell.name} and hits for {damage} damage.")
        else:
            print(f"{self.name} misses against {target.name}. It rolled {roll_to_hit} and {target.name} has {target.ac} AC")


    def random_attack_spell_picker(self) -> AttackSpell:
        index = roll(0,len(self.spellList.attack)-1)
        picked = self.spellList.attack[index]
        return picked

