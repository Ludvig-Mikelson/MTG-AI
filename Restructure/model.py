from collections import defaultdict
import json

# Load data from the .txt file
data = []
with open('training_data.txt', 'r') as f:
    for line in f:
        try:
            # Parse each line as JSON
            entries = json.loads(line.strip())
            if isinstance(entries, list):  # Check if the line is a list of dictionaries
                data.extend(entries)  # Add all dictionaries from the list
            else:
                print(f"Skipping non-list entry: {entries}")
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line.strip()}")  # Handle parsing errors

# Aggregate rewards for duplicate state vectors
aggregated_data = defaultdict(list)
for entry in data:
    try:
        state_vector = tuple(entry["state_vector"])  # Convert to tuple for hashability
        reward = entry["reward"]
        aggregated_data[state_vector].append(reward)
    except KeyError:
        print(f"Skipping entry due to missing key: {entry}")

# Calculate the average reward for each unique state vector
averaged_data = {k: sum(v) / len(v) for k, v in aggregated_data.items()}

# Save the aggregated results to a new file
with open('aggregated_training_data.txt', 'w') as f:
    for state_vector, avg_reward in averaged_data.items():
        f.write(f"{list(state_vector)} {avg_reward}\n")

# Output results
print("Averaged Data:", averaged_data)
