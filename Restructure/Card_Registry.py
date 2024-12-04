import Effects as ef
import Classes as cs
        
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
    #     "deathrattle": ["Spawn(\"Small Rock\")"] 
    # },
    "Heartfire Hero": {
        "name": "Heartfire Hero",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 1,
        "effects": ["ef.Valiant_Heartfire()"],
        "deathrattle": ["ef.DmgToAny(0)"],  # Damage is defined later
        "is_mouse": True
    },
    "Monastery Swiftspear": {
        "name": "Monastery Swiftspear",
        "mana_cost": 1,
        "og_power": 1,
        "og_toughness": 2,
        "effects": ["ef.Prowess()"],
        "tapped": False         # This is HASTE! Because that's for starting value
    },
    "Emberheart Challenger": {
        "name": "Emberheart Challenger",
        "mana_cost": 2,
        "og_power": 2,
        "og_toughness": 2,
        "effects": ["ef.Prowess()", "ef.Valiant_Emberheart()"],
        "tapped": False,
        "is_mouse": True
    },
    "Manifold Mouse": {
        "name": "Manifold Mouse",
        "mana_cost": 2,
        "og_power": 1,
        "og_toughness": 2,
        "cast_effects": ["ef.Offspring(2)"],
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
        "effects": ["ef.Prowess_Slickshot()"],
        "tapped": False,
        "flying": True
    }    
}


Land_Card_Registry = {
    "Mountain": {
        "name": "Mountain",
        "tap_effects": ["ef.GainManaEffect()"] ,
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
        "effects": ["ef.DmgToAny(3)"]         
    },
    "Shock": {
        "name": "Shock",
        "mana_cost": 1,
        "effects": ["ef.DmgToAny(2)"]         
    },
    "Monstrous Rage": {
        "name": "Monstrous Rage",
        "mana_cost": 1,
        "effects": ["ef.ApplyBuffs(2,0)"]  # Bet šim jābūt tikai līdz gājiena beigām, un vēl citi efekti ir.
    },
    "Might of the Meek": {
        "name": "Might of the Meek",
        "mana_cost": 1,
        "effects": ["ef.Might_of_the_Meek()"]
    }
}

Enchantment_Card_Registry = {
    "Demonic Ruckus": {
        "name": "Demonic Ruckus",
        "mana_cost": 2,
        "effects": ["ef.Demonic_Aura()"]
    }
}
    



# Card factory function to create unique card instances
def card_factory(card_name,card_type):
    if card_type == "Creature":
        template = Creature_Card_Registry.get(card_name)


        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")
        

        return cs.CreatureCard(
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
        
        return cs.LandCard(
            name=template["name"],
            tapped=template.get("tapped", False),
            tap_effects=[eval(tap_effects) for tap_effects in template.get("tap_effects", [])]
        )
        
    elif card_type == "Instant":
        template = Instant_Card_Registry.get(card_name)
         
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")   
        
        return cs.InstantCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            effects=[eval(effects) for effects in template.get("effects", [])]
        )      
    
    elif card_type == "Enchantment":
        template = Enchantment_Card_Registry.get(card_name)
         
        if not template:
            raise ValueError(f"Card '{card_name}' is not in the registry.")   
        
        return cs.EnchantmentCard(
            name=template["name"],
            mana_cost=template["mana_cost"],
            effects=[eval(effects) for effects in template.get("effects", [])]
        )   
    
    else:
        print("ERROR: CardFactory, no such type")



