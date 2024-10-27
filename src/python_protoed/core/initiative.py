from dataclasses import dataclass, field
from random import randint as rand
from typing import List, DefaultDict, Dict
from collections import defaultdict
from .character import Combatant


@dataclass
class Teams:
    round: int = 0
    turn: int = 0
    order: List[Combatant] = field(default_factory=list)
    round_status: DefaultDict[str,str] = field(default_factory=lambda: defaultdict(str))

    def __post_init__(self):
        for comb in self.order:
            self.round_status[comb.name] = "alive"

    def autoIncrementTrackers(self):
        self.turn += 1
        if self.turn % len(self.order) == 0:
            self.round += 1
            self.turn = 1

    def splitTeams(self):
        self.team_one = [comb for comb in self.order if comb.id ==1]
        self.team_two = [comb for comb in self.order if comb.id ==2]

    def addToTracker(self, teams: list):
        for comb in teams:
            comb.rollInitiative()
            self.round_status[comb.name] = "alive"
        sorted_teams = sorted(teams, key=lambda comb: comb.initiative, reverse=True)
        self.order = sorted_teams

    def status(self):
        print("\n=== Turn Status Board ===")
        print(f"Round: {self.round}, Turn: {self.turn % len(self.order) + 1}")
        for comb in self.order:
            status = "alive" if comb.isAlive() else "dead"
            self.round_status[comb.name] = status
            print(f"{comb.name} (Team {comb.id}):")
            print(f"  Status: {status}")
            print(f"  HP: {comb.hp}")
            print(f"  AC: {comb.ac}")
            print(f"  Attack Roll: {comb.attackRoll}")
            print(f"  Damage: {comb.damage}")
            print(f"  Initiative: {comb.initiative}\n")
            if status == "dead":
                print(f"**** {comb.name} has been defeated! ***\n")
        print("=== End of Turn ===\n")


    def getNext(self)->Combatant:
        return self.order[(self.turn) % len(self.order)]

    def areAlive(self, id: int):
        self.alive_team_one = any(comb.isAlive() for comb in self.team_one)
        self.alive_team_two = any(comb.isAlive() for comb in self.team_two)
        return self.alive_team_one if id == 1 else self.alive_team_two

    def pick_random(self, id):
        pick_from = []
        if id == 1:
            pick_from = [comb for comb in self.order if comb.isAlive() and comb.id==2]
        if id == 2:
            pick_from = [comb for comb in self.order if comb.isAlive() and comb.id==1]
        if not pick_from:
            return None
        comb_index = rand(1,len(pick_from))
        return pick_from[comb_index-1]




