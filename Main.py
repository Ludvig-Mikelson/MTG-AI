# tests
import random

def play_creature_legal_actions(player_s, actions):
        # Add creature actions
    for creature in player_s.hand:
        if isinstance(creature, CreatureCard) and creature.mana_cost <= player_s.mana_pool:
            actions.append({
                "type": "creature",
                "id": creature.id,
                "name": creature.name,
                "player": player_s,
                "target": None,
                "action": "play_creature"
            })


def play_instant_legal_actions(player_s, actions):
        # Add instant actions
    for instant in player_s.hand:
        if isinstance(instant, InstantCard) and instant.mana_cost <= player_s.mana_pool:
            actions.append({
                "type": "instant",
                "id": instant.id,
                "name": instant.name,
                "player": player_s,
                "target": None,
                "action": "choose_target"
            })

def play_land_legal_actions(player_s, actions):
    
    for land in player_s.hand:
        if isinstance(land, LandCard) and player_s.played_land == False:
            actions.append({
                "type": "land",
                "id": land.id,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": "play_land"
            })
            
def tap_land_legal_actions(player_s, actions):
        # Add tap land actions
    for land in player_s.land_board:
        if not land.tapped:
            actions.append({
                "type": "land",
                "id": land.id,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": "tap_land"
            })
            
def target_instant_legal_actions(player_s, player_ns, instant_to_target, actions):
    
    if instant_to_target:
        for target in [player_ns, player_s] + player_ns.board + player_s.board:
            actions.append({
                "type": "instant",
                "id": instant_to_target["id"],  
                "name": instant_to_target["name"],
                "player": player_s,
                "target": target,
                "action": "play_instant" 
                })
    return actions

def attack_legal_actions(player_AP,actions):
    
    creatures = player_AP.board
    for creature in creatures:
        if creature.tapped == False:
            actions.append({
                "type": "attack",
                "id": creature["id"],  
                "name": creature["name"],
                "player": player_AP,
                "target": "self",
                "action": "declare_attack" 
                })
    
def block_legal_actions(player_AP, player_NAP, actions):
    
    creatures_ap = player_AP.board
    creatures_nap = player_NAP.board
    
    for creature_blk in creatures_nap:
        if creature_blk.tapped == False and creature_blk.blocking == False:
            for creature_atk in creatures_ap:
                if creature_atk.attacking == True:
                    actions.append({
                        "type": "block",
                        "id": creature_blk["id"],  
                        "name": creature_blk["name"],
                        "player": player_NAP,
                        "target": creature_atk["id"],
                        "action": "declare_block" 
                        })
    

def legal_actions(GameState, instant_to_target=None):
    actions = []
    player_ns = GameState.player_NS
    player_s = GameState.player_S
    phase = GameState.phase
    player_ap = GameState.player_AP
    player_nap = GameState.player_NAP

    # target instant actions
    if instant_to_target:
        target_instant_legal_actions(player_s, player_ns, instant_to_target, actions)
        return actions
    
    if phase == "main phase 1" or "main phase 2":
        # tap land actions
        tap_land_legal_actions(player_s, actions)

        # play land actions
        play_land_legal_actions(player_s, actions)
        
        # play creature actions
        play_creature_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        
    elif phase == "declare_attack_phase":
        # tap land actions
        tap_land_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        
        # declare attack actions
        attack_legal_actions(player_ap, actions)
    
    elif phase == "declare_block_phase":
        # tap land actions
        tap_land_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        
        # declare block acions
        block_legal_actions(player_ap, player_nap, actions)
        
         
    elif phase == "resolve battle phase":
        # tap land actions
        tap_land_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        

    return actions
            
            
            
        # For cards that require choice, create a half action append it to half action list and make so that legal action function
        # locks all actions that are not half action if there is anything inside the half action set.      
        


# Choose action, opponent has abillity to choose an action, you have an opportunity to choose an action, loop like that untill both
# players choose to not make an action in a row. then resolve the actions in the order they were made. 

def choose_action(actions):
    if actions:
        action = random.choice(actions)
        
        if action.type == "Instant":
            if action.target == None:
                action = legal_actions(GameState, instant_to_target=action)
        
    GameState.stack.append(action)

def execute_stack(GameState):
    stack = GameState.stack.reverse()
    
    for action in stack:
        if action["target"] is None:
            action["action"](None)
        else:
            action["action"](action["target"])
        
    
    

# Once the actions resolve, move the loop towards the next phase or sub phase, and set the playerAP to have the priority
# Switch AP/NAP at end phase
# Loop like this untill one of the players life goes to 0 or bellow or a card is drawn when deck is empty.


        
            