import math
import random
import Engine as en
import Classes as cs
import Card_Registry as cr
import copy

deck1 = en.build_deck(cr.creature_list, cr.instant_list)
deck2 = en.build_deck(cr.creature_list, cr.instant_list)
start_hand1 = deck1[:7]
start_hand2 = deck2[:8]
deck1 = deck1[7:]
deck2 = deck2[8:]
        
player1 = copy.deepcopy(cs.Player("Bob", start_hand1, deck1, [], [], [], 0, 10))
player2 = copy.deepcopy(cs.Player("Alice", start_hand2, deck2, [], [], [], 0, 10))
state = en.GameState(player_AP=player1, player_NAP=player2, stack=[])


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        
        
    def is_fully_expanded(self):
        """Check if all possible actions have been tried."""
        tried_actions = [child.state.action_taken for child in self.children]
        all_actions = self.state.legal_actions()
        # Do this by id right now actions are added to tried, but not removed from untried. Do the same bellow
        #print(f"TEST {all_actions}")

        tried_action_id = {action["id"] for action in tried_actions}
        untried_actions = [
            action for action in all_actions if action["id"] not in tried_action_id
        ]
            
        #print(f"Tried action IDs {tried_action_id}")
        #print(f"Tried actions {tried_actions} LENGTH ({len(tried_actions)})")
        #print(f"Untried actions {untried_actions} LENGTH ({len(untried_actions)})")
        #print(f"All actions {all_actions} LENGTH ({len(all_actions)})")

            
        return len(untried_actions) == 0

    def best_child(self, exploration_weight=0.5):
        """Choose the best child node based on UCB."""
        best_score = -float('inf')
        best_child = None
        
        for child in self.children:
            
            # Calculate UCB score
            exploitation = child.value / (child.visits + 1e-6)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            ucb_score = exploitation + exploration
            #print(f"Child Value: {child.value}")
            #print(f"Child Visits: {child.visits}")
            #print(f"UCB Score: {ucb_score}")
            #print(f"Action Taken: {child.state.action_taken}")
            score_list = []
            if ucb_score >= best_score:
                
                best_score = ucb_score
                best_child = child
                
        
        return best_child

    def update(self, result):
        """Update the node with the result of a simulation."""
        self.visits += 1
        self.value += result

    def expand(self):
        """Expand a node by creating a new child for an untried action."""
        new_state = copy.deepcopy(self.state)
        tried_actions = [child.state.action_taken for child in self.children]
        tried_action_id = {action["id"] for action in tried_actions}
        untried_actions = [
                action for action in new_state.legal_actions() if action["id"] not in tried_action_id
            ]
        #print("\n gg \n gg")
        #print(f"Tried actions {tried_actions} LENGTH ({len(tried_actions)})")
        #print(f"Untried actions {untried_actions} LENGTH ({len(untried_actions)})")
        #print(f"All actions {self.state.legal_actions()} LENGTH ({len(self.state.legal_actions())})")
        
        if not untried_actions:
            return self  # No actions to expand
        action = random.choice(untried_actions)

        
        new_state.execute_action(action)
        new_state.action_taken = action
        child_node = Node(new_state, parent=self)
        
        

        self.children.append(child_node)
        
        #print(child_node)
        #print(self.children)
        
        return child_node


def simulate(state, ai):
    """Simulate a random game from the given state."""
    stato = copy.deepcopy(state)
    if stato.action_taken["type"] == "pass":
        return 0
    i = 0
    while not stato.is_terminal() and i < 25:

        legal_actions = stato.legal_actions()
        action = random.choice(legal_actions)
        #print(f"{legal_actions} HERE")
        #print(action)
        stato.execute_action(action)
        #print(f"{stato.get_result(ai)} this")
        i+=1
    return stato.get_result(ai)

def mcts(root,ai, iterations=10):
    """Perform MCTS to find the best action."""
    
    for _ in range(iterations):
        node = root
        
        random.shuffle(node.state.player_S.deck)
        random.shuffle(node.state.player_NS.deck)
        #print(node)
        # Selection
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
            #print(node)
        # Expansion
        if not node.state.is_terminal():

            node = node.expand()
            #print(node)
        # Simulation
        result = simulate(node.state, ai)
        #print(result)
        # Backpropagation
        while node.parent is not None:
            #print(f"Player AP {node.state.player_AP.name}")
            #print(f"Player NAP {node.state.player_NAP.name}")
            #print(f"Action Taken {node.state.action_taken}")
            node.update(result)
            node = node.parent
            #print("g")
        
        node.update(result)
            
            
    return root.best_child(exploration_weight=0.0)


if __name__ == "__main__":
    ai = player1
    wins = 0
    not_finished = 0
    acts = []
    for _ in range(0,10,1):

        initial_state = state
        root = Node(initial_state)
        
        if ai == player1:
            training_data = [initial_state]
        else:
            training_data = []
            
        i=0
        while not root.state.is_terminal(): #and i < 200:
            if root.state.player_S.name == ai.name:
                
                #print(f"{root.state.player_S}")
                #print(f"{root.state.player_NS}")
                root = mcts(root,ai, iterations=5)
                
                root_copy = copy.deepcopy(root)
                training_data.append(root_copy.state)
                
                if root:
                    if root.state.action_taken:
                        acts.append(f"Best action: {root.state.action_taken["type"]} value {root.value} phase {root.state.phase}, #{i}")
                        #print(f"{root.state.action_taken}")
                        
                        #print("STOP")
                    else:
                        acts.append(f"Best action: {root.state.action_taken}")
                        
                    #print(root.value)
                
            else:
 
                actions = root.state.legal_actions()
                action = random.choice(actions)
                #acts.append(f"Best action: {action} NON AI")
                root.state.execute_action(action)
            
            i+=1


        






        print(f"{root.state.player_AP.name}  {root.state.player_AP.life}")
        print(f"{root.state.player_NAP.name}  {root.state.player_NAP.life}")

        if root.state.winner == None:
            reward = 0
            not_finished += 1
            
        elif root.state.winner.name == ai.name:
            wins += 1
            reward = 1
        else:
            reward = -1
            
            
        while root_for_val is not None:
            state = root_for_val.state
            root_for_val = root_for_val.parent
            
            
            
   
    print(acts)
    print(wins)
    print(not_finished)


"""
bob = 0
alice = 0
for _ in range(0,100,1):

    stato = copy.deepcopy(state)
    random.shuffle(stato.player_AP.deck)
    random.shuffle(stato.player_AP.hand)
    
    random.shuffle(stato.player_NAP.deck)
    random.shuffle(stato.player_NAP.hand)

    while not stato.is_terminal():
        
        actions = stato.legal_actions()
        action = random.choice(actions)
        stato.execute_action(action)

    stato.determine_winner()

    if stato.winner.name == "Bob":
        bob+=1
    elif stato.winner.name == "Alice":
        alice+=1
        
#print(bob)
#print(alice)
"""