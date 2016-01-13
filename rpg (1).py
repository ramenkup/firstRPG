import random
'''
This class simulates Advanced Dnd combat between two fighter characters.
Initiation is rolled for, followed by roll to hit, followed by a damage roll.
Combat is looped round by round until one of the characters dies, upon which
a report is output.
'''
class Fighter:
    '''
    def __init__(Obj, str):
    Initialize a Fighter object. gives a unique name(str) 
    and 10 hit points(int).
    '''
    def __init__(self, name):
        self.name=name
        self.hit_points=10
    '''
    def __repr__(Obj):
    returns a textual representation of a fighter and his current HP
    '''   
    def __repr__(self):
        returner= self.name+ ' (HP: '+ str(self.hit_points) + ')'#do i have to ref self?
        return returner
    '''
    def take_damage(Obj, int)
        This method applies damage to a Fighter object by subtracting
        from their hit points, then outputting the damage / if the Fighter
        has fallen.
    '''
    def take_damage(self, damage_amount):
        self.hit_points-= damage_amount
        if self.hit_points <= 0:
            print ('\t'+'Alas,', self.name, 'has fallen!')
        else:
            print ('\t'+self.name,'has', self.hit_points,'hit points remaining.')
        return None
    '''
    def attack(Obj,Obj):
    runs the combat sequence of the two fighters. It prints who is attacking
    who. Next it rolls to hit (>=12 to hit). upon a successful hit, it rolls
    for damage(1-6). it calls take_damage to apply the damage to the Fighter.
    '''
    def attack(self, other):
        print (self.name, 'attacks', other.name+'!')
        roll_to_hit= random.randrange(1,21)
        if roll_to_hit >=12:
            dmg_roll= random.randrange(1,7)
            print('\t'+'Hits for',dmg_roll,'hit points!')
            other.take_damage(dmg_roll)
        else:
            print('\t'+'Misses!')
        return None
    '''
    def is_alive(Obj):
    checks the hit points of the fighter to see if they are still alive.
    returns Boolean
    '''
    def is_alive(self):
        if self.hit_points > 0:
            return True
        return False
'''
def combat_round(Obj, Obj):
Rolls for initiation. if the same value, targets attack simultaneously.
The result is always output.
'''
def combat_round(P1, P2):
    P1_roll= random.randrange(1,7)
    P2_roll= random.randrange(1,7)
    if P1_roll == P2_roll:
        print('Simultaneous!')
        P1.attack(P2)
        P2.attack(P1)
    else:
        if P1_roll > P2_roll:
            P1.attack(P2)
            if P2.is_alive():
                P2.attack(P1)
        elif P2_roll > P1_roll:
            P2.attack(P1)
            if P1.is_alive():
                P1.attack(P2)
    return None
'''
def main():
main loops rounds of combats until at least one of the Fighters dies, each
round is headered with the round number, and pause-promts the user to begin
the fight. Outputs each players HP status until one of them dies, where upon
death, 'The battle is over!' is output, followed by the player representation.
'''
def main():
    Rich= Fighter('Rich')
    Thompson= Fighter('Thompson')
    round_count=1
    while Rich.is_alive() and Thompson.is_alive():
        print('\n'+'===================','ROUND',round_count,'===================')
        print(Rich)
        print(Thompson)
        input('Enter to Fight!')
        combat_round(Rich,Thompson)
        round_count+=1
    print('\n'+"The battle is over!")
    print(Rich)
    print(Thompson)

if __name__ == '__main__':
    main()