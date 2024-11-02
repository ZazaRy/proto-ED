from .dice import zig_roll as roll





def dagger_basic(target, dmg, crit=None):
    target.hp -= dmg

def dagger_mastery(target, dmg, crit=None):
    target.hp -= dmg

def qstaff_basic(target, dmg) -> int:
    dmg += roll(1,8)
    target.hp -= dmg
    print(f"Basic Quarterstaff attack for {dmg} on {target.name}. HP left {target.hp}")
    if target.hp < 0:
        print(f"{target.name} has been defeated")
    return dmg

def qstaff_mastery(target, dmg, dc, crit=None, two_handed=None):
    if crit:
        if two_handed:
            qstaff_dmg = roll(2,8)
            print(f"Two Handed Crit roll: {qstaff_dmg} modifier is {dmg} total should be {qstaff_dmg+dmg}")
        else:
            qstaff_dmg = roll(2,6)
            print(f"One Handed Crit roll: {qstaff_dmg} modifier is {dmg} total should be {qstaff_dmg+dmg}")
    else:
        if two_handed:
            qstaff_dmg = roll(1,8)
        else:
            qstaff_dmg = roll(1,6)
    dmg += qstaff_dmg
    target.hp -= dmg
    result = target.save(effect="PRONE", dc=dc, save_type="con")
    if not result:
        target.conditions.prone = 1
        print(f"{target.name} failed against prone")
    else:
        target.conditions.prone = 0
        print(f"{target.name} saved against prone")
    return dmg
