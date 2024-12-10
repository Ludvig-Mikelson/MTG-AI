import math
import random
import Engine as en
import Classes as cs
import Card_Registry as cr
import copy
import json
import tensorflow as tf
import numpy as np
import joblib

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="trained_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the scaler for input normalization
scaler = joblib.load('scaler.pkl')

# Create Initial GameState
deck1 = en.build_deck(cr.creature_list, cr.instant_list)
deck2 = en.build_deck(cr.creature_list, cr.instant_list)
player1 = copy.deepcopy(cs.Player("Bob", [], deck1, [], [], [], 0, 10))
player2 = copy.deepcopy(cs.Player("Alice", [], deck2, [], [], [], 0, 10))
state = en.GameState(player_AP=player1, player_NAP=player2, stack=[])

training_data = []

def predict_with_tflite(input_vector):
    # Normalize the input vector
    input_vector_scaled = scaler.transform(input_vector.reshape(1, -1))

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_vector_scaled.astype(np.float32))

    # Run inference
    interpreter.invoke()

    # Get the prediction
    prediction = interpreter.get_tensor(output_details[0]['index'])
    return prediction[0][0]  # Return the scalar value



class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        
    # Check if all actions have been tried      
    def is_fully_expanded(self):
        """Check if all possible actions have been tried."""
        tried_actions = [child.state.action_taken for child in self.children]
        all_actions = self.state.legal_actions()

        tried_action_id = {action["id"] for action in tried_actions}
        untried_actions = [
            action for action in all_actions if action["id"] not in tried_action_id
        ]
            
        return len(untried_actions) == 0
    # Check which is the best child
    def best_child(self, exploration_weight=0.5):
        """Choose the best child node based on UCB."""
        best_score = -float('inf')
        best_child = None

        for child in self.children:
            input_vector = np.array(child.state.get_vector(ai))
            predicted_val = predict_with_tflite(input_vector)
            
            # MCTS vai NN
            MCTS_val = child.value
            val = predicted_val

            # Calculate UCB score
            exploitation = val / (child.visits + 1e-6)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            ucb_score = exploitation + exploration

            if ucb_score >= best_score:
                best_score = ucb_score
                best_child = child

        return best_child

        
    def update(self, result):
        """Update the node with the result of a simulation."""
        self.visits += 1
        self.value += result

    # If any actions untried Expand
    def expand(self):
        """Expand a node by creating a new child for an untried action."""
        new_state = copy.deepcopy(self.state)
        tried_actions = [child.state.action_taken for child in self.children]
        tried_action_id = {action["id"] for action in tried_actions}
        untried_actions = [
                action for action in new_state.legal_actions() if action["id"] not in tried_action_id
            ]

        if not untried_actions:
            return self  
        action = random.choice(untried_actions)

        new_state.execute_action(action)
        new_state.action_taken = action
        child_node = Node(new_state, parent=self)
        
        self.children.append(child_node)
        
        return child_node

# Simulate Game either Random for MCTS or NN
def simulate(state, ai):
    """Simulate a random game from the given state."""
    stato = copy.deepcopy(state)
    
    
    #if stato.action_taken["type"] == "pass":
        #return 0
    
    input_vector = np.array(stato.get_vector(ai))
    predicted_val = predict_with_tflite(input_vector)
    predicted_val = float(predicted_val) 
    
    #i = 0
    """ while not stato.is_terminal() and i < 25:

        legal_actions = stato.legal_actions()
        action = random.choice(legal_actions)
        #print(f"{legal_actions} HERE")
        #print(action)
        stato.execute_action(action)
        #print(f"{stato.get_result(ai)} this")
        i+=1 """
    return predicted_val #stato.get_result(ai)

# Find the Best action
def mcts(root,ai, iterations=10):
 
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
        while node is not None:
            #print(f"Player AP {node.state.player_AP.name}")
            #print(f"Player NAP {node.state.player_NAP.name}")
            #print(f"Action Taken {node.state.action_taken}")
            node.update(result)
            
            vector = node.state.get_vector(ai)
            training_data.append({'state_vector': vector, 'reward': result})
            
            node = node.parent
            #print("g")
    

            
            
    return root.best_child(exploration_weight=0.0)

# Play Games with MCTS or NN
if __name__ == "__main__":
          
    ai = player1
    wins = 0
    not_finished = 0
    acts = []
    
    
    for _ in range(0,100,1):
        initial_state = copy.deepcopy(state)
        
        random.shuffle(deck1)
        random.shuffle(deck2)
        start_hand1 = deck1[:7]
        start_hand2 = deck2[:8]
        deck11 = deck1[7:]
        deck22 = deck2[8:]
        
        initial_state.player_AP.deck = deck11
        initial_state.player_AP.hand = start_hand1
        
        initial_state.player_NAP.deck = deck22
        initial_state.player_NAP.hand = start_hand2


        root = Node(initial_state)
        i=0
        game_data = []
        
        
    
        while not root.state.is_terminal(): #and i < 200:
            if root.state.player_S.name == ai.name:
                

                # 1 itteration for NN, more for MCTS
                root = mcts(root,ai, iterations=1)
                state_copy = copy.deepcopy(root.state)
                game_data.append(state_copy)
                if root:
                    if root.state.action_taken:
                        acts.append(f"Best action: {root.state.action_taken["type"]} value {root.value} phase {root.state.phase}, #{i}")

                    else:
                        acts.append(f"Best action: {root.state.action_taken}")

                
            else:
 
                actions = root.state.legal_actions()
                action = random.choice(actions)
                root.state.execute_action(action)
            
            i+=1
            
            
            
        print(f"{root.state.player_AP.name}  {root.state.player_AP.life}")
        print(f"{root.state.player_NAP.name}  {root.state.player_NAP.life}")
        print(_)
        
        if root.state.winner == None:
            reward = 0
            not_finished += 1
            
        elif root.state.winner.name == ai.name:
            reward = 1
            wins += 1
        else:
            reward = -1
            
        for stato in game_data:
            vector = stato.get_vector(ai)
            training_data.append({'state_vector': vector, 'reward': reward})
            
            
    with open('training_data.txt', 'w') as f:
        json.dump(training_data, f)      
   
    print(wins)
    print(not_finished)


# Play Random games
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
        
print(bob)
print(alice)
