# %% 
import Classes as cs
import Effects as ef
import Card_Registry as cr
import random





        
    
def build_random_deck(deck_size=60):
    card_names = list(cr.Creature_Card_Registry.keys())  
    land_card_names = list(cr.Land_Card_Registry.keys())
    sorcery_card_names = list(cr.Instant_Card_Registry.keys())
    deck = []
    
    for _ in range((deck_size-30)):
        card_name = random.choice(card_names)  # Randomly select a card name
        card = cr.card_factory(card_name,"Creature")  # Create a unique instance of the card
        deck.append(card)  # Add the card to the deck
       
    for _ in range(20):
        land_card_name = random.choice(land_card_names)  
        card = cr.card_factory(land_card_name,"Land")  
        deck.append(card) 
        
    for _ in range(10):
        sorcery_card_name = random.choice(sorcery_card_names)  
        card = cr.card_factory(sorcery_card_name,"Instant")  
        deck.append(card)         
    
    random.shuffle(deck)

    return deck
    
    
def draw_card(player):
    if len(player.deck) > 0:
        player.hand.append(player.deck.pop())     
    else:
        print("No more cards")
    hand=[]
    for card in player.hand:
        hand.append(card.name)
    print(player.name,"'s hand: ", hand)
        
def next_turn(state:cs.GameState):
    state.turn += 1
    
def begin_phase(state:cs.GameState):
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0    
    state.phase = "begin phase"
    state.player_AP.played_land = False
    for land in state.player_AP.land_board:
        land.tapped = False
    for creature in state.player_AP.board:
        creature.tapped = False
    
    draw_card(state.player_AP)
    print("Begin Phase")

    
def main_phase_1(state:cs.GameState):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    
    state.phase = "main phase 1"
    print(f"{state.player_AP.name} Main Phase 1")
    
def attack_phase(state:cs.GameState):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    
    state.phase = "declare attack phase"
    print(f"{state.player_AP.name} declare attack phase")
    
def block_phase(state:cs.GameState):
    
    state.phase = "declare block phase"
    print(f"{state.player_AP.name} declare block phase")    
    
def resolve_phase(state:cs.GameState):
    
    state.phase = "resolve battle phase"
    print(f"{state.player_AP.name} resolve battle phase")  
    
                
def main_phase_2(state:cs.GameState):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0

    state.phase = "main phase 2"
    print(f"{state.player_AP.name} Main Phase 2")
    
        
        
def battle_phase(player_atk:cs.Player,player_def:cs.Player):
    
    for creature in player_atk.board:
        if creature.tapped == False:
            if random.choice([1,1]) == 1:
                creature.attacking = True
                creature.tapped = True
                print(f"{creature.power}/{creature.toughness} {creature.name} is attacking {player_def.name}")
        
    attackers = [creature for creature in player_atk.board if creature.attacking is True]
    n=0
    attack_block_set = []
    if attackers:
        for blocker in player_def.board:
            if random.choice([1,2]) == 1:
                to_block = random.choice(attackers)
                blocker.blocked_creature_id = to_block.id
                
            
        for attacker in attackers:
            blockers = [blocker for blocker in player_def.board if blocker.blocked_creature_id == attacker.id]
            if blockers:
                for blocker in blockers:
                    if blocker.power <= 0:
                        blocker.power = 0
                    if attacker.power <= 0:
                        attacker.power = 0
                    print(f"{blocker.power}/{blocker.toughness} {blocker.name} is blocking {attacker.power}/{attacker.toughness} {attacker.name}")

                    bt = blocker.toughness
                    ap = attacker.power
                    bp = blocker.power
                    
                    blocker.toughness -= ap
                    attacker.toughness -= bp
                    attacker.power -= bt
            else:
                print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals damage to the {player_def.name}.")
                player_def.life -= attacker.power
                print(f"{player_def.name} has {player_def.life} life left")
                
        dead_creatures_atk = [creature.id for creature in player_atk.board if creature.toughness <= 0]
        for dead_creature_id in dead_creatures_atk:   
            dead_creature = next((creature for creature in player_atk.board if creature.id == dead_creature_id), None)
            if dead_creature:
                dead_creature.leaves_battlefield(player_atk, player_def)
                
        dead_creatures_def = [creature.id for creature in player_def.board if creature.toughness <= 0]
        for dead_creature_id in dead_creatures_def:   
            dead_creature = next((creature for creature in player_def.board if creature.id == dead_creature_id), None)
            if dead_creature:
                dead_creature.leaves_battlefield(player_def, player_atk)
            

    
def reset_creatures(player: cs.Player):
    # Reset creatures on the player's board
    for creature in player.board:
        if isinstance(creature,cs.CreatureCard):
            creature.power = creature.og_power + creature.counter_power
            creature.toughness = creature.og_toughness + creature.counter_toughness
            creature.attacking = False
            creature.blocking = False 
            creature.blocked_creature_id = None
            creature.spell_targeted = False

    # Reset creatures in the player's graveyard
    for creature in player.graveyard:
        if isinstance(creature,cs.CreatureCard):
            creature.power = creature.og_power
            creature.toughness = creature.og_toughness
            creature.attacking = False
            creature.blocking = False
            creature.blocked_creature_id = None
            
def end_phase(playerAP:cs.Player,playerNAP:cs.Player,state:cs.GameState):
    state.phase = "end phase"
    reset_creatures(playerAP)
    reset_creatures(playerNAP)
    
    next_turn(state)
    
    
    

phase_actions = {
    "first phase": begin_phase,
    "begin phase": main_phase_1,
    "main phase 1": attack_phase,
    "declare attack phase": block_phase,
    "after attack": block_phase,
    "declare block phase": resolve_phase,
    "after block": resolve_phase,
    "resolve battle phase": main_phase_2,
    "main phase 2": end_phase,
    "end phase": begin_phase
}






deck1 = build_random_deck()
deck2 = build_random_deck()
start_hand1 = deck1[:7]
start_hand2 = deck2[:7]
deck1 = deck1[7:]
deck2 = deck2[7:]
    
player1 = cs.Player("Bob", start_hand1, deck1, [], [], [], 0, 20)
player2 = cs.Player("Alice", start_hand2, deck2, [], [], [], 0, 20)
players = [player1, player2]


    
    

        
    