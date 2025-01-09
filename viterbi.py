import math
from collections import defaultdict

def get_init_state_prob():
    """contains weights for every state and describes the prior probability of each – P(s)."""
    tot_weight = 0
    state_weights = {}
    with open('state_weights.txt', 'r') as file:
        file.readline()
        first_line = file.readline().strip().split()
        try:
            num_states, default_weight = int(first_line[0]), float(first_line[1])
        except:
            num_states, default_weight = int(first_line[0]), 0

        for line in file:
            line_parts = line.strip().split()
            state = line_parts[0]
            weight = float(line_parts[1])
            state_weights[state] = weight
            tot_weight += weight

    # Convert to log probabilities
    for state in state_weights:
        state_weights[state] = math.log(state_weights[state] / tot_weight) if tot_weight > 0 and state_weights[state] /tot_weight > 0 else float('-inf')

    return state_weights

def get_transition_model():
    """file contains weights for (state, action, state) triples and describes the probability of state
    transitions – P(s, a, s). Triples not specified in the table should be given the default weight from the
    second line. Need to normalize these weights into the appropriate probability distribution
    P(s’ | a, s)."""
    transition_weights = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: float('-inf'))))
    all_states = set()
    all_actions = set()

    with open("state_action_state_weights.txt", 'r') as file:
        file.readline()
        first_line = file.readline().strip().split()
        num_triples, num_states, num_actions, default_weight = int(first_line[0]), int(first_line[1]), int(first_line[2]), float(first_line[3])

        for line in file:
            line_parts = line.strip().split()
            state = line_parts[0]
            action = line_parts[1]
            next_state = line_parts[2]
            weight = float(line_parts[3])

            all_states.update([state, next_state])
            all_actions.add(action)
            transition_weights[state][action][next_state] = weight

    # Normalize and convert to log probabilities
    for state in all_states:
        for action in all_actions:
            action_total_weight = sum(transition_weights[state][action].values()) + (
                default_weight * (len(all_states) - len(transition_weights[state][action]))
            )

            for next_state in all_states:
                if next_state not in transition_weights[state][action]:
                    transition_weights[state][action][next_state] = default_weight
                transition_weights[state][action][next_state] = (
                    math.log(transition_weights[state][action][next_state] / action_total_weight)
                    if action_total_weight > 0 and transition_weights[state][action][next_state] / action_total_weight > 0 else float('-inf')
                )

    return transition_weights

def get_appearance_model():
    """contains weights for every (state, observation) pair, and describes the probability
    of each state observation pair P(s, o). Pairs not specified in the table should be given the default weight
    specified in the second line. Need to normalize these weights into the appropriate
    probability distribution P(o | s)."""
    appearance_weights = defaultdict(lambda: defaultdict(lambda: float('-inf')))
    all_states = set()
    all_observations = set()

    with open("state_observation_weights.txt", 'r') as file:
        file.readline()
        first_line = file.readline().strip().split()
        num_pairs, num_states, num_observations, default_weight = int(first_line[0]), int(first_line[1]), int(first_line[2]), float(first_line[3])

        for line in file:
            line_parts = line.strip().split()
            state = line_parts[0]
            observation = line_parts[1]
            weight = float(line_parts[2])

            all_states.add(state)
            all_observations.add(observation)
            appearance_weights[state][observation] = weight

    # Normalize and convert to log probabilities
    for state in all_states:
        state_total_weight = sum(appearance_weights[state].values()) + (default_weight * (len(all_observations) - len(appearance_weights[state])))

        for observation in all_observations:
            if observation not in appearance_weights[state]:
                appearance_weights[state][observation] = default_weight
            appearance_weights[state][observation] = (
                math.log(appearance_weights[state][observation] / state_total_weight)
                if state_total_weight > 0 and appearance_weights[state][observation] /state_total_weight > 0 else float('-inf')
            )

    return appearance_weights

def viterbi(state_weights, transition_weights, appearance_weights, obs):
    V = [{} for _ in range(len(obs))]
    path = {}

    # Base case
    for state in state_weights:
        observation, action = obs[0]
        V[0][state] = state_weights[state] + appearance_weights[state][observation]
        path[state] = [state]

    # Recurrence
    for t in range(1, len(obs)):
        new_path = {}
        observation = obs[t][0]
        action = obs[t-1][1]

        for state in state_weights.keys():
            best_prob = float('-inf')
            best_prev_state = None
            
            for prev_state in state_weights.keys():
                prob = V[t-1][prev_state] + transition_weights[prev_state][action][state] + appearance_weights[state][observation]
                
                if prob > best_prob:
                    best_prob = prob
                    best_prev_state = prev_state
            
            V[t][state] = best_prob
            new_path[state] = path[best_prev_state] + [state] if best_prev_state else [state]

        path = new_path

    # Backtracking 
    best_prob = float('-inf')
    best_state = None
    for state in state_weights.keys():
        if V[len(obs) - 1][state] > best_prob:
            best_prob = V[len(obs) - 1][state]
            best_state = state

    return path[best_state] if best_state else []

def main():
    state_weights = get_init_state_prob()
    transition_weights = get_transition_model()
    appearance_weights = get_appearance_model()

    obs = []
    with open("observation_actions.txt", 'r') as file:
        file.readline()
        first_line = file.readline().strip().split()
        num_pairs = int(first_line[0])

        for _ in range(num_pairs-1):
            line = file.readline()
            line_parts = line.strip().split()
            observation = line_parts[0]
            action = line_parts[1]
            obs.append((observation, action))
        line = file.readline().strip().split()
        observation = line[0]
        obs.append((observation, None))

    res = viterbi(state_weights, transition_weights, appearance_weights, obs)

    with open('states.txt', 'w') as file:
        file.write('states\n')
        file.write(str(len(res)) + '\n')
        for state in res:
            file.write(state + '\n')

if __name__ == '__main__':
    main()  
    
