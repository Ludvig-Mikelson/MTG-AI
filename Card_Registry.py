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



class CreatureCard(Card):
    def __init__(self, name: str, mana_cost: int, og_power: int, og_toughness: int, effects=None, deathrattle=None, is_token=False,
                 auras = []):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.og_power = og_power
        self.og_toughness = og_toughness
        self.power = og_power  # Initialize with original values
        self.toughness = og_toughness  # Initialize with original values
        self.attacking = False
        self.blocking = False
        self.blocked_creature_id = None
        self.effects = effects if effects else []
        self.is_token = is_token
        self.deathrattle = deathrattle if deathrattle else []
        self.auras = auras
        
        
    def activate_effects(self, player):
        # Trigger the card's effects
        for effect in self.effects:
            effect.apply(player)        
        
    def play(self,player,state):
        if state.phase == "Main Phase 1":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.board.append(self)
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                
                self.activate_effects(player)
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play creature outside Main Phase")
            
    

    def leaves_battlefield(self, player):
        """Called when the creature leaves the battlefield."""
        if self.is_token:
            # Remove token from the player's battlefield
            player.board.remove(self)
            print(f"{self.name} (token) is removed from the game")
        else:
            player.board.remove(self)
            player.graveyard.append(self)
            print(f"{self.name} leaves the battlefield.")
            
            # Check if the card has a DeathRattle effect
            for deathrattle in self.deathrattle:
                deathrattle.apply(player)
                
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
        if state.phase == "Main Phase 1":
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
            
class SorceryCard(Card):
    def __init__(self,name:str,mana_cost: int, effects=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.mana_cost = mana_cost
        self.effects = effects if effects else []
        
    def activate_effects(self, target):

        for effect in self.effects:
            effect.apply(self,target)   
            
    def play(self,player,state,target):
        if state.phase == "Main Phase 1":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                player.graveyard.append(self)
                
                self.activate_effects(target)
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play sorcery outside Main Phase")    
            
            
            
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
        if state.phase == "Main Phase 1":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                creaturecard.auras.append(self)
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                
                self.activate_effects(player)
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play creature outside Main Phase")
            
        
    
    def leaves_battlefield(self, player):
        self.activate_effects(player)
        player.board.remove(self)
        player.graveyard.append(self)
        print(f"{self.name} leaves the battlefield.")
        
        

Creature_Card_Registry = {
    "Giant Bear": {
        "name": "Giant Bear",
        "mana_cost": 5,
        "og_power": 5,
        "og_toughness": 4,
        "effects": []  
    },
    "Undead Soldier": {
        "name": "Undead Soldier",
        "mana_cost": 2,
        "og_power": 2,
        "og_toughness": 2,
        "effects": []  
    },
    "Goblin Grunt": {
        "name": "Goblin Grunt",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 1,
        "effects": []  
    },
    "Goblin Shaman": {
        "name": "Goblin Shaman",
        "mana_cost": 3,
        "og_power": 2,
        "og_toughness": 2,
        "effects": ["GainManaEffect()"] 
    },
        "Small Rock": {
        "name": "Small Rock",
        "mana_cost": 1,
        "og_power": 0,
        "og_toughness": 2,
        "effects": [], 
        "is_token": True
    },
        "Rock": {
        "name": "Rock",
        "mana_cost": 2,
        "og_power": 0,
        "og_toughness": 4,
        "deathrattle": ["Spawn(\"Small Rock\")"] 
    },
    "Heartfire Hero": {
        "name": "Heartfire Hero",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 1,
        "effects": []
    },
    "Monastery Swiftspear": {
        "name": "Monastery Swiftspear",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 2,
        "effects": []
    },
    "Emberheart Challenger": {
        "name": "Emberheart Challenger",
        "mana_cost": 2,
        "og_power": 2,
        "og_toughness": 2,
        "effects": []
    },
    "Manifold Mouse": {
        "name": "Manifold Mouse",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 2,
        "effects": []
    },
    "Slickshot Show-Off": {
        "name": "Slickshot Show-Off",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 2,
        "effects": []
    }
    
    
}


Land_Card_Registry = {
    "Mountain": {
        "name": "Mountain",
        "tap_effects": ["GainManaEffect()"] ,
        "tapped": False 
    },
    "Rockface Village": {
        "name": "Rockface Village",
        "tap_effects": ["GainManaEffect()"] ,   # Un vēl 2 alternatīvas ko var darīt
        "tapped": False 
    }
    
    
}

Sorcery_Card_Registry = {
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
            effects = [eval(effect) for effect in template.get("effects", [])],
            deathrattle=[eval(deathrattle) for deathrattle in template.get("deathrattle", [])],
            is_token= template.get("is_token", False)
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
        
    elif card_type == "Sorcery":
        template = Sorcery_Card_Registry.get(card_name)
         
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")   
        
        return SorceryCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            effects=[eval(effects) for effects in template.get("effects", [])]
        )      
        



class GainManaEffect:
    def __init__(self, mana_amount=1):
        self.mana_amount = mana_amount

    def apply(self, player):
        # This effect adds mana to the player's mana pool
        player.mana_pool += self.mana_amount
        print(f"{player.name} gains {self.mana_amount} mana! Current mana: {player.mana_pool}")
        
class Spawn:
    def __init__(self, token = False):
        self.token = card_factory(token,"Creature")
    
    def apply(self,player):
        player.board.append(self.token)
        print(f"{player.name} spawns {self.token.name}")
        
class DmgToAny:
    def __init__(self, damage = 0):
        self.damage = damage
        
    def apply(self,card,target):
        if isinstance(target,Player):
            target.life -= self.damage
            print(f"{card.name} does {self.damage} damage to {target.name}")
        elif isinstance(CreatureCard):
            target.toughness -= self.damage
            print(f"{card.name} does {self.damage} damage to {target.name}")
        else:
            print(f"{target.name} is not a valid target")

# Mēģināju pēc analoģijas interes pēc pievienot power/toughness mainītāju, kas strādā gan ar +, gan -. 
# Idejiski gan šis pagaidām pamaina paliekoši, nevis tikai līdz gājiena beigām.
class ApplyBuffs:
    def __init__(self, power_change=0, toughness_change=0):
        self.power_change = power_change
        self.toughness_change = toughness_change
    
    def apply(self, card, target):
        if isinstance(CreatureCard):
            if self.power_change != 0:
                target.power += self.power_change
                print(f"{card.name} gives {self.power_change} power to {target.name}")
            if self.toughness_change != 0:
                target.toughness += self.toughness_change
                print(f"{card.name} gives {self.toughness_change} toughness to {target.name}")
        else:
            print(f"{target.name} is not a valid target")
        
