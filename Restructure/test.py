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
            if ucb_score > best_score:
                
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

# Modify the get_result method to accept dynamic parameters for optimization
def custom_get_result(state, ai_player, coeff_board_self, coeff_board_opponent, coeff_life_opponent, coeff_life_self):
    score = 0
    if state.player_S.name == ai_player.name:
        if state.player_NS.life <= 0:
            score += 1
        elif state.player_S.life <= 0:
            score -= 1
        else:
            score += len(state.player_S.board) * coeff_board_self
            score -= len(state.player_NS.board) * coeff_board_opponent
            score += (20 - state.player_NS.life) * coeff_life_opponent
            score += (state.player_S.life - 20) * coeff_life_self
    else:
        if state.player_S.life <= 0:
            score += 1
        elif state.player_NS.life <= 0:
            score -= 1
        else:
            score += len(state.player_NS.board) * coeff_board_self
            score -= len(state.player_S.board) * coeff_board_opponent
            score += (20 - state.player_S.life) * coeff_life_opponent
            score += (state.player_NS.life - 20) * coeff_life_self
    return score

# Simulate function for random game play (modified to use custom_get_result with dynamic coefficients)
def simulate(state, ai, max_depth, coeff_board_self, coeff_board_opponent, coeff_life_opponent, coeff_life_self):
    stato = copy.deepcopy(state)
    if stato.action_taken and stato.action_taken["type"] == "pass":
        return 0
    i = 0
    while not stato.is_terminal() and i < max_depth:

        legal_actions = stato.legal_actions()
        action = random.choice(legal_actions)
        #print(f"{legal_actions} HERE")
        #print(action)
        stato.execute_action(action)
        i += 1
    return custom_get_result(stato, ai, coeff_board_self, coeff_board_opponent, coeff_life_opponent, coeff_life_self)

# MCTS function (modified to pass optimized coefficients)
def mcts(root, ai, iterations=10, max_depth=25, coeff_board_self=0.03, coeff_board_opponent=0.03, coeff_life_opponent=0.06, coeff_life_self=0.05):
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
        result = simulate(node.state, ai, max_depth=max_depth, coeff_board_self=coeff_board_self, coeff_board_opponent=coeff_board_opponent,
                          coeff_life_opponent=coeff_life_opponent, coeff_life_self=coeff_life_self)
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


######
# Parametru optimizācija:

import optuna


def objective(trial):
    # Suggest values for parameters
    coeff_board_self = trial.suggest_float("coeff_board_self", 0.01, 0.1)
    coeff_board_opponent = trial.suggest_float("coeff_board_opponent", 0.01, 0.1)
    coeff_life_opponent = trial.suggest_float("coeff_life_opponent", 0.01, 0.1)
    coeff_life_self = trial.suggest_float("coeff_life_self", 0.01, 0.1)

    max_depth = 15
    num_iterations = 20
    simulations = 20  # Number of games to simulate for evaluation

    ai = player2
    wins = 0
    losses = 0
    not_finished = 0
    for i in range(simulations):
        initial_state = state
        root = Node(initial_state)

        while not root.state.is_terminal():
            if root.state.player_S.name == ai.name:
                
                #print(f"{root.state.player_S}")
                #print(f"{root.state.player_NS}")

                root = mcts(root, ai, iterations=num_iterations, max_depth=max_depth, coeff_board_self=0.02, 
                            coeff_board_opponent=0.02, coeff_life_opponent=0.5, coeff_life_self=0.065)

            else:
                actions = root.state.legal_actions()
                action = random.choice(actions)
                #acts.append(f"Best action: {action} NON AI")
                root.state.execute_action(action)
                        

        # print(f"{root.state.player_AP.name}  {root.state.player_AP.life}")
        # print(f"{root.state.player_NAP.name}  {root.state.player_NAP.life}")
        ##print(root.state.winner.name)
        ##print(ai.name)

        if i%5 ==0:
            print(i)
        
        if root.state.winner == None:
            not_finished += 1
            
        elif root.state.winner.name == ai.name:
            wins += 1
        
        elif root.state.winner.name == player1.name:
            losses += 1
            
    print("AI wins:", wins)
    print("AI losses:", losses)
    print("not finished:", not_finished)


    # Return win rate as the objective to maximize
    return wins / simulations



# Run Optuna study
if __name__ == "__main__":
    study = optuna.create_study(
        direction="maximize",
        storage="sqlite:///optuna_study.db",  # Save results in SQLite
        load_if_exists=True
    )
    study.optimize(objective, n_trials=100)

    # Display best parameters and results
    print("Best parameters:", study.best_params)
    print(f"Best win rate: {study.best_value*100:.1f}%")





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