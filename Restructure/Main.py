import Engine as en
import Classes as cs
import random
import math



player1 = en.player1
player2 = en.player2

state = en.GameState(player_AP=player1,player_NAP=player2,stack=[])

#for _ in range(1,100):
#    actions = state.legal_actions()
#    if actions:
#        action = random.choice(actions)
#    else:
#        action = []
#    state.execute_action(action)
    
    
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}  # Maps hashable actions to child nodes
        self.visit_count = 0
        self.total_value = 0

    def is_fully_expanded(self):
        """
        Returns True if all legal actions for the current state have been expanded.
        """
        legal_actions = self.state.legal_actions()
        legal_action_keys = {
            tuple(sorted(action.items())) if isinstance(action, dict) else action
            for action in legal_actions
        }
        return legal_action_keys.issubset(set(self.children.keys()))

    def best_child(self, c_param=1.4):
        """
        Selects the child with the highest Upper Confidence Bound (UCB).
        """
        if not self.children:
            raise ValueError("No children to select from.")
        return max(
            self.children.items(),
            key=lambda item: (
                item[1].total_value / item[1].visit_count
                + c_param * (math.sqrt(math.log(self.visit_count) / item[1].visit_count))
            ),
        )[1]



def mcts_search(root, simulations=100):
    """
    Perform Monte Carlo Tree Search starting from the root node.
    """
    for _ in range(simulations):
        node = root

        # Selection: Traverse down the tree
        while node.is_fully_expanded() and node.children:
            try:
                node = node.best_child()
            except ValueError:
                print("No children found during selection.")
                break

        # Expansion: Add a new child node for an untried action
        if not node.is_fully_expanded():
            actions = node.state.legal_actions()
            for action in actions:
                action_key = tuple(sorted(action.items())) if isinstance(action, dict) else action
                if action_key not in node.children:
                    next_state = node.state.copy()
                    next_state.execute_action(action)
                    child_node = MCTSNode(state=next_state, parent=node)
                    node.children[action_key] = child_node
                    node = child_node
                    break

        # Simulation: Perform a rollout to determine the result
        simulation_state = node.state.copy()
        depth = 0
        max_depth = 50  # Prevent infinite rollouts
        while not simulation_state.is_terminal() and depth < max_depth:
            actions = simulation_state.legal_actions()
            if actions:
                random_action = random.choice(actions)
                simulation_state.execute_action(random_action)
            else:
                simulation_state.execute_action(False)  # No legal actions, pass turn
            depth += 1
        reward = simulation_state.get_result()

        # Backpropagation: Update the node values up to the root
        while node:
            node.visit_count += 1
            node.total_value += reward
            node = node.parent

    # Return the best action based on visit count
    best_action = max(root.children.items(), key=lambda item: item[1].visit_count)[0]
    return best_action

root = MCTSNode(state)

# Initialize players and game state


# Initialize MCTS root node
root = MCTSNode(state)

# Perform MCTS search
try:
    best_action = mcts_search(root, simulations=1000)
    print(f"Best action determined by MCTS: {best_action}")
except Exception as e:
    print(f"Error during MCTS: {e}")



    

