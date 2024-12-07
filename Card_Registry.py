import uuid
import random

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

# Ko darīt ar izvēles soļiem? Vot svarīgākais jautājums, jo tādu ir padaudz, piem. manifold mouse ir 2 tādas izvēles.
# Jebšu, ko darīt ar "target creature" ?

class CreatureCard(Card):
    def __init__(self, name: str, mana_cost: int, og_power: int, og_toughness: int, cast_effects=None, later_effects=None, deathrattle=None,
                 is_token=False, auras = [], tapped = True, flying = False, is_mouse = False, trample = False, trample_eot = False, menace = False):
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
        self.blocked_creature_id = None
        self.cast_effects = cast_effects if cast_effects else []        # These are effects that activate ONLY on cast
        self.later_effects = later_effects if later_effects else []     # These are the conditional effects that must not activate on casting
        self.is_token = is_token
        self.deathrattle = deathrattle if deathrattle else []
        self.auras = auras
        self.tapped = tapped
        self.spell_targeted = False
        self.blockers = []
        self.flying = flying
        self.is_mouse = is_mouse
        self.trample = trample
        self.trample_eot = trample_eot  # for effects that apply trample only until end of turn
        self.menace = menace
        
        
    # def activate_cast_effects(self, player):
    #     # Trigger the card's on-play effects, for this deck only for Manifold Mouse
    #     for effect in self.cast_effects:
    #         effect.apply(self, player)        # So all creature effects have to take in creature and player, because both could be needed.
        
    def play(self,player,state):
        if state.phase == "main phase 1" or "main phase 2":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.board.append(self)
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                
                # Trigger the card's on-play effects, for this deck only for Manifold Mouse
                for effect in self.cast_effects:
                    effect.apply(self, player)        # So all creature effects have to take in creature and player, because both could be needed.

                # self.activate_cast_effects(player)
                
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play creature outside Main Phase")
            
    

    def leaves_battlefield(self, player, player_op):
        """Called when the creature leaves the battlefield."""
        if self.is_token:
            # Remove token from the player's battlefield
            player.board.remove(self)
            print(f"{self.name} (token) is removed from the game")
        else:            
            # Check if the card has a DeathRattle effect
            for deathrattle in self.deathrattle:
                # deathrattle.apply(self, player)   # Doesn't work if the effects have different specifics

                if isinstance(deathrattle, DmgToAny):       # Heartfire Hero
                    print(f"!!!!!!!!!!!! Heartfire Hero power for deathrattle, is correct?: {self.og_power + self.counter_power}")
                    deathrattle.apply(self, player_op, player, damage = self.og_power + self.counter_power)
            
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
        
    # def activate_effects(self, target, player):

    #     for effect in self.effects:
    #         effect.apply(self,target, player)   
            
    def play(self,player,state,target_choices):
        if self.name == "Lightning strike":
            target = random.choice(target_choices["all_enemies"])
        elif self.name == "Shock":
            target = random.choice(target_choices["all_enemies"])

        elif self.name == "Monstrous Rage":
            targets = target_choices["controlled_creatures"]
            if targets:
                target = random.choice(targets)    # Technically can target anyone, but putting in only reasonable options.
            else:
                print("Cannot play this card, no targets.")
                target = None

        elif self.name == "Might of the Meek":
            targets = target_choices["controlled_creatures"]
            if targets:
                target = random.choice(targets)
            else:
                print("Cannot play this card, no targets.")
                target = None
        else:
            print("ERROR: name for Instant not in options")

        if target:
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                player.graveyard.append(self)
                    
                # self.activate_effects(target, player)

                for effect in self.effects:             # Activating all the spell's effects right here
                    effect.apply(self, target, player)   

                # Trigger them effects for all creatures with cast-spell effects:
                for creature in player.board:
                    for effect in creature.later_effects:
                        if isinstance(effect, Prowess):
                            effect.apply(creature, player)  
                        if isinstance(effect, Prowess_Slickshot):
                            effect.apply(creature, player)
                # Trigger effects that activate on targeted:
                if isinstance(target, CreatureCard):
                    for effect in target.later_effects:
                        if target in player.hand:       # This activates only if cast on controlled target
                            if isinstance(effect, Valiant_Heartfire):       
                                effect.apply(target, player)
                            if isinstance(effect, Valiant_Emberheart):
                                effect.apply(target, player)

            else:
                print(f"Not enough mana to play {self.name}")

            
            
class EnchantmentCard(Card):
    def __init__(self,name:str,mana_cost: int, effects=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.effects = effects if effects else []
        # self.deathrattle = deathrattle if deathrattle else []
        
    # def activate_effects(self, target):

    #     for effect in self.effects:
    #         effect.apply(self,target)          
        
    def play(self,player,state,target_creatures):
        if self.name == "Demonic Ruckus":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                target = random.choice(target_creatures)
                # player.graveyard.append(self)
                    
                # self.activate_effects(target, player)

                for effect in self.effects:             # Activating all the spell's effects right here
                    effect.apply(self, target, player)   

                # Trigger them effects for all creatures with cast-spell effects:
                for creature in player.board:
                    for effect in creature.later_effects:
                        if isinstance(effect, Prowess):
                            effect.apply(creature, player)  
                        if isinstance(effect, Prowess_Slickshot):
                            effect.apply(creature, player)
                # Trigger effects that activate on targeted:
                if isinstance(target, CreatureCard):
                    for effect in target.later_effects:
                        if target in player.hand:       # This activates only if cast on controlled target
                            if isinstance(effect, Valiant_Heartfire):       
                                effect.apply(target, player)
                            if isinstance(effect, Valiant_Emberheart):
                                effect.apply(target, player)

            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("ERROR: name for Enchantment not in options")
            
        
    
    # def leaves_battlefield(self, player):
    #     self.activate_effects(player)
    #     player.board.remove(self)
    #     player.graveyard.append(self)
    #     print(f"{self.name} leaves the battlefield.")
        
        

Creature_Card_Registry = {
    # "Giant Bear": {
    #     "name": "Giant Bear",
    #     "mana_cost": 5,
    #     "og_power": 5,
    #     "og_toughness": 4,
    #     "effects": []  
    # },
    # "Undead Soldier": {
    #     "name": "Undead Soldier",
    #     "mana_cost": 2,
    #     "og_power": 2,
    #     "og_toughness": 2,
    #     "effects": []  
    # },
    # "Goblin Grunt": {
    #     "name": "Goblin Grunt",
    #     "mana_cost": 1,
    #     "og_power": 1,
    #     "og_toughness": 1,
    #     "effects": []  
    # },
    # "Goblin Shaman": {
    #     "name": "Goblin Shaman",
    #     "mana_cost": 3,
    #     "og_power": 2,
    #     "og_toughness": 2,
    #     "effects": ["GainManaEffect()"] 
    # },
    #     "Small Rock": {
    #     "name": "Small Rock",
    #     "mana_cost": 1,
    #     "og_power": 0,
    #     "og_toughness": 2,
    #     "effects": [], 
    #     "is_token": True
    # },
    #     "Rock": {
    #     "name": "Rock",
    #     "mana_cost": 2,
    #     "og_power": 0,
    #     "og_toughness": 4,
        # "deathrattle": ["Spawn(\"Small Rock\")"] 
    # },
    "Heartfire Hero": {
        "name": "Heartfire Hero",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 1,
        "later_effects": ["Valiant_Heartfire()"],
        "deathrattle": ["DmgToAny(0)"],  # Means damage is defined later
        "is_mouse": True
    },
    "Monastery Swiftspear": {
        "name": "Monastery Swiftspear",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 2,
        "tests": 71,
        "later_effects": ["Prowess()"],
        "tapped": False         # This is HASTE! Because that's for starting value
    },
    "Emberheart Challenger": {
        "name": "Emberheart Challenger",
        "mana_cost": 2,
        "og_power": 2,
        "og_toughness": 2,
        "later_effects": ["Prowess()", "Valiant_Emberheart()"],
        "tapped": False,
        "is_mouse": True
    },
    "Manifold Mouse": {
        "name": "Manifold Mouse",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 2,
        "cast_effects": ["Offspring(2)"],
        "later_effects": [],    # šeit jābūt vēl target mouse buff efektam
        "is_mouse": True
    },
    "Manifold Mouse Token": {
        "name": "Manifold Mouse Token",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 1,
        "later_effects": [],    # šeit jābūt vēl target mouse buff efektam
        "is_mouse": True,
        "is_token": True
    },
    "Slickshot Show-Off": {
        "name": "Slickshot Show-Off",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 2,
        "later_effects": ["Prowess_Slickshot()"],
        "tapped": False,
        "flying": True
    }
}


Land_Card_Registry = {
    "Mountain": {
        "name": "Mountain",
        "tap_effects": ["GainManaEffect()"] ,
        "tapped": False
    },
    # "Rockface Village": {
    #     "name": "Rockface Village",
    #     "tap_effects": ["GainManaEffect()"] ,   # Un vēl 2 alternatīvas ko var darīt
    #     "tapped": False 
    # } 
}

Instant_Card_Registry = {
    "Lightning strike": {
        "name": "Lightning strike",
        "mana_cost": 2,
        "effects": ["DmgToAny(3)"]         
    },
    "Shock": {
        "name": "Shock",
        "mana_cost": 1,
        "effects": ["DmgToAny(2)"]         
    },
    "Monstrous Rage": {
        "name": "Monstrous Rage",
        "mana_cost": 1,
        "effects": ["ApplyBuffs(2,0)"]  # Bet šim jābūt tikai līdz gājiena beigām, un vēl citi efekti ir.
    },
    "Might of the Meek": {
        "name": "Might of the Meek",
        "mana_cost": 1,
        "effects": ["Might_of_the_Meek()"]
    }
}

Enchantment_Card_Registry = {
    "Demonic Ruckus": {
        "name": "Demonic Ruckus",
        "mana_cost": 2,
        "effects": ["Demonic_Aura()"]
    }
}

        

# Card factory function to create unique card instances
def card_factory(card_name,card_type):
    if card_type == "Creature":
        template = Creature_Card_Registry.get(card_name)


        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")
        

        return CreatureCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            og_power=template["og_power"],
            og_toughness=template["og_toughness"],
            cast_effects=[eval(effect) for effect in template.get("cast_effects", [])],
            later_effects=[eval(effect) for effect in template.get("later_effects", [])],
            deathrattle=[eval(deathrattle) for deathrattle in template.get("deathrattle", [])],
            is_token=template.get("is_token", False),
            auras=template.get("auras", []),
            tapped=template.get("tapped", True),
            flying=template.get("flying", False),
            is_mouse=template.get("is_mouse", False),
            trample=template.get("trample", False),
            trample_eot=template.get("trample_eot", False),
            menace=template.get("menace", False)
        )
    
    elif card_type == "Land":
        template = Land_Card_Registry.get(card_name)
        
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")
        
        return LandCard(
            name=template["name"],
            tapped=template.get("tapped", False),
            tap_effects=[eval(tap_effects) for tap_effects in template.get("tap_effects", [])]
        )
        
    elif card_type == "Instant":
        template = Instant_Card_Registry.get(card_name)
         
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")   
        
        return InstantCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            effects=[eval(effects) for effects in template.get("effects", [])]
        )      
    
    elif card_type == "Enchantment":
        template = Enchantment_Card_Registry.get(card_name)
         
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")   
        
        return EnchantmentCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            effects=[eval(effects) for effects in template.get("effects", [])]
        )   
    
    else:
        print("ERROR: CardFactory, no such type")
        



class GainManaEffect:
    def __init__(self, mana_amount=1):
        self.mana_amount = mana_amount

    def apply(self, player):
        # This effect adds mana to the player's mana pool
        player.mana_pool += self.mana_amount
        print(f"{player.name} gains {self.mana_amount} mana! Current mana: {player.mana_pool}")
        
class Spawn:
    def __init__(self, token_name = False):
        self.token = card_factory(token_name,"Creature")
    
    def apply(self,player):
        player.board.append(self.token)
        print(f"{player.name} spawns {self.token.name}")
        
class DmgToAny:
    def __init__(self, damage = 0):
        self.damage = damage
        
    def apply(self, card, target, player, damage = 0):          # self nāk no DmgToAny inita, card ir selfs? ko padod instantā izsaukšana.
        if isinstance(target,Player):
            if self.damage > 0:         # The case when damage can be defined at start
                damage = self.damage
            target.life -= damage
            print(f"{card.name} does {damage} damage to {target.name}")
            print(f"{target.name} has {target.life} life left")
        elif isinstance(target, CreatureCard):
            if self.damage > 0:         # The case when damage can be defined at start
                damage = self.damage
            target.toughness -= damage
            print(f"{card.name} does {damage} damage to {target.name}")
        else:
            print(f"{target.name} is not a valid target")

# Mēģināju pēc analoģijas interes pēc pievienot power/toughness mainītāju, kas strādā gan ar +, gan -. 
# Idejiski gan šis pagaidām pamaina paliekoši, nevis tikai līdz gājiena beigām.
class ApplyBuffs:
    def __init__(self, power_change=0, toughness_change=0):
        self.power_change = power_change
        self.toughness_change = toughness_change
    
    def apply(self, card, target, player):
        if isinstance(target, CreatureCard):
            target.power += self.power_change
            target.toughness += self.toughness_change
            print(f"{card.name} gives +{self.power_change}/+{self.toughness_change} to {target.name}")
        else:
            print(f"{target.name} is not a valid target")

class Prowess:
    def apply(self, creature: CreatureCard, player):
        # Apply the +1/+1 effect to the creature
        creature.power += 1
        creature.toughness += 1
        print(f"{creature.name} got +1/+1 until end of turn from Prowess")

class Prowess_Slickshot: 
    def apply(self, creature: CreatureCard, player):
        # Apply the +2/+0 effect to the creature
        creature.power += 2
        creature.toughness += 0
        print(f"{creature.name} got +2/+0 until end of turn from Prowess_Slickshot")

class Valiant_Heartfire:        # Šim vajag aktivizēties arī no Manifold Mouse targeted efekta
    def apply(creature: CreatureCard, player):
        print("Valiant Heartfire called")
        if creature.spell_targeted == False:
            creature.counter_power += 1
            creature.counter_toughness += 1
            creature.spell_targeted = True
            print(f"Valiant Heartfire buffed {creature.name}")


class Valiant_Emberheart:
    def apply(creature: CreatureCard, player):
        print("Valiant Emberheart called")
        if creature.spell_targeted == False:
            player.deck.pop()
            # Jāpieliek, ka var izspēlēt līdz gājiena beigām
            creature.spell_targeted = True
            print(f"Valiant Emberheart activated from {creature.name}")

class Offspring:
    def __init__(self, mana_cost):
        self.mana_cost = mana_cost
    
    def apply(self, card, player):
        if player.mana_pool >= self.mana_cost:
            if random.choice([0,1]) == 1:
                print(f"{player.name} used Offspring")
                player.mana_pool -= self.mana_cost
                offspring = Spawn("Manifold Mouse Token")
                offspring.apply(player)                     # creates and plays the token

class Might_of_the_Meek:
    def apply(self, card, target: CreatureCard, player: Player):
        if isinstance(target, CreatureCard):
            target.trample_eot = True
            controlled_mouses = [creature for creature in player.board if creature.is_mouse == True]
            print(f"{card.name} gave Trample to {target.name} until EOT. ")
            if controlled_mouses:
                target.power += 1
                print(f"and {target.name} also received +1/+0 from {card.name} since {player.name} is controlling a Mouse")
        else:
            print(f"{target.name} is not a valid target")

class Demonic_Aura:
    def apply(self, card, creature: CreatureCard, player: Player):    # self?
        creature.counter_power += 1         # So it could be a perma buff
        creature.counter_toughness += 1
        creature.menace = True              # Both also permanent
        creature.trample = True
        creature.auras += [Demonic_Aura]
        print(f"{card.name} buffed and applied an Aura to {creature.name}")

    def leaves_battlefield(player):
        # draw_card(player)
                        # vajag draw_card, bet laikam ne šeit, bet enginā.
        print(f"{player.name}'s Demonic Aura left the battlefield, needs to draw a card.")


        
