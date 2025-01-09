# viterbi-algo

---

# **Viterbi Algorithm Implementation**

## **Overview**
This project implements the **Viterbi Algorithm**, a dynamic programming method for finding the most probable sequence of hidden states in a Hidden Markov Model (HMM), given a sequence of observations and actions. The program reads configuration data from input files, processes it into probabilistic models, and outputs the most likely state sequence based on the observations and actions.

---

## **Files**

1. **`viterbi.py`**
   - The main Python script containing:
     - Functions to compute probabilities from input data.
     - The implementation of the Viterbi algorithm.
     - A driver function (`main`) that orchestrates the workflow.

2. **Input Files**:
   - `state_weights.txt`: Contains prior probabilities for each state.
   - `state_action_state_weights.txt`: Contains transition probabilities for `(state, action, next state)` triples.
   - `state_observation_weights.txt`: Contains probabilities for `(state, observation)` pairs.
   - `observation_actions.txt`: Contains the sequence of observations and actions for testing.

3. **Output File**:
   - `states.txt`: Outputs the most probable sequence of states based on the observations and actions.

---

## **How It Works**

1. **Input Parsing**:
   - Reads weights and configurations from `state_weights.txt`, `state_action_state_weights.txt`, and `state_observation_weights.txt`.
   - Normalizes the weights into probabilities and converts them to log probabilities for numerical stability.

2. **Viterbi Algorithm**:
   - Computes the most probable sequence of hidden states based on:
     - Initial state probabilities (`P(s)`).
     - Transition probabilities (`P(s' | s, a)`).
     - Observation probabilities (`P(o | s)`).
   - Uses a recursive approach to build a dynamic programming table (`V`) that stores the probability of each state at each step.
   - Backtracks through the table to extract the most likely sequence.

3. **Outputs**:
   - Writes the most probable sequence of states to `states.txt`.

---

## **How to Run**

### **Dependencies**
No external dependencies are required beyond Python's standard library.

### **Steps**
1. Ensure the required input files are in the same directory as `viterbi.py`:
   - `state_weights.txt`
   - `state_action_state_weights.txt`
   - `state_observation_weights.txt`
   - `observation_actions.txt`

2. Run the script:
   ```bash
   python viterbi.py
   ```

3. View the results in `states.txt`.

---

## **Input File Formats**

### 1. **`state_weights.txt`**
- Specifies the prior probabilities for each state.
- Format:
  ```
  num_states default_weight
  state1 weight1
  state2 weight2
  ...
  ```

### 2. **`state_action_state_weights.txt`**
- Contains transition probabilities for `(state, action, next state)` triples.
- Format:
  ```
  num_triples num_states num_actions default_weight
  state action next_state weight
  ...
  ```

### 3. **`state_observation_weights.txt`**
- Contains probabilities for `(state, observation)` pairs.
- Format:
  ```
  num_pairs num_states num_observations default_weight
  state observation weight
  ...
  ```

### 4. **`observation_actions.txt`**
- Specifies the sequence of observations and actions.
- Format:
  ```
  num_pairs
  observation1 action1
  observation2 action2
  ...
  observationN
  ```

---

## **Output File Format**

### **`states.txt`**
- Contains the most probable sequence of states.
- Format:
  ```
  states
  num_states
  state1
  state2
  ...
  ```

---

## **Example**

### Input
#### `state_weights.txt`
```
3 1.0
A 2.0
B 3.0
C 1.0
```

#### `state_action_state_weights.txt`
```
3 3 2 0.1
A action1 B 0.5
B action2 C 0.3
C action1 A 0.2
```

#### `state_observation_weights.txt`
```
3 3 3 0.1
A obs1 0.4
B obs2 0.3
C obs1 0.2
```

#### `observation_actions.txt`
```
3
obs1 action1
obs2 action2
obs1
```

### Output
#### `states.txt`
```
states
3
A
B
C
```

---

## **Features**
- Handles missing data gracefully by using default weights.
- Supports a flexible number of states, actions, and observations.
- Provides numerical stability using log probabilities.

---

## **Future Enhancements**
- Add support for visualizing the Viterbi path.
- Extend to multi-threaded or GPU-based implementation for large datasets.

---
