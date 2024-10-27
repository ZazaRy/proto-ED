from core import initiative as init
from core.dice import *
from core.character import *






def main():
    combat_logger = ConsoleCombatLogger()
    t = init.Teams()
    warrior = Combatant(hp=33, ac=14, attackRoll=5, id=1, damage=5, name="Warrior", primary="str", logger=combat_logger)
    mage = Mage(hp=33, ac=14, attackRoll=2, id=1, damage=5, name="Mage", primary="int", logger=combat_logger)
    gob_mage = Mage(hp=33, ac=14, attackRoll=2, id=2, damage=5, name="Goblin Mage", primary="int", logger=combat_logger)
    goblin = Combatant(hp=33, ac=14, attackRoll=5, id=2, damage=5,  name="Goblin", primary="str", logger=combat_logger)
    archer = Combatant(hp=33, ac=14, attackRoll=5, id=1, damage=5, name="Archer", primary="dex",  logger=combat_logger)
    gob_archer = Combatant(hp=13, ac=14, attackRoll=5, id=2, damage=5, name="Goblin Archer", primary="dex", logger=combat_logger)
    teams = [warrior,goblin, archer, gob_archer, mage, gob_mage]
    t.addToTracker(teams)
    t.splitTeams()
    tcTrack = t.autoIncrementTrackers
    status = t.status
    while True:
        attacker = t.getNext()
        if attacker.hp < 1:
            tcTrack()
            continue
        defender = t.pick_random(attacker.id)
        if defender is None:
            print(f"No valid targets. Combat is over. Team {attacker.id} wins")

        tcTrack()
        if isinstance(attacker, Mage):
            attacker.spellAttack(defender)
        elif isinstance(attacker, Combatant):
            attacker.Attack(defender)
        if not t.areAlive(1) or not t.areAlive(2):
            print(f"Combat is over")
            break




if __name__ == "__main__":
    main()