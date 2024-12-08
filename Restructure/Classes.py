import uuid
import random

class Card:
    pass

class Player:
    def __init__(self, name: str, hand: list[Card], deck: list[Card], 
                 board: list[Card], land_board: list[Card], graveyard: list[Card], mana_pool: 0, life: 20):
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
        

        
        
class CreatureCard(Card):
    def __init__(self, name: str, mana_cost: int, og_power: int, og_toughness: int, cast_effects=None, deathrattle_dmg=None,
                is_token=False, auras = [], tapped = True, flying = False, is_mouse = False, trample = False, trample_eot = False, menace = False,
                prowess=None, valiant=None):
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
        self.is_token = is_token
        self.auras = auras
        self.tapped = tapped
        self.spell_targeted = False
        self.blockers = []
        self.flying = flying
        self.is_mouse = is_mouse
        self.trample = trample
        self.trample_eot = trample_eot  # for effects that apply trample only until end of turn
        self.menace = menace

        self.cast_effects = cast_effects if cast_effects else []        # These are effects that activate ONLY on cast
        self.prowess = prowess if prowess else []
        self.valiant = valiant if valiant else []
        self.deathrattle_dmg = deathrattle_dmg if deathrattle_dmg else []
        

    def activate_cast_effects(self, player):
        for effect in self.cast_effects:
            effect.apply(self, player)        # So all creature effects have to take in creature and player.
                    
    def activate_prowess(self):
        for effect in self.prowess:
            print(f"this is self {self}")
            effect.apply(self)        # So all creature effects have to take in creature and player.
    
    def activate_valiant(self, player):
        for effect in self.valiant:
            effect.apply(self, player)        # So all creature effects have to take in creature and player.

    def activate_deathrattle_dmg(self, player_op, player):
        print(f"!!!!!!!!!!!! Heartfire Hero power for deathrattle, is correct?: {self.og_power + self.counter_power}")
        for effect in self.deathrattle_dmg:
            effect.damage = self.og_power + self.counter_power
            effect.apply(self, player_op)        # So all creature effects have to take in creature and player.

    def play(self,player):
        
        print(f"{player.name} plays {self.name}")
        player.board.append(self)
        player.hand.remove(self)        # un manapool cena tad ir jau samaksāta pirms šejienes?
            
        # Trigger the card's on-play effects, for this deck only for Manifold Mouse
        # for effect in self.cast_effects:
        #     effect.apply(self, player)        # So all creature effects have to take in creature and player, because both could be needed.

        self.activate_cast_effects(player)      # izdzēsu self, cerams strādā.

            
    def attack(self,player):
        self.attacking = True
        print(f"{player.name}'s {self.name} declares attack")
        
    def block(self,player,attacker):
        self.blocking = True
        attacker.blockers.append(self)
        print(f"{player.name}'s {self.name} declares block on {attacker.name}")
        
            

    def leaves_battlefield(self, player, player_op):       # vajag arī op_player, lai var Heartfire deathrattle damage izpildīt.
        """Called when the creature leaves the battlefield."""
        if self.is_token:
            # Remove token from the player's battlefield
            player.board.remove(self)
            print(f"{self.name} (token) is removed from the game")
        else:            
            # Heartfire Hero Deathrattle only inside:
            self.activate_deathrattle_dmg(player_op, player)

            # for deathrattle in self.deathrattle:
            #     # deathrattle.apply(self, player)   # Doesn't work if the effects have different specifics

            #     if isinstance(deathrattle, ef.DmgToAny):       # Heartfire Hero
            #         print(f"!!!!!!!!!!!! Heartfire Hero power for deathrattle, is correct?: {self.og_power + self.counter_power}")
            #         deathrattle.apply(self, player_op, player, damage = self.og_power + self.counter_power)
            
            player.board.remove(self)
            player.graveyard.append(self)
            self.counter_power = 0
            self.counter_toughness = 0
            print(f"{self.name} leaves the battlefield.")

        if len(self.auras) > 0:
            for aura in self.auras:
                aura.leaves_battlefield(player)
                

    #def __str__(self):
        # Return a human-readable string when printing the object
        #return f"{self.name} (Mana: {self.mana_cost}, Power: {self.power}, Toughness: {self.toughness}, ID: {self.id})"
    
class LandCard(Card):
    def __init__(self,name:str,tap_effects,tapped = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tapped = tapped
        self.tap_effects = tap_effects if tap_effects else []
        
    def play(self,player):
        
        print(f"{player.name} plays {self.name}")
        player.land_board.append(self)
        player.hand.remove(self)
        player.played_land = True
        print("test")
            
        
    def tap(self,player):
        if self.tapped == False:
            print(f"{player.name} tapped {self.name} for mana")
            self.tap_effects[0].apply(player)

            self.tapped = True
            
class InstantCard(Card):
    def __init__(self,name:str,mana_cost: int, effects=None, targets = "all"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.effects = effects if effects else []
        self.targets = targets
        
    def activate_effects(self, target):

        for effect in self.effects:
            effect.apply(self,target)   
            
    def play(self,player, target):  

        print(f"{player.name} plays {self.name}")
        player.mana_pool -= self.mana_cost
        player.graveyard.append(self)
            
        self.activate_effects(target)

        # for effect in self.effects:             # Activating all the spell's effects right here
        #     effect.apply(self, target, player)   

        # Trigger them effects for all creatures with cast-spell effects:
        for creature in player.board:
            creature.activate_prowess()
            # for effect in creature.prowess:
            #     if isinstance(effect, ef.Prowess):
            #         effect.apply(creature, player)  
            #     if isinstance(effect, ef.Prowess_Slickshot):
            #         effect.apply(creature, player)

        # Trigger effects that activate on targeted:
        if isinstance(target, CreatureCard):
            if target in player.hand:       # This activates only if cast on controlled target
                    target.activate_valiant(target, player)
                # for effect in target.later_effects:
                #     if isinstance(effect, ef.Valiant_Heartfire):       
                #         effect.apply(target, player)
                #     if isinstance(effect, ef.Valiant_Emberheart):
                #         effect.apply(target, player)



    
        # print(f"{player.name} plays {self.name}")
        # #player.hand.remove(self)
        # player.graveyard.append(self)
                
        # self.activate_effects(target)
        # for effect in self.effects:
        #     effect.apply(self,target)  

        #     # Trigger them effects for all creatures with said effects:
        # for creature in player.board:
        #     if creature.prowess:
        #         for effect in creature.prowess:
        #             effect.apply(creature, player)

        #     # Trigger the effects that activate on targeted:
        # if isinstance(target, CreatureCard):
        #     if target.valiant:
        #         for effect in target.valiant:
        #                 effect.apply(target, player)

       

            
            
            
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
        
    def play(self,player,target_creatures):
        if self.name == "Demonic Ruckus":
            if player.mana_pool >= self.mana_cost:          # Vai šeit vajag šo pārbaudi?
                print(f"{player.name} plays {self.name}")
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                target = random.choice(target_creatures)
                target.auras.append(self)
                # player.graveyard.append(self)
                    
                self.activate_effects(target, player)

                # Trigger them effects for all creatures with cast-spell effects:
                for creature in player.board:
                    creature.activate_prowess(creature, player)
                    # for effect in creature.prowess:
                    #     if isinstance(effect, ef.Prowess):
                    #         effect.apply(creature, player)  
                    #     if isinstance(effect, ef.Prowess_Slickshot):
                    #         effect.apply(creature, player)

                # Trigger effects that activate on targeted:
                if isinstance(target, CreatureCard):
                    if target in player.hand:       # This activates only if cast on controlled target
                            target.activate_valiant(target, player)
                        # for effect in target.later_effects:
                        #     if isinstance(effect, ef.Valiant_Heartfire):       
                        #         effect.apply(target, player)
                        #     if isinstance(effect, ef.Valiant_Emberheart):
                        #         effect.apply(target, player)

            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("ERROR: name for Enchantment not in options")



            # if player.mana_pool >= self.mana_cost:            # šeit vajag šo pārbaudi?
            #     print(f"{player.name} plays {self.name}")
            #     creaturecard.auras.append(self)
            #     player.hand.remove(self)
            #     player.mana_pool -= self.mana_cost
                
                # self.activate_effects(player)
            # Trigger them effects for all creatures with said effects:
            # for creature in player.board:
            #     if creature.prowess:
            #         for effect in creature.prowess:
            #             effect.apply(creature, player)

            
        
    
    # def leaves_battlefield(self, player):
    #     self.activate_effects(player)
    #     player.board.remove(self)
    #     player.graveyard.append(self)
    #     print(f"{self.name} leaves the battlefield.")    