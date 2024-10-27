import unittest
from core.character import Combatant


class TestCharacter(unittest.TestCase):
    def test_initialization(self):
        c = Combatant(hp=100, ac=10, attackRoll=10, id=1, damage=10, name='unknown')
        d = Combatant(hp=100, ac=10, attackRoll=10, id=2, damage=10, name='unknown')
        self.assertEqual(c.name, 'unknown')
        self.assertEqual(c.hp, 100)
        self.assertEqual(c.ac, 10)
        self.assertEqual(c.attackRoll, 10)
        self.assertEqual(c.damage, 10)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
