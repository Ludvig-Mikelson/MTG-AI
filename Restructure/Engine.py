# %% 
import Classes as cs
import Effects as ef
import Card_Registry as cr
import random



  
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
        

    
def begin_phase(state:cs.GameState):
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

    
def main_phase_1(state:cs.GameState):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "main phase 1"
    print(f"{state.player_AP.name} Main Phase 1")
    
def attack_phase(state:cs.GameState):
    
    state.player_AP.mana_pool = 0
    state.player_NAP.mana_pool = 0
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "declare attack phase"
    print(f"{state.player_AP.name} declare attack phase")
    
def block_phase(state:cs.GameState):
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "declare block phase"
    print(f"{state.player_AP.name} declare block phase")    
    
def resolve_phase(state:cs.GameState):
    state.player_AP.passed = False
    state.player_NAP.passed = False
    
    state.phase = "resolve battle phase"
    print(f"{state.player_AP.name} resolve battle phase")  
    
                
def main_phase_2(state:cs.GameState):
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
            
def end_phase(state:cs.GameState):
    state.phase = "end phase"
    
    reset_creatures(state.player_AP)
    reset_creatures(state.player_NAP)
    
    ap_copy = state.player_AP
    nap_copy = state.player_NAP
    
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


# adjust legal action functions to include the actions themselves not string

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
        # Add instant actions
    for instant in player_s.hand:
        if isinstance(instant, cs.InstantCard) and instant.mana_cost <= player_s.mana_pool:
            print([player_ns.board + player_s.board])
            if instant.name == "Monstrous Rage" and not player_ns.board + player_s.board:
                continue
            else:
                actions.append({
                    "type": "instant",
                    "id": instant,
                    "name": instant.name,
                    "player": player_s,
                    "target": None,
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
    

def legal_actions(GameState, instant_to_target=None):
    actions = []
    player_ns = GameState.player_NS
    player_s = GameState.player_S
    phase = GameState.phase
    player_ap = GameState.player_AP
    player_nap = GameState.player_NAP

    # target instant actions
    if instant_to_target:
        target_instant_legal_actions(player_s, player_ns, instant_to_target, actions)
        return actions
    
    if phase == "main phase 1" or phase == "main phase 2":
        
        if player_s == player_ap and not GameState.stack:
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
        attack_legal_actions(player_ap, actions)
        
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
        
        
        
        
        

    return actions
            
            
            
def choose_action(actions, GameState):
    #print("Choose Action")
    
    # If there are any actions that can be made randomly choose to take random action or not
    print(f"{GameState.player_S.name}'s priority")
    if actions:
        action = random.choice(actions)
        
        # If the action is an instant choose the target first
        if action["type"] == "instant":
            if action["target"] == None:
                actions = legal_actions(GameState, instant_to_target=action)
                action = random.choice(actions)
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
            
        elif action["type"] == "land" or action["type"] == "tap land":
            
            action["action"](action["player"])
            GameState.reset_prio = True
            action = None
            
        
            
            
            
        
        
        
        
        #print(GameState.phase)
        
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
    stack = list(reversed(GameState.stack))
    
    print(stack)
    for action in stack:
        
        if action["target"] is not None:
            
            #print(action["action"])
            action["action"](action["player"], action["target"])
        else:
            #print(action["target"])
            action["action"](action["player"])
            
    
            
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP
    GameState.stack = []
        

def change_phase(GameState):
    #print("Change Phase")
    
    current_phase = GameState.phase
    phase_actions[current_phase](GameState)
    GameState.player_S = GameState.player_AP
    GameState.player_NS = GameState.player_NAP


def add_to_stack(GameState):
    #print("Add to Stack")
    actions = legal_actions(GameState)
    action = choose_action(actions, GameState)
    if action:
        GameState.stack.append(action) 
    
    
def main_action(GameState):
    #print("Main Action")
    
    add_to_stack(GameState)
    
    # Execute stack if both players passed and there is anything to execute    
    if GameState.stack and GameState.player_AP.passed and GameState.player_NAP.passed:
        #print("Execute stack if both players passed")

        execute_stack(GameState)
        
        
    
    # Change phase if no stack and both players pass        
    elif not GameState.stack and GameState.player_AP.passed and GameState.player_NAP.passed:
        #print("Change Phase if both players passes and no actions")
        
        if GameState.phase == "resolve battle phase":
            resolve_combat(GameState)
        
        change_phase(GameState)
    
    # Keep prio on attacker or blocker during the just attacks/blocks phase 
    elif GameState.reset_prio == True:
        #print("gamestate prio is reset")

        GameState.player_S = GameState.player_AP
        GameState.player_NS = GameState.player_NAP
        GameState.reset_prio = False
        GameState.player_AP.passed = False
        GameState.player_NAP.passed = False
    
    # Switch between player adding to the stack
    else:

        #print("Prio is switched")
    
        GameState.player_S_copy = GameState.player_NS
        GameState.player_NS_copy = GameState.player_S

        GameState.player_S = GameState.player_S_copy
        GameState.player_NS = GameState.player_NS_copy


    
    

        
    