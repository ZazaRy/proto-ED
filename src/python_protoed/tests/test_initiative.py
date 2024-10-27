from ..core.initiative import *
from ..core.character import Combatant
import unittest

import unittest

class TestInitiative(unittest.TestCase):
    def test_initialization(self):
        a = Combatant(hp=20, ac=14, attackRoll=5, id=1,damage=10, name="Warrior")
        b = Combatant(hp=20, ac=14, attackRoll=5, id=1,damage=10,  name="Goblin")
        c = Combatant(hp=20, ac=14, attackRoll=5, id=2,damage=10, name="Archer")
        d = Combatant(hp=20, ac=14, attackRoll=5, id=2,damage=10, name="Goblin Archer")
        teams = [a,b,c,d]
        t = Teams()
        tracker = t.addToTracker(teams)

        for comb in teams:
            self.assertGreater(comb.initiative, 0)
if __name__ == "__main__":
    unittest.main()

