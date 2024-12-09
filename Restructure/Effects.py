import random
import Classes as cs
import Card_Registry as cr


class GainManaEffect:
    def __init__(self, mana_amount=1):
        self.mana_amount = mana_amount

    def apply(self, player):
        # This effect adds mana to the player's mana pool
        player.mana_pool += self.mana_amount
        #print(f"{player.name} gains {self.mana_amount} mana! Current mana: {player.mana_pool}")
        
class Spawn:
    def __init__(self, token_name = False):
        self.token = cr.card_factory(token_name,"Creature")
    
    def apply(self,player):
        player.board.append(self.token)
        #print(f"{player.name} spawns {self.token.name}")
        
class DmgToAny:
    def __init__(self, damage = 0):
        self.damage = damage
        
    def apply(self, card, target):
        #print(card)
        #print(target)
        if isinstance(target,cs.Player):
            if self.damage > 0:         # The case when damage can be defined at start
                damage = self.damage
            target.life -= damage
            #print(f"{card.name} does {damage} damage to {target.name}")
            #print(f"{target.name} has {target.life} life left")
        elif isinstance(target, cs.CreatureCard):
            if self.damage > 0:         # The case when damage can be defined at start
                damage = self.damage
            target.toughness -= damage
            #print(f"{card.name} does {damage} damage to {target.name}")
        else:
            g=1
            #print(f"{target.name} is not a valid target")

# Mēģināju pēc analoģijas interes pēc pievienot power/toughness mainītāju, kas strādā gan ar +, gan -. 
class ApplyBuffs:
    def __init__(self, power_change=0, toughness_change=0):
        self.power_change = power_change
        self.toughness_change = toughness_change
    
    def apply(self, card, target):
        if isinstance(target, cs.CreatureCard):
            target.power += self.power_change
            target.toughness += self.toughness_change
            #print(f"{card.name} gives +{self.power_change}/+{self.toughness_change} to {target.name}")
        else:
            g=1
            #print(f"{target.name} is not a valid target")

class Prowess:
    def apply(self,creature: cs.CreatureCard):       #Man meta erroru ka par maz parametru, ķipa vajadzēja lietot arī self
        # Apply the +1/+1 effect to the creature
        creature.power += 1
        creature.toughness += 1
        #print(f"{creature.name} got +1/+1 until end of turn from Prowess")

class Prowess_Slickshot: 
    def apply(self,creature: cs.CreatureCard):
        # Apply the +2/+0 effect to the creature
        creature.power += 2
        creature.toughness += 0
        #print(f"{creature.name} got +2/+0 until end of turn from Prowess_Slickshot")

class Valiant_Heartfire:        # Šim vajag aktivizēties arī no Manifold Mouse targeted efekta
    def apply(creature: cs.CreatureCard):
        if creature.spell_targeted == False:
            creature.counter_power += 1
            creature.counter_toughness += 1
            creature.spell_targeted = True
            #print(f"Valiant Heartfire buffed {creature.name}")


class Valiant_Emberheart:
    def apply(creature: cs.CreatureCard, player):
        #print("Valiant Emberheart called")
        if creature.spell_targeted == False:
            player.deck.pop()
            # Jāpieliek, ka var izspēlēt līdz gājiena beigām
            creature.spell_targeted = True
            #print(f"Valiant Emberheart activated from {creature.name}")

class Offspring:
    def __init__(self, mana_cost):
        self.mana_cost = mana_cost
    
    def apply(self, card, player):
        if player.mana_pool >= self.mana_cost:
            if random.choice([0,1]) == 1:
                #print(f"{player.name} used Offspring")
                player.mana_pool -= self.mana_cost
                offspring = Spawn("Manifold Mouse Token")
                offspring.apply(player)                     # creates and plays the token

class Might_of_the_Meek:
    def apply(self, card, target: cs.CreatureCard, player):
        if isinstance(target, cs.CreatureCard):
            target.trample_eot = True
            controlled_mouses = [creature for creature in player.board if creature.is_mouse == True]
            #print(f"{card.name} gave Trample to {target.name} until EOT. ")
            if controlled_mouses:
                target.power += 1
                #print(f"and {target.name} also received +1/+0 from {card.name} since {player.name} is controlling a Mouse")
        else:
            g=1
            #print(f"{target.name} is not a valid target")

class Demonic_Aura:
    def apply(self, card, creature: cs.CreatureCard):    # self?
        creature.counter_power += 1         # So it could be a perma buff
        creature.counter_toughness += 1
        creature.menace = True              # Both also permanent
        creature.trample = True
        creature.auras += [Demonic_Aura]
        #print(f"{card.name} buffed and applied an Aura to {creature.name}")

    def leaves_battlefield(player):
        # draw_card(player)
        g=1
                        # vajag draw_card, bet laikam ne šeit, bet enginā.
        #print(f"{player.name}'s Demonic Aura left the battlefield, needs to draw a card.")


        
