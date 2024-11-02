from core import initiative as init
from core.character import *
import numba
import numpy





def main():
    t = init.Teams()
    # t.addToTracker()
    t.splitTeams()
    tcTrack = t.autoIncrementTrackers
    status = t.status
    dummy = Combatant(hp=1000, ac=18, attackRoll=0, id=0, damage_mod=0, weapon_type=DAGGER, name="Passive Dummy", primary=STR)

    chris = Combatant(hp=100, ac=16, attackRoll=10, attacks=3, id=0, damage_mod=5, pb=5, weapon_type=QSTAFF_MAST, name="Chris", primary=STR, statblock=Stats(3, 3, 2, 0, 0, 0))

    accum = 0
    round = 0
    summing = 0

    # Flag to track first round for Shillelagh
    first_round = True

    while dummy.isAlive():
        round += 1
        print(f"=== ROUND {round} ===")
        accum = 0
        chris.reset_attacks()
        print(f"Number of attacks left {chris.current_attacks}")

        # Pass first_round only in the first round, then set to False
        accum += chris.champion_tactic(dummy, first_round=first_round)
        first_round = False  # After first round, Shillelagh won't be cast again

        print(f"Damage this round: {accum}")
        dummy.clear_conditions()
        summing += accum

    print(f"DPR for this fight is {summing/round}")




if __name__ == "__main__":
    main()
