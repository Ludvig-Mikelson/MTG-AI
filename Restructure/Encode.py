

def declare_attack(creature_atk):
    creature_atk.attacking = True
    
def declare_block(creature_atk, creature_def):
    creature_atk.blockers.append(creature_def)
    

def play_instant(instant, player, target):
    instant.play(player, target)
    
def activate_instant(instant, player, target):
    instant.activate(player, target)
    
    