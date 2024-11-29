import uuid

class Card:
    pass

class Player:
    def __init__(self, name: str, hand: list[Card], deck: list[Card], 
                 board: list[Card], land_board: list[Card], graveyard: list[Card], mana_pool: int, life: int):
        self.name = name
        self.hand = hand
        self.deck = deck
        self.board = board
        self.land_board = land_board
        self.graveyard = graveyard
        self.mana_pool = mana_pool
        self.life = life
        self.played_land = False
        self.passed = False
        
class GameState:
    def __init__(self, player_AP: Player, player_NAP: Player, 
                 turn: int, stack: list):
        self.player_AP = player_AP
        self.player_NAP = player_NAP
        self.player_S = player_AP
        self.player_NS = player_NAP
        self.turn = turn
        self.stack = stack
        self.phase = "first phase"  
        
        
class CreatureCard(Card):
    def __init__(self, name: str, mana_cost: int, og_power: int, og_toughness: int, effects=None, prowess=None, valiant=None,
                 auras = [], tapped = True):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.og_power = og_power
        self.og_toughness = og_toughness
        self.power = og_power  # Initialize with original values
        self.toughness = og_toughness  # Initialize with original values
        self.counter_power = 0
        self.counter_toughness = 0
        self.attacking = False
        self.blocking = False
        self.effects = effects if effects else []       # These are only effects that DON'T activate on placement!
        self.auras = auras
        self.tapped = tapped
        self.spell_targeted = False
        self.blockers = []
        self.prowess = prowess if prowess else []
        self.valiant = valiant if valiant else []
        
        
    def activate_effects(self, player):
        # Trigger the card's on-play effects, for this deck there are none
        for effect in self.effects:
            effect.apply(self, player)        # So all creature effects have to take in creature and player.
            
    def activate_prowess(self, player):
        # Trigger the card's on-play effects, for this deck there are none
        for effect in self.prowess:
            effect.apply(self, player)        # So all creature effects have to take in creature and player.
        
    def play(self,player,state):
        if state.phase == "main phase 1" or "main phase 2":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.board.append(self)
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                
                # self.activate_effects(player)     # Because there are no on-play effects

            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play creature outside Main Phase")
            
    

    def leaves_battlefield(self, player, player_op):
        """Called when the creature leaves the battlefield."""

        player.board.remove(self)
        player.graveyard.append(self)
        self.counter_power = 0
        self.counter_toughness = 0
        print(f"{self.name} leaves the battlefield.")
                     
        if len(self.auras) > 0:
            for aura in self.auras:
                aura.leaves_battlefield(player)
                

    def __str__(self):
        # Return a human-readable string when printing the object
        return f"{self.name} (Mana: {self.mana_cost}, Power: {self.power}, Toughness: {self.toughness}, ID: {self.id})"
    
class LandCard(Card):
    def __init__(self,name:str,tap_effects,tapped = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tapped = tapped
        self.tap_effects = tap_effects if tap_effects else []
        
    def play(self,player,state):
        if state.phase == "main phase 1" or "main phase 2":
            if player.played_land == False:
                print(f"{player.name} plays {self.name}")
                player.land_board.append(self)
                player.hand.remove(self)
                
            else:
                print(f"Can't play {self.name}, land was already played")
        else:
            print("Cannot play land outside Main Phase")        
        
    def tap(self,player):
        if self.tapped == False:
            print(f"{player.name} tapped {self.name} for mana")
            self.tap_effects[0].apply(player)

            self.tapped = True
            
class InstantCard(Card):
    def __init__(self,name:str,mana_cost: int, effects=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.effects = effects if effects else []
        
    def activate_effects(self, target):

        for effect in self.effects:
            effect.apply(self,target)   
            
    def play(self,player,target):

        if player.mana_pool >= self.mana_cost:
            print(f"{player.name} plays {self.name}")
            player.hand.remove(self)
            player.mana_pool -= self.mana_cost
            player.graveyard.append(self)
                
            self.activate_effects(target)

            # Trigger them effects for all creatures with said effects:
            for creature in player.board:
                if creature.prowess:
                    for effect in creature.prowess:
                        effect.apply(creature, player)

            # Trigger the effects that activate on targeted:
            if target.valiant:
                for effect in target.valiant:
                        effect.apply(target, player)

        else:
            print(f"Not enough mana to play {self.name}")

            
            
            
class EnchantmentCard(Card):
    def __init__(self,name:str,mana_cost: int, effects=None, deathrattle=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.effects = effects if effects else []
        self.deathrattle = deathrattle if deathrattle else []
        
    def activate_effects(self, target):

        for effect in self.effects:
            effect.apply(self,target)          
        
    def play(self,player,state,creaturecard):
        if state.phase == "main phase 1" or "main phase 2":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                creaturecard.auras.append(self)
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                
                self.activate_effects(player)
            # Trigger them effects for all creatures with said effects:
            for creature in player.board:
                if creature.prowess:
                    for effect in creature.prowess:
                        effect.apply(creature, player)
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play creature outside Main Phase")
            
        
    
    def leaves_battlefield(self, player):
        self.activate_effects(player)
        player.board.remove(self)
        player.graveyard.append(self)
        print(f"{self.name} leaves the battlefield.")    