import uuid

class Card:
    
    pass

class CreatureCard(Card):
    def __init__(self, name: str, mana_cost: int, og_power: int, og_toughness: int, effects=None,deathrattle=None, is_token = False):
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
        
    def activate_effects(self, player):

        for effect in self.effects:
            effect.apply(player)   
            
    def play(self,player,state):
        if state.phase == "Main Phase 1":
            if player.mana_pool >= self.mana_cost:
                print(f"{player.name} plays {self.name}")
                player.hand.remove(self)
                player.mana_pool -= self.mana_cost
                player.graveyard.append(self)
                
                self.activate_effects(player)
            else:
                print(f"Not enough mana to play {self.name}")
        else:
            print("Cannot play sorcery outside Main Phase")    
        
        

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
    }
    
    
}


Land_Card_Registry = {
    "Mountain": {
        "name": "Mountain",
        "tap_effects": ["GainManaEffect()"] ,
        "tapped": False 
        
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
