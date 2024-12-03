import Classes as cs

class GainManaEffect:
    def __init__(self, mana_amount=1):
        self.mana_amount = mana_amount

    def apply(self, player):
        #This effect adds mana to the player's mana pool
        player.mana_pool += self.mana_amount
        print(f"{player.name} gains {self.mana_amount} mana! Current mana: {player.mana_pool}")
        
# class Spawn:
#     def __init__(self, token = False):
#         self.token = card_factory(token,"Creature")
    
#     def apply(self,player):
#         player.board.append(self.token)
#         print(f"{player.name} spawns {self.token.name}")
        
class DmgToAny:
    def __init__(self, damage = 0):
        self.damage = damage
        
    def apply(self, card, target):
        print("BADABAAMFMAMFAMFAMFMAMF HEHEHEEHHEHEHEHEHEHHHEH HHIHIHIHIHI")
        print(card)
        print(target)
        if isinstance(target,cs.Player):
            
            target.life -= self.damage
            print(f"{card.name} does {self.damage} damage to {target.name}")
            print(f"{target.name} has {target.life} life left")
        elif isinstance(target, cs.CreatureCard):
            target.toughness -= self.damage
            print(f"{card.name} does {self.damage} damage to {target.name}")
        else:
            ""
            print(f"{target.name} is not a valid target")

# Mēģināju pēc analoģijas interes pēc pievienot power/toughness mainītāju, kas strādā gan ar +, gan -. 
# Idejiski gan šis pagaidām pamaina paliekoši, nevis tikai līdz gājiena beigām.
class ApplyBuffs:
    def __init__(self, power_change=0, toughness_change=0):
        self.power_change = power_change
        self.toughness_change = toughness_change
    
    def apply(self, card, target):
        if isinstance(target, cs.CreatureCard):
            if self.power_change != 0:
                target.power += self.power_change
                print(f"{card.name} gives {self.power_change} power to {target.name}")
            if self.toughness_change != 0:
                target.toughness += self.toughness_change
                print(f"{card.name} gives {self.toughness_change} toughness to {target.name}")
        else:
            ""
            print(f"{target.name} is not a valid target")

class Prowess:
    def apply(creature: cs.CreatureCard, player):
        # Apply the +1/+1 effect to the creature
        creature.power += 1
        creature.toughness += 1
        print(f"{creature.name} got +1/+1 until end of turn from Prowess")

class Prowess_Slickshot: 
    def apply(creature: cs.CreatureCard, player):
        # Apply the +2/+0 effect to the creature
        creature.power += 2
        creature.toughness += 0
        print(f"{creature.name} got +2/+0 until end of turn from Prowess_Slickshot")

class Valiant_Heartfire:        # Fak, šim vajag aktivizēties arī no Manifold Mouse targeted efekta
    def apply(creature: cs.CreatureCard, player):
        if creature.spell_targeted == False:
            creature.counter_power += 1
            creature.counter_toughness += 1
            creature.spell_targeted = True

    