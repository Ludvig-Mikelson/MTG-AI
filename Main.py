# tests

def legal_actions(GameState):
    
    land_actions = []
    play_creature_actions = []
    
    if GameState.phase == "main phase 1":
        
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
            })
            
        # play creature actions
        creatures_hand = [creature for creature in hand_playable if isinstance(creature, CreatureCard)]
        
        for creature in creatures_hand:
            play_creature_actions.append({
                "id": creature.id,
                "name": creature.name,
            })        
    
    return land_actions,play_creature_actions



        
            