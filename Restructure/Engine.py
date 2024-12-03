# %% 
import Classes as cs
import Effects as ef
import Card_Registry as cr
import random
import copy



  
def build_random_deck(deck_size=60):
    card_names = list(cr.Creature_Card_Registry.keys())  
    land_card_names = list(cr.Land_Card_Registry.keys())
    sorcery_card_names = list(cr.Instant_Card_Registry.keys())
    deck = []
    
    for _ in range((deck_size-30)):
        card_name = random.choice(card_names)  # Randomly select a card name
        card = cr.card_factory(card_name,"Creature")  # Create a unique instance of the card
        deck.append(card)  # Add the card to the deck
       
    for _ in range(20):
        land_card_name = random.choice(land_card_names)  
        card = cr.card_factory(land_card_name,"Land")  
        deck.append(card) 
        
    for _ in range(10):
        sorcery_card_name = random.choice(sorcery_card_names)  
        card = cr.card_factory(sorcery_card_name,"Instant")  
        deck.append(card)         
    
    random.shuffle(deck)

    return deck
    
    
def draw_card(player):
    if len(player.deck) > 0:
        player.hand.append(player.deck.pop())  
        print(f"{player.name} draws a card")   
    else:
        print("No more cards")
    hand=[]
    for card in player.hand:
        hand.append(card.name)
    print(player.name,"'s hand: ", hand)
        

    
def begin_phase(state):
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0    
    state.phase = "begin phase"
    state.player_AP.played_land = False
    for land in state.player_AP.land_board:
        land.tapped = False
    for creature in state.player_AP.board:
        creature.tapped = False
    
    draw_card(state.player_AP)
    
    print("Begin Phase")

    
def main_phase_1(state):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    
    # Resets passed so that phase doesn't auto end if the first player passes
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "main phase 1"
    print(f"{state.player_AP.name} Main Phase 1")
 
 
# Battle phase is divided in 3 phases, one where AP can declare attacks, one where NAP can declare blocks and one where it resolves
# Attack and block phases have subphases defined later in the code   
def attack_phase(state):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "declare attack phase"
    print(f"{state.player_AP.name} declare attack phase")
    
def block_phase(state):
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "declare block phase"
    print(f"{state.player_AP.name} declare block phase")    
    
def resolve_phase(state):
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "resolve battle phase"
    print(f"{state.player_AP.name} resolve battle phase")  
    
                
def main_phase_2(state):
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0

    state.phase = "main phase 2"
    print(f"{state.player_AP.name} Main Phase 2")
    
            

    
def reset_creatures(player: cs.Player):
    # Reset creatures on the player's board
    for creature in player.board:
        if isinstance(creature,cs.CreatureCard):
            creature.power = creature.og_power + creature.counter_power
            creature.toughness = creature.og_toughness + creature.counter_toughness
            creature.attacking = False
            creature.blocking = False 
            creature.blocked_creature_id = None
            creature.spell_targeted = False

    # Reset creatures in the player's graveyard
    for creature in player.graveyard:
        if isinstance(creature,cs.CreatureCard):
            creature.power = creature.og_power
            creature.toughness = creature.og_toughness
            creature.attacking = False
            creature.blocking = False
            creature.blocked_creature_id = None
            
def end_phase(state):
    state.phase = "end phase"
    
    reset_creatures(state.player_AP)
    reset_creatures(state.player_NAP)
    
    ap_copy = state.player_AP
    nap_copy = state.player_NAP
    
    # Swaps between AP and NAP aka changed turn
    state.player_AP = nap_copy
    state.player_NAP = ap_copy
    
    
def resolve_combat(GameState):
    
    creatures = GameState.player_AP.board
    
    for attacker in creatures:
        if attacker.attacking:
            if attacker.blockers:
                for blocker in attacker.blockers:
                    
                    
                    if attacker.power <= 0:
                        attacker.power = 0
                    if attacker.toughness <= 0:
                        attacker.toughness = 0
                    if blocker.toughness <= 0:
                        blocker.toughness = 0    
                        
                    print(f"{blocker.power}/{blocker.toughness} {blocker.name} is blocking {attacker.power}/{attacker.toughness} {attacker.name}")
                    
                    bt = blocker.toughness
                    ap = attacker.power
                    bp = blocker.power
                        
                    blocker.toughness -= ap
                    attacker.toughness -= bp
                    attacker.power -= bt
                
                # When Trample is ready this can be uncommented
                #if attacker.trample:
                    #GameState.player_NAP.life -= attacker.power
            else:
                
                print(f"{attacker.power}/{attacker.toughness} {attacker.name} deals damage to the {GameState.player_NAP.name}.")
                GameState.player_NAP.life -= attacker.power
                print(f"{GameState.player_NAP.name} has {GameState.player_NAP.life} life left")
                
    for creature in GameState.player_AP.board:
        if creature.toughness <= 0:
            creature.leaves_battlefield(GameState.player_AP)
            
    for creature in GameState.player_NAP.board:
        if creature.toughness <= 0:
            creature.leaves_battlefield(GameState.player_NAP)
                
    
    
# Dictonary for when change_phase function gets called, maps next phase function to the current phase
phase_actions = {
    "first phase": begin_phase,
    "begin phase": main_phase_1,
    "main phase 1": attack_phase,
    "declare attack phase": block_phase,
    "after attack": block_phase,
    "declare block phase": resolve_phase,
    "after block": resolve_phase,
    "resolve battle phase": main_phase_2,
    "main phase 2": end_phase,
    "end phase": begin_phase
}






deck1 = build_random_deck()
deck2 = build_random_deck()
start_hand1 = deck1[:7]
start_hand2 = deck2[:7]
deck1 = deck1[7:]
deck2 = deck2[7:]
    
player1 = cs.Player("Bob", start_hand1, deck1, [], [], [], 0, 20)
player2 = cs.Player("Alice", start_hand2, deck2, [], [], [], 0, 20)
players = [player1, player2]



# Legal action functions, not perfectly optimized, but do seem to work
def play_creature_legal_actions(player_s, actions):
        # Add creature actions
    for creature in player_s.hand:
        if isinstance(creature, cs.CreatureCard) and creature.mana_cost <= player_s.mana_pool:
            actions.append({
                "type": "creature",
                "id": creature.id,
                "name": creature.name,
                "player": player_s,
                "target": None,
                "action": creature.play,
                "cost": creature.mana_cost
            })


def play_instant_legal_actions(player_s, player_ns, actions):

    targets = player_ns.board + player_s.board + [player_s, player_ns]
    
            
        
        
        
        # Add instant actions
    for instant in player_s.hand:
        if isinstance(instant, cs.InstantCard) and instant.mana_cost <= player_s.mana_pool:
            if instant.name == "Monstrous Rage":    
                targets = player_ns.board + player_s.board
            
            # bad way to solve the fact that monstrous rage can't target face
            if instant.name == "Monstrous Rage" and not player_ns.board + player_s.board:
                continue
            
            else:
                for target in targets:
                    actions.append({
                        "type": "instant",
                        "id": instant,
                        "name": instant.name,
                        "player": player_s,
                        "target": target,
                        "action": instant.play,
                        "cost": instant.mana_cost
                    })

def play_land_legal_actions(player_s, actions):
    
    for land in player_s.hand:
        if isinstance(land, cs.LandCard) and player_s.played_land == False:
            actions.append({
                "type": "land",
                "id": land,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": land.play,
                "cost": 0
            })
            
def tap_land_legal_actions(player_s, actions):
        # Add tap land actions
    for land in player_s.land_board:
        if not land.tapped:
            actions.append({
                "type": "tap land",
                "id": land.id,
                "name": land.name,
                "player": player_s,
                "target": None,
                "action": land.tap,
                "cost": 0
            })
            
def target_instant_legal_actions(player_s, player_ns, instant_to_target, actions):
    
    # again bad fix for monstrous rage
    if instant_to_target["name"] == "Monstrous Rage":
        players = []
    else:
        players = [player_ns, player_s]
    
    
    if instant_to_target:
        for target in players + player_ns.board + player_s.board:
            
            
            actions.append({
                "type": "instant",
                "id": instant_to_target["id"],  
                "name": instant_to_target["name"],
                "player": instant_to_target["player"],
                "target": target,
                "action": instant_to_target["action"],
                "cost": instant_to_target["cost"] 
                })
    return actions

def attack_legal_actions(player_AP,actions):
    
    creatures = player_AP.board
    for creature in creatures:
        if creature.tapped == False and creature.attacking == False:
            actions.append({
                "type": "attack",
                "id": creature.id,  
                "name": creature.name,
                "player": player_AP,
                "target": None,
                "action": creature.attack,
                "cost": 0
                })
    
def block_legal_actions(player_AP, player_NAP, actions):
    
    creatures_ap = player_AP.board
    creatures_nap = player_NAP.board
    
    for creature_blk in creatures_nap:
        if creature_blk.tapped == False and creature_blk.blocking == False:
            for creature_atk in creatures_ap:
                if creature_atk.attacking == True:
                    actions.append({
                        "type": "block",
                        "id": creature_blk.id,  
                        "name": creature_blk.name,
                        "player": player_NAP,
                        "target": creature_atk,
                        "action": creature_blk.block,
                        "cost": 0 
                        })
    


            
            
            
def choose_action(action, GameState):
    #print("Choose Action")
    
    # If there are any actions that can be made randomly choose to take random action or not
    print(f"{GameState.player_S.name}'s priority")
    if action:
        
        
        # If the action is an instant choose the target first
        if action["type"] == "instant":
        
                # Remove from hand before playing so that it can't be played multiple times (bad solution)
                action["player"].hand.remove(action["id"])
                
            
        # Once the first attack declaration is made, only attack declarations can be made    
        elif action["type"] == "attack" and GameState.player_AP.passed == False:
            action["action"](action["player"])
            GameState.phase = "just attacks"
            action = None
            
        # Same but for blocks 
        elif action["type"] == "block" and GameState.player_NAP.passed == False:
            action["action"](action["player"],action["target"]) # adjust for actual declare block function
            GameState.phase = "just blocks"
            action = None
        
        # playing lands and tapping lands doesn't go to stack so activate it here and give prio to the player_s    
        elif action["type"] == "land" or action["type"] == "tap land":
            
            action["action"](action["player"])
            GameState.reset_prio = True
            action = None
            
        
            
        #print(GameState.phase)
        # Adjust this when action can be skipped
        if action != None:
            GameState.player_S.mana_pool -= action["cost"]
            print(f"{action["player"].name}, {action["type"]}")
            GameState.stack.append(action)
    
            
            
    # If the player choosing to attack or block doesn't, move to after phase where no blcoks or attacks can be declared      
    elif GameState.phase == "just attacks":
        GameState.phase = "after attack"
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
        GameState.reset_prio = True
        
    elif GameState.phase == "just blocks":
        GameState.phase = "after block"
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
        GameState.reset_prio = True

    
        
    else:
        GameState.player_S.passed = True
        print(f"{GameState.player_S.name} passed")
        
 
    
def execute_stack(GameState):
    #print("Execute Stack")
    # Stack is executed in reverse order from play order
    stack = list(reversed(GameState.stack))
    
    print(stack)
    for action in stack:
        
        if action["target"] is not None:
            
            #print(action["action"])
            action["action"](action["player"], action["target"])
        else:
            #print(action["target"])
            action["action"](action["player"])
            
    
    # Reset prio and stack        
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP
    GameState.stack = []
        

def change_phase(GameState):
    #print("Change Phase")
    
    current_phase = GameState.phase
    phase_actions[current_phase](GameState)
    
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP


#def add_to_stack(GameState):
    #print("Add to Stack")
    #actions = legal_actions(GameState)
    #action = choose_action(actions, GameState)
    
    
    #if action:
        #GameState.stack.append(action) 
    
    



class GameState:
    def __init__(self, player_AP: cs.Player, player_NAP: cs.Player, 
                 stack: list):
        self.player_AP = player_AP
        self.player_NAP = player_NAP
        self.player_S = player_AP
        self.player_NS = player_NAP
        self.stack = stack
        self.phase = "first phase"
        self.reset_prio = False
        self.winner = None
        
    def get_result(self):
        
        if self.winner == self.player_AP:
            return +1
        elif self.winner == self.player_NAP:
            return -1
        return 0
        
    def is_terminal(self):
        return self.winner is not None
        
    def determine_winner(self):
        if self.player_AP.life <= 0:
            self.winner = self.player_NAP
        elif self.player_NAP.life <= 0:
            self.winner = self.player_AP
        else:
            self.winner = None 
            
            
    def copy(self):
        
        return GameState(
            player_AP=copy.deepcopy(self.player_AP),
            player_NAP=copy.deepcopy(self.player_NAP),
            stack=copy.deepcopy(self.stack)
        )
        
        
    def legal_actions(self):
        actions = []
        player_ns = self.player_NS
        player_s = self.player_S
        phase = self.phase
        player_ap = self.player_AP
        player_nap = self.player_NAP

        
        
        if phase == "main phase 1" or phase == "main phase 2":
            
            if player_s == player_ap and not self.stack:
                # tap land actions
                tap_land_legal_actions(player_s, actions)

                # play land actions
                play_land_legal_actions(player_s, actions)
                
                # play creature actions
                play_creature_legal_actions(player_s, actions)
                
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
                
            else:
                # tap land actions
                tap_land_legal_actions(player_s, actions)
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
                
            
        elif phase == "declare attack phase":
            
            if player_s == player_ap:
                # tap land actions
                tap_land_legal_actions(player_s, actions)
                
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
                
                # declare attack actions
                attack_legal_actions(player_ap, actions)
                
            elif player_s == player_nap:
                # tap land actions
                tap_land_legal_actions(player_s, actions)
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
        
        elif phase == "declare block phase":
            
            if player_s == player_ap:
                # tap land actions
                tap_land_legal_actions(player_s, actions)
                
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
                
            elif player_s == player_nap:
                # tap land actions
                tap_land_legal_actions(player_s, actions)
                
                # play instant actions
                play_instant_legal_actions(player_s, player_ns, actions)
                
                # declare block acions
                block_legal_actions(player_ap, player_nap, actions)
            
            
        elif phase == "resolve battle phase":
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, player_ns, actions)
            
        elif phase == "just attacks":
            
            # declare attack actions
            # Only the AP can declare attakcs
            attack_legal_actions(player_ap, actions)
        
        # Once attacks are declared, players have a chance to cast instants same with after block   
        elif phase == "after attack":
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, player_ns, actions)
            
        elif phase == "just blocks":
            
            if player_s == player_nap:
                # declare block acions
                block_legal_actions(player_ap, player_nap, actions)
            
        elif phase == "after block":
            # tap land actions
            tap_land_legal_actions(player_s, actions)
            
            # play instant actions
            play_instant_legal_actions(player_s, player_ns, actions)
            
            
            
        if not actions:
            actions = [False]
            

        return actions
    
    def execute_action(self,action):
    #print("Main Action")
    
        if self.player_AP.life <= 0:
            self.winner = self.player_NAP.life
            
        elif self.player_NAP.life <= 0:
            self.winner = self.player_AP.life
            
        else:
            
            choose_action(action,self)
            
            # Execute stack if both players passed and there is anything to execute    
            if self.stack and self.player_AP.passed and self.player_NAP.passed:
                #print("Execute stack if both players passed")
                execute_stack(self)
                
            # Change phase if no stack and both players pass        
            elif not self.stack and self.player_AP.passed and self.player_NAP.passed:
                #print("Change Phase if both players passes and no actions")
                
                if self.phase == "resolve battle phase":
                    resolve_combat(self)
                
                change_phase(self)
            
            # Keep prio on attacker or blocker during the just attacks/blocks phase 
            elif self.reset_prio == True:
                #print("prio is reset")

                self.player_S = self.player_AP
                self.player_NS = self.player_NAP
                self.reset_prio = False
                self.player_AP.passed = False
                self.player_NAP.passed = False
            
            # Switch between player adding to the stack
            else:

                #print("Prio is switched")
            
                self.player_S_copy = self.player_NS
                self.player_NS_copy = self.player_S

                self.player_S = self.player_S_copy
                self.player_NS = self.player_NS_copy
    
    

        
    