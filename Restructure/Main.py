# %% 

import random
import Classes as cs
import Effects as ef
import Card_Registry as cr
import Engine as en

# adjust legal action functions to include the actions themselves not string

def play_creature_legal_actions(player_s, actions):
        # Add creature actions
    for creature in player_s.hand:
        if isinstance(creature, cs.CreatureCard) and creature.mana_cost <= player_s.mana_pool:
            actions.append({
                "type": "creature",
                "id": creature.id,
                "name": creature.name,
                "player": player_s,
                "target": None,
                "action": creature.play,
                "cost": creature.mana_cost
            })


def play_instant_legal_actions(player_s, actions):
        # Add instant actions
    for instant in player_s.hand:
        if isinstance(instant, cs.InstantCard) and instant.mana_cost <= player_s.mana_pool:
            actions.append({
                "type": "instant",
                "id": instant.id,
                "name": instant.name,
                "player": player_s,
                "target": None,
                "action": instant.play,
                "cost": instant.mana_cost
            })

def play_land_legal_actions(player_s, actions):
    
    for land in player_s.hand:
        if isinstance(land, cs.LandCard) and player_s.played_land == False:
            actions.append({
                "type": "land",
                "id": land,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": land.play,
                "cost": 0
            })
            
def tap_land_legal_actions(player_s, actions):
        # Add tap land actions
    for land in player_s.land_board:
        if not land.tapped:
            actions.append({
                "type": "tap land",
                "id": land.id,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": land.tap,
                "cost": 0
            })
            
def target_instant_legal_actions(player_s, player_ns, instant_to_target, actions):
    
    if instant_to_target:
        for target in [player_ns, player_s] + player_ns.board + player_s.board:
            actions.append({
                "type": "instant",
                "id": instant_to_target["id"],  
                "name": instant_to_target["name"],
                "player": instant_to_target["player"],
                "target": target,
                "action": instant_to_target["action"],
                "cost": instant_to_target["cost"] 
                })
    return actions

def attack_legal_actions(player_AP,actions):
    
    creatures = player_AP.board
    for creature in creatures:
        if creature.tapped == False and creature.attacking == False:
            actions.append({
                "type": "attack",
                "id": creature.id,  
                "name": creature.name,
                "player": player_AP,
                "target": None,
                "action": creature.attack,
                "cost": 0
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
                        "id": creature_blk.id,  
                        "name": creature_blk.name,
                        "player": player_NAP,
                        "target": creature_atk,
                        "action": creature_atk.block,
                        "cost": 0 
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
    
    if phase == "main phase 1" or phase == "main phase 2":
        
        if player_s == player_ap:
            # tap land actions
            tap_land_legal_actions(player_s, actions)

            # play land actions
            play_land_legal_actions(player_s, actions)
            
            # play creature actions
            play_creature_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, actions)
            
        elif player_s == player_nap:
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            # play instant actions
            play_instant_legal_actions(player_s, actions)
            
        
    elif phase == "declare attack phase":
        
        if player_s == player_ap:
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, actions)
            
            # declare attack actions
            attack_legal_actions(player_ap, actions)
            
        elif player_s == player_nap:
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            # play instant actions
            play_instant_legal_actions(player_s, actions)
    
    elif phase == "declare block phase":
        
        if player_s == player_ap:
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, actions)
            
        elif player_s == player_nap:
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
        
    elif phase == "just attacks":
        
        # declare attack actions
        attack_legal_actions(player_ap, actions)
        
    elif phase == "after attack":
        # tap land actions
        tap_land_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        
    elif phase == "just blocks":
        
        # declare block actions
        block_legal_actions(player_ap, actions)
        
    elif phase == "after block":
        # tap land actions
        tap_land_legal_actions(player_s, actions)
        
        # play instant actions
        play_instant_legal_actions(player_s, actions)
        
        
        
        
        

    return actions
            
            
            
def choose_action(actions, GameState):
    print("Choose Action")
    
    # If there are any actions that can be made randomly choose to take random action or not
    print(f"{GameState.player_S.name}'s priority")
    if actions:
        action = random.choice(actions)
        
        # If the action is an instant choose the target first
        if action["type"] == "Instant":
            if action.target == None:
                actions = legal_actions(GameState, instant_to_target=action)
                action = random.choice(actions)
                
            
        # Once the first attack declaration is made, only attack declarations can be made    
        elif action["type"] == "attack" and GameState.player_AP.passed == False:
            action["action"](action["player"])
            GameState.phase = "just attacks"
            action = None
            
        # Same but for blocks 
        elif action["type"] == "block" and GameState.player_NAP.passed == False:
            action["action"](action["player"]) # adjust for actual declare block function
            GameState.phase = "just blocks"
            action = None
            
        elif action["type"] == "land":
            GameState.player_S.played_land = True
            action["id"].tapped = True
            
        GameState.player_S.passed = False
        GameState.player_S.mana_pool -= action["cost"]
        
        print(f"{action["player"].name}, {action["type"]}")
        
        #print(GameState.phase)
        
        if action != None:
            GameState.stack.append(action)
    
            
            
    # If the player choosing to attack or block doesn't, move to after phase where no blcoks or attacks can be declared      
    elif GameState.phase == "just attacks":
        GameState.phase = "after attack"
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
        GameState.reset_prio = True
        
    elif GameState.phase == "just blocks":
        GameState.phase = "after block"
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
        GameState.reset_prio = True

    
        
    else:
        GameState.player_S.passed = True
        print(f"{GameState.player_S.name} passed")
        
 
    
def execute_stack(GameState):
    print("Execute Stack")
    stack = list(reversed(GameState.stack))
    
    print(stack)
    for action in stack:
        
        if action["target"] is not None:
        
            print(action["action"])
            action["action"](action["player"], action["target"])
        else:
        
            action["action"](action["player"])
            
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP
    GameState.stack = []
        

def change_phase(GameState):
    print("Change Phase")
    
    current_phase = GameState.phase
    en.phase_actions[current_phase](GameState)
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP


def add_to_stack(GameState):
    print("Add to Stack")
    actions = legal_actions(GameState)
    action = choose_action(actions, GameState)
    if action:
        GameState.stack.append(action) 
    
    
def main_action(GameState):
    print("Main Action")
    
    add_to_stack(GameState)
    
    # Execute stack if both players passed and there is anything to execute    
    if GameState.stack and GameState.player_AP.passed and GameState.player_NAP.passed:
        print("Execute stack if both players passed")

        execute_stack(GameState)
    
    # Change phase if no stack and both players pass        
    elif not GameState.stack and GameState.player_AP.passed and GameState.player_NAP.passed:
        print("Change Phase if both players passes and no actions")

        change_phase(GameState)
    
    # Keep prio on attacker or blocker during the just attacks/blocks phase 
    elif GameState.reset_prio == True:
        print("gamestate prio is reset")

        GameState.player_S = GameState.player_AP
        GameState.player_NS = GameState.player_NAP
        GameState.reset_prio = False
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
    
    # Switch between player adding to the stack
    else:

        print("Prio is switched")
    
        GameState.player_S_copy = GameState.player_NS
        GameState.player_NS_copy = GameState.player_S

        GameState.player_S = GameState.player_S_copy
        GameState.player_NS = GameState.player_NS_copy

        
player1 = en.player1
player2 = en.player2

state = cs.GameState(player_AP=player1,player_NAP=player2,stack=[])



for _ in range(1,100):
    main_action(state)
    
    
    

# Once the actions resolve, move the loop towards the next phase or sub phase, and set the playerAP to have the priority
# Switch AP/NAP at end phase
# Loop like this untill one of the players life goes to 0 or bellow or a card is drawn when deck is empty.


        
            