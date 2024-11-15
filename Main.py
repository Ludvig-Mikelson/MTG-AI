# tests

def legal_actions(GameState, instant_to_target = []):
    
    land_actions = []
    play_creature_actions = []
    play_instant_actions = []
    
    instant_tt = instant_to_target
    
    if instant_tt:
        # 
        g=1
    
    elif GameState.phase == "main phase 1":
        
        player = GameState.player  
        hand = player.hand 
        hand_playable = [card for card in hand if card.mana_cost <= player.mana_pool]    
         
        # land actions
        lands = player.land_board
        untapped_lands = [land for land in lands if land.tapped == False]
        
        for land in untapped_lands:
            land_actions.append({
                "id": land.id,
                "name": land.name,
                "tap": land.tap(player)
            })
            
        # play creature actions
        creatures_hand = [creature for creature in hand_playable if isinstance(creature, CreatureCard)]
        
        for creature in creatures_hand:
            play_creature_actions.append({
                "id": creature.id,
                "name": creature.name,
                "play": creature.play(player)
            })
            
            
            
        # For cards that require choice, create a half action append it to half action list and make so that legal action function
        # locks all actions that are not half action if there is anything inside the half action set.      
        
        instants_hand = [instant for instant in hand_playable if isinstance(instant, InstantCard)]  
        
        for instant in instants_hand:
            
            play_instant_actions.append({
                "id": instant.id,
                "name": instant.name,
                "play": instant.play(player)
            })            
            
    
    return land_actions,play_creature_actions


# Choose action, opponent has abillity to choose an action, you have an opportunity to choose an action, loop like that untill both
# players choose to not make an action in a row. then resolve the actions in the order they were made. 

def stack(GameState,action,stack_list = []):
    
    stack_list.append(action)



# Once the actions resolve, move the loop towards the next phase or sub phase, and set the playerAP to have the priority
# Switch AP/NAP at end phase
# Loop like this untill one of the players life goes to 0 or bellow or a card is drawn when deck is empty.


        
            