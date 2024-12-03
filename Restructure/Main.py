import Engine as en
import Classes as cs
import random
import math

# Initialize players and game state
player1 = en.player1
player2 = en.player2
state = en.GameState(player_AP=player1, player_NAP=player2, stack=[])



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

def mcts_search(root, simulations=100, ai_player=None):
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

    if not node.is_fully_expanded():
    
        actions = node.state.legal_actions()
        if not actions:
            actions = [False]  # Default action if no legal actions exist

        for action in actions:
            action_key = False if action is False else tuple(sorted(action.items())) if isinstance(action, dict) else action
            if action_key not in node.children:
                next_state = node.state.copy()
                print(action)
                next_state.execute_action(action)
                child_node = MCTSNode(state=next_state, parent=node)
                node.children[action_key] = child_node
                print(f"Expanded new action: {action_key}")
                break

        # Simulation: Perform a rollout to determine the result
        reward = simulate_rollout(node.state.copy(), ai_player)

        # Backpropagation: Update the node values up to the root
    while node:
        # Verify reward consistency during propagation
        print(f"Backpropagating reward: {reward}, Node visits: {node.visit_count}, Total value: {node.total_value}")

        node.visit_count += 1
        node.total_value += reward
        print(f"Updated Node: Visits={node.visit_count}, Total Value={node.total_value}")
        
        # Move up to the parent node
        node = node.parent

    # Evaluate and return the best action
    print("Actions evaluated at root:")
    for action, child in root.children.items():
        print(f"Root action: {action}, Visits: {child.visit_count}, Total Value: {child.total_value}")

    # Consider only valid actions for the best action
    valid_actions = [(action, child) for action, child in root.children.items() if action is not False]
    if valid_actions:
        best_action = max(valid_actions, key=lambda item: item[1].visit_count)[0]
    else:
        print("No valid actions, defaulting to `False`.")
        best_action = False  # Default to `False` if no other actions are valid
    return best_action

def simulate_rollout(state, ai_player, max_depth=100):
    """
    Simulate a game rollout from the given state.
    """
    depth = 0
    while not state.is_terminal() and depth < max_depth:
        print("Gotta be here")
        actions = state.legal_actions()
        if actions:
            if state.player_AP == ai_player:
                action = random.choice(actions)  # Replace with better heuristic if needed
            else:
                action = random.choice(actions)
            print(f"Simulating action: {action}")
            state.execute_action(action)
        else:
            print("No legal actions, passing priority.")
            state.execute_action(False)  # Pass turn
        depth += 1
    reward = state.get_result(ai_player)
    print(f"Rollout reached terminal state. Reward: {reward}, Depth: {depth}")
    return reward


# Specify AI player
ai_player = player1  # AI is controlling player1

# Initialize MCTS root node
root = MCTSNode(state)

# Perform MCTS search
try:
    best_action = mcts_search(root, simulations=100, ai_player=ai_player)
    print(f"Best action determined by MCTS: {best_action}")
except Exception as e:
    print(f"Error during MCTS: {e}")
