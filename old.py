"""
def play_card(player:Player,card:CreatureCard,state:GameState):
    if state.phase == "Main Phase 1":
        if player.mana_pool >= card.mana_cost:
            print(f"{player.name} plays {card.name}")
            player.board.append(card)
            player.hand.remove(card)
            player.mana_pool -= card.mana_cost
            
            card.activate_effects(player)
        else:
            print(f"Not enough mana to play {card.name}")
    else:
        print("Cannot play creature outside Main Phase")
        
        
        
"""        