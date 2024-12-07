# %% 
import random
from Card_Registry import card_factory, Creature_Card_Registry,Land_Card_Registry, Card,CreatureCard,LandCard, Player,InstantCard,Instant_Card_Registry, EnchantmentCard, Enchantment_Card_Registry


class GameState:
    def __init__(self, player_AP: Player, player_NAP: Player, player_S: Player, player_NS: Player, 
                 turn: int, phase: str, stack: list):
        self.player_AP = player_AP
        self.player_NAP = player_NAP
        self.player_S = player_S
        self.player_NS = player_NS
        self.turn = turn
        self.stack = stack
        self.phase = phase      

        
class GameState:
    def __init__(self, players: list[Player], turn: int, phase: str):
        self.players = players
        self.turn = turn
        self.phase = phase 
        
        
def print_board(player):
    if len(player.board) == 0:
        print(f"{player.name}'s board is empty.")
    else:
        print(f"{player.name}'s board:")
        for card in player.board:
            print(card)  
        

        
def build_random_deck(deck_size=60):
    card_names = list(Creature_Card_Registry.keys())  
    land_card_names = list(Land_Card_Registry.keys())
    instant_card_names = list(Instant_Card_Registry.keys())
    enchantment_card_names = list(Enchantment_Card_Registry.keys())
    deck = []
    
    for _ in range((deck_size-30)):
        card_name = random.choice(card_names)  # Randomly select a card name
        card = card_factory(card_name,"Creature")  # Create a unique instance of the card
        deck.append(card)  # Add the card to the deck
       
    for _ in range(20):
        land_card_name = random.choice(land_card_names)  
        card = card_factory(land_card_name,"Land")  
        deck.append(card) 
        
    for _ in range(20):
        instant_card_name = random.choice(instant_card_names)  
        card = card_factory(instant_card_name,"Instant")  
        deck.append(card)    

    for _ in range(10):
        enchantment_card_name = random.choice(enchantment_card_names)
        card = card_factory(enchantment_card_name,"Enchantment")  
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
        
def next_turn(state:GameState):
    state.turn += 1
    
def begin(playerAP:Player,playerNAP:Player,state:GameState):
    playerAP.mana_pool = 0
    playerNAP.mana_pool = 0    
    state.phase = "begin phase"
    playerAP.played_land = False
    for land in playerAP.land_board:
        land.tapped = False
    for creature in playerAP.board:
        creature.tapped = False
    
    draw_card(playerAP)

    board=[]
    for card in playerAP.board:
        board.append(card.name)
    print(playerAP.name,"'s board: ", board)


def main_phase(playerAP:Player,playerNAP:Player,state:GameState):
    lands = [card for card in playerAP.hand if isinstance(card, LandCard)]
    if playerAP.played_land == False and len(lands) > 0:
        random.choice(lands).play(playerAP,state)
        playerAP.played_land = True
    
    if len(playerAP.land_board) > 0:
        for land in playerAP.land_board:
            if land.tapped == False:
                land.tap(playerAP)

    # For now, play random card
    ### Creature:
    creatures_hand = [card for card in playerAP.hand if isinstance(card, CreatureCard)]
    instants_hand = [card for card in playerAP.hand if isinstance(card, InstantCard)]
    enchantments_hand = [card for card in playerAP.hand if isinstance(card, EnchantmentCard)]
    if len(creatures_hand) > 0:
        random.choice(creatures_hand).play(playerAP,state)
        
    controlled_creatures = [card for card in playerAP.board if isinstance(card, CreatureCard)]
    enemy_creatures = [card for card in playerNAP.board if isinstance(card, CreatureCard)]
    
    ### Instant:
    if len(instants_hand) > 0:
        target_choices = {"controlled_creatures": controlled_creatures,
                       "enemy_creatures": enemy_creatures,
                       "all_creatures": controlled_creatures + enemy_creatures,
                       "all_enemies": enemy_creatures + [playerNAP],
                       "all_targets": controlled_creatures + enemy_creatures + [playerNAP]
                       }
        print(f"instants hand: {[card.name for card in instants_hand]}")
        chosen_instant = random.choice(instants_hand)
        print(f"name of chosen instant: {chosen_instant.name}")
        chosen_instant.play(playerAP,state,target_choices)

    ### Enchantment:
    if len(enchantments_hand) > 0:
        if len(controlled_creatures) > 0:
            random.choice(enchantments_hand).play(playerAP,state,controlled_creatures)
        else:
            print("Cannot play this Enchantment, no targets.")

    
def main_phase_1(playerAP:Player,playerNAP:Player,state:GameState):
    
    state.phase = "main phase 1"
    print(f"{playerAP.name} Main Phase 1")
    main_phase(playerAP, playerNAP, state)
                    

def main_phase_2(playerAP:Player,playerNAP:Player,state:GameState): 

    # Vajag pagaidām COPY-PASTE no phase-1 :
    state.phase = "main phase 2"
    print(f"{playerAP.name} Main Phase 2")
    main_phase(playerAP, playerNAP, state)
        
        
        
# def battle_phase(player_atk:Player,player_def:Player):
    
#     for creature in player_atk.board:           # Manifold Mouse effect
#         if creature.name == "Manifold Mouse":   
#             buff = random.choice(["trample"])   # UN "double strike" vajag vēl!
#             controlled_mouses = [creature for creature in player_atk.board if creature.is_mouse == True]
#             mouse = random.choice(controlled_mouses)
#             # Valiant effect activation!
#             print(f"Manifold mouse effect gave {buff} to {mouse.name} until EOT.")
        
#             if buff == "trample":
#                 mouse.trample_eot == True
#             elif buff == "double_strike":
#                 pass
        
#     for creature in player_atk.board:
#         if creature.tapped == False:
#             if random.choice([1,1]) == 1:       # Uzbrūk vienmēr ar visiem
#                 creature.attacking = True
#                 creature.tapped = True
#                 print(f"{creature.power}/{creature.toughness} {creature.name} is attacking {player_def.name}")
        
#     attackers = [creature for creature in player_atk.board if creature.attacking is True]
#     n=0
#     attack_block_set = []
#     if attackers:
#         for blocker in player_def.board:
#             if random.choice([1,2]) == 1:
#                 to_block = random.choice(attackers)
#                 if not (to_block.flying==True and blocker.flying==False):   # only 1 out of 4 cases when cannot block
#                     blocker.blocked_creature_id = to_block.id
#                 else:
#                     print(f"Couldn't block, attacker {to_block.name} flying: {to_block.flying}, blocker {blocker.name} flying: {blocker.flying}")
                
            
#         for attacker in attackers:
#             blockers = [blocker for blocker in player_def.board if blocker.blocked_creature_id == attacker.id]
#             if blockers:
#                 if (attacker.menace == True and len(blockers) >= 2) or attacker.menace == False:    # checks menace condition
#                     for blocker in blockers:
#                         if blocker.power <= 0:
#                             blocker.power = 0
#                         if attacker.power <= 0:
#                             attacker.power = 0
#                         print(f"{blocker.power}/{blocker.toughness} {blocker.name} is blocking {attacker.power}/{attacker.toughness} {attacker.name}")

#                         bt = blocker.toughness
#                         ap = attacker.power
#                         bp = blocker.power
                        
#                         blocker.toughness -= ap
#                         attacker.toughness -= bp
#                         attacker.power -= bt

#                     if (attacker.trample==True or attacker.trample_eot==True) and attacker.power>0:    # for remaining power, and doesn't need toughness check?
#                         print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals Trample damage to Player {player_def.name}.")
#                         player_def.life -= attacker.power
#                         print(f"{player_def.name} has {player_def.life} life left")
#                 elif attacker.menace == True and len(blockers) == 1:
#                     print(f"One blocker {blockers[0].name} cannot block {attacker.name} with Menace")
#             else:
#                 print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals damage to Player {player_def.name}.")
#                 player_def.life -= attacker.power
#                 print(f"{player_def.name} has {player_def.life} life left")
                
#         dead_creatures_atk = [creature.id for creature in player_atk.board if creature.toughness <= 0]
#         for dead_creature_id in dead_creatures_atk:   
#             dead_creature = next((creature for creature in player_atk.board if creature.id == dead_creature_id), None)
#             if dead_creature:
#                 dead_creature.leaves_battlefield(player_atk, player_def)
                
#         dead_creatures_def = [creature.id for creature in player_def.board if creature.toughness <= 0]
#         for dead_creature_id in dead_creatures_def:   
#             dead_creature = next((creature for creature in player_def.board if creature.id == dead_creature_id), None)
#             if dead_creature:
#                 dead_creature.leaves_battlefield(player_def, player_atk)
            

    
def reset_creatures(player: Player):
    # Reset creatures on the player's board
    for creature in player.board:
        if isinstance(creature,CreatureCard):
            creature.power = creature.og_power + creature.counter_power
            creature.toughness = creature.og_toughness + creature.counter_toughness
            creature.attacking = False
            creature.blocking = False 
            creature.blocked_creature_id = None
            creature.spell_targeted = False
            creature.trample_eot = False

    # Reset creatures in the player's graveyard
    for creature in player.graveyard:
        if isinstance(creature,CreatureCard):
            creature.power = creature.og_power
            creature.toughness = creature.og_toughness
            creature.attacking = False
            creature.blocking = False
            creature.blocked_creature_id = None
            
def end_phase(playerAP:Player,playerNAP:Player,state:GameState):
    
    reset_creatures(playerAP)
    reset_creatures(playerNAP)
    next_turn(state)



def play_game(players: list[Player]):
    # Initialize the game state
    state = GameState(players, 1, "beginning")
    
    # Loop while all players have life > 0
    while all(player.life > 0 for player in state.players) and state.turn<20:
        # Determine the current player and the opponent
        current_player = state.players[state.turn % len(players)]
        opp_player = state.players[(state.turn + 1) % len(players)]
        begin(current_player,opp_player,state)

        # Start turn for the current player
        main_phase_1(current_player,opp_player, state)

        # Battle phase - attack with creatures if any are on the board
        if len(current_player.board) > 0:
            battle_phase(current_player, opp_player)

        main_phase_2(current_player,opp_player, state)
            
        end_phase(current_player,opp_player,state)
            

        
    print("Game over!")      

#prampampam DUBULTĀ, lai varēja Compare files darīt vieglākai pārkopēšanai uz jauno metodi. ja šo failu plāno izmantot,
# pareizā battle_phase pozīcija ir tur augstāk. Bet jāiekopē šis kods no zemāk, kaut kas maznedaudz pamainīts.

def battle_phase(player_atk:Player,player_def:Player):
    
    for creature in player_atk.board:           # Manifold Mouse effect
        if creature.name == "Manifold Mouse":   
            buff = random.choice(["trample"])   # UN "double strike" vajag vēl!
            controlled_mouses = [creature for creature in player_atk.board if creature.is_mouse == True]
            mouse = random.choice(controlled_mouses)
            # Valiant effect activation needed!
            print(f"Manifold mouse effect gave {buff} to {mouse.name} until EOT.")
        
            if buff == "trample":
                mouse.trample_eot == True
            elif buff == "double_strike":
                pass     # for now
        
    for creature in player_atk.board:
        if creature.tapped == False:
            if random.choice([1,1]) == 1:       # Uzbrūk vienmēr ar visiem
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
                if not (to_block.flying==True and blocker.flying==False):   # only 1 out of 4 cases when cannot block
                    blocker.blocked_creature_id = to_block.id
                else:
                    print(f"Couldn't block, attacker {to_block.name} flying: {to_block.flying}, blocker {blocker.name} flying: {blocker.flying}")
                
            
        for attacker in attackers:
            blockers = [blocker for blocker in player_def.board if blocker.blocked_creature_id == attacker.id]
            if blockers:
                if (attacker.menace == True and len(blockers) >= 2) or attacker.menace == False:    # checks menace condition
                    for blocker in blockers:
                        if attacker.power <= 0:
                            attacker.power = 0
                        if blocker.power <= 0:
                            blocker.power = 0
                        print(f"{blocker.power}/{blocker.toughness} {blocker.name} is blocking {attacker.power}/{attacker.toughness} {attacker.name}")

                        bt = blocker.toughness
                        ap = attacker.power
                        bp = blocker.power
                        
                        blocker.toughness -= ap
                        attacker.toughness -= bp
                        attacker.power -= bt

                    if (attacker.trample==True or attacker.trample_eot==True) and attacker.power>0:    # for remaining power, and doesn't need toughness check?
                        print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals Trample damage to Player {player_def.name}.")
                        player_def.life -= attacker.power
                        print(f"{player_def.name} has {player_def.life} life left")
                elif attacker.menace == True and len(blockers) == 1:
                    print(f"One blocker {blockers[0].name} cannot block {attacker.name} with Menace")
            else:
                print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals damage to Player {player_def.name}.")
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



deck1 = build_random_deck()
deck2 = build_random_deck()
start_hand1 = deck1[:7]
start_hand2 = deck2[:7]
deck1 = deck1[7:]
deck2 = deck2[7:]
    
player1 = Player("Bob", start_hand1, deck1, [], [], [], 0, 20)
player2 = Player("Alice", start_hand2, deck2, [], [], [], 0, 20)
players = [player1, player2]

play_game(players)
    
    

        
    