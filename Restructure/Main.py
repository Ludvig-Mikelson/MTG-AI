import Engine as en
import Classes as cs
import random
import math

# Initialize players and game state
player1 = en.player1
player2 = en.player2
state = en.GameState(player_AP=player1, player_NAP=player2, stack=[])


def get_action_key(action):
    """
    Convert an action to a consistent, hashable key.
    """
    if isinstance(action, dict):
        return (
            action.get('type'),
            id(action.get('id')),  # Use `id()` to get a unique hashable identifier
            action.get('name'),
            id(action.get('player')),  # Use `id()` to hash the player object
        )
    return action


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
        print(f"Legal actions: {legal_actions}")
        legal_action_keys = {get_action_key(action) for action in legal_actions}
        return legal_action_keys.issubset(set(self.children.keys()))
    
    def best_child(self, c_param=1.4):
        """Selects the child with the highest UCB value."""
        if not self.children:
            raise ValueError("No children to select from.")
        return max(
            self.children.items(),
            key=lambda item: (
                item[1].total_value / item[1].visit_count if item[1].visit_count > 0 else float('inf')
                + c_param * (math.sqrt(math.log(self.visit_count) / (item[1].visit_count or 1)))
            ),
        )[1]

    def get_child_node_for_action(self, action):
        """
        Retrieve the child node corresponding to a specific action.
        """
        action_key = get_action_key(action)
        return self.children.get(action_key, None)


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

        # Expansion: Add a new node if possible
        if not node.is_fully_expanded():
            actions = node.state.legal_actions()
            if not actions:
                actions = [False]  # Default action if no legal actions exist

            for action in actions:
                action_key = get_action_key(action)
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
            print(node)
            print(f"Backpropagating reward: {reward}, Node visits: {node.visit_count}, Total value: {node.total_value}")
            node.visit_count += 1
            node.total_value += reward
            print(f"Updated Node: Visits={node.visit_count}, Total Value={node.total_value}")
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


def play_game_with_mcts(ai_player, max_simulations=100):
    """
    Main game loop to play a game using Monte Carlo Tree Search for the AI player.
    """
    game_state = en.GameState(player_AP=player1, player_NAP=player2, stack=[])
    root = MCTSNode(game_state, parent=None)

    while not game_state.is_terminal():
        print(f"\nCurrent Phase: {game_state.phase}")
        print(f"{game_state.player_AP.name} Life: {game_state.player_AP.life}, {game_state.player_NAP.name} Life: {game_state.player_NAP.life}")
        current_player = game_state.player_S
        print(f"Current Player: {'AI' if current_player == ai_player else 'Opponent'}")
        legal_actions = game_state.legal_actions()

        if game_state.phase in ["begin phase", "end phase", "first phase"]:
            en.change_phase(game_state)

        if not legal_actions or legal_actions == [False]:
            print("No valid actions. Passing priority.")
            game_state.execute_action(False)
            continue

        if current_player == ai_player:
            print("AI is thinking...")
            try:
                best_action = mcts_search(root, max_simulations, ai_player)
                print(f"AI chooses action: {best_action}")
                game_state.execute_action(best_action)
            except Exception as e:
                print(f"Error during AI decision-making: {e}")
                game_state.execute_action(False)  # Fallback to passing priority
        else:
            print("Opponent is thinking...")
            opponent_action = random.choice(legal_actions)
            print(f"Opponent chooses action: {opponent_action}")
            game_state.execute_action(opponent_action)

        if game_state.is_terminal():
            break

        root = root.get_child_node_for_action(game_state) or MCTSNode(game_state, parent=None)

    game_state.determine_winner()
    print("\nGame Over!")
    if game_state.winner == ai_player:
        print(f"AI {game_state.winner.name} wins!")
    elif game_state.winner is None:
        print("It's a draw!")
    else:
        print(f"Opponent {game_state.winner.name} wins!")


play_game_with_mcts(player1)
