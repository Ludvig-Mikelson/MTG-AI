# %% 
import random
from Card_Registry import card_factory, Creature_Card_Registry,Land_Card_Registry, Card,CreatureCard,LandCard, Player,InstantCard,Instant_Card_Registry


#class GameState:
    #def __init__(self, player_AP: Player, player_NAP: Player, player_S: Player, player_NS: Player, 
       #          turn: int, phase: str):
       # self.player_AP = player_AP
       # self.player_NAP = player_NAP
       #self.player_S = player_S
       #self.player_NS = player_NS
       # self.turn = turn
       #self.phase = phase      

        
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
    sorcery_card_names = list(Instant_Card_Registry.keys())
    deck = []
    
    for _ in range((deck_size-30)):
        card_name = random.choice(card_names)  # Randomly select a card name
        card = card_factory(card_name,"Creature")  # Create a unique instance of the card
        deck.append(card)  # Add the card to the deck
       
    for _ in range(20):
        land_card_name = random.choice(land_card_names)  
        card = card_factory(land_card_name,"Land")  
        deck.append(card) 
        
    for _ in range(10):
        sorcery_card_name = random.choice(sorcery_card_names)  
        card = card_factory(sorcery_card_name,"Instant")  
        deck.append(card)         
    
    random.shuffle(deck)

    return deck
    
    
def draw_card(player):
    if len(player.deck) > 0:
        player.hand.append(player.deck.pop())     
    else:
        print("No more cards")
        
def next_turn(state:GameState):
    state.turn += 1
    
def begin(playerAP:Player,playerNAP:Player,state:GameState):
    playerAP.mana_pool = 0
    playerNAP.mana_pool = 0    
    state.phase = "begin phase"
    playerAP.played_land = False
    for land in playerAP.land_board:
        land.tapped = False
    
    draw_card(playerAP)

    
def main_phase_1(playerAP:Player,playerNAP:Player,state:GameState):
    
    playerAP.mana_pool = 0
    playerNAP.mana_pool = 0
    state.phase = "main phase 1"
    print(f"{playerAP.name} Main Phase 1")
    
    lands = [card for card in playerAP.hand if isinstance(card, LandCard)]
    if playerAP.played_land == False and len(lands) > 0:
    
        random.choice(lands).play(playerAP,state)
        playerAP.played_land == True
    
    if len(playerAP.land_board) > 0:
        for land in playerAP.land_board:
            if land.tapped == False:
                land.tap(playerAP)
                
def main_phase_2(playerAP:Player,playerNAP:Player,state:GameState):
    state.phase = "main phase 2"

            

def reset_creatures(player: Player):
    # Reset creatures on the player's board
    for creature in player.board:
        if isinstance(creature,CreatureCard):
            creature.power = creature.og_power
            creature.toughness = creature.og_toughness
            creature.attacking = False
            creature.blocking = False
            creature.blocked_creature_id = None

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
    
        
        
        
def battle_phase(player_atk:Player,player_def:Player):
    
    for creature in player_atk.board:
        if random.choice([1,2]) == 1:
            creature.attacking = True
            print(f"{creature.power}/{creature.toughness} {creature.name}, is attacking {player_def.name}")
    
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
                print(f"{dead_creature.name} is sent to the graveyard.")
                #player_atk.board.remove(dead_creature)
                #player_atk.graveyard.append(dead_creature)
                dead_creature.leaves_battlefield(player_atk)
                
        dead_creatures_def = [creature.id for creature in player_def.board if creature.toughness <= 0]
        for dead_creature_id in dead_creatures_def:   
            dead_creature = next((creature for creature in player_def.board if creature.id == dead_creature_id), None)
            if dead_creature:
                print(f"{dead_creature.name} is sent to the graveyard.")
                #player_def.board.remove(dead_creature)
                #player_def.graveyard.append(dead_creature)
                dead_creature.leaves_battlefield(player_def)
            
    


def play_game(players: list[Player]):
    # Initialize the game state
    state = GameState(players, 1, "beginning")
    
    # Loop while all players have life > 0
    while all(player.life > 0 for player in state.players):
        # Determine the current player and the opponent
        current_player = state.players[state.turn % len(players)]
        opp_player = state.players[(state.turn + 1) % len(players)]
        begin(current_player,opp_player,state)
        # Start turn for the current player
        main_phase_1(current_player,opp_player, state)


        # For now, play random card
        creatures_hand = [card for card in current_player.hand if isinstance(card, CreatureCard)]
        sorceries_hand = [card for card in current_player.hand if isinstance(card, InstantCard)]
        if len(creatures_hand) > 0:
            #play_card(current_player, current_player.hand[0], state)  # Play the first card in hand
            random.choice(creatures_hand).play(current_player,state)
            
        if len(sorceries_hand) > 0:
            random.choice(sorceries_hand).play(current_player,state,opp_player)

        # Battle phase - attack with creatures if any are on the board
        if len(current_player.board) > 0:
            battle_phase(current_player, opp_player)
            
        end_phase(current_player,opp_player,state)
            

        

    
    print("Game over!")      


deck1 = build_random_deck()
deck2 = build_random_deck()
    
player1 = Player("Bob", [], deck1, [], [], [], 0, 20)
player2 = Player("Alice", [], deck2, [], [], [], 0, 20)
players = [player1, player2]

play_game(players)
    
    

        
    