import os

import numpy as np

class QLearningAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.q_table = np.zeros(state_size + (action_size,))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.action_size = action_size

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)
        return np.argmax(self.q_table[tuple(state)])

    def update(self, state, action, reward, next_state):
        current = self.q_table[tuple(state)][action]
        target = reward + self.gamma * np.max(self.q_table[tuple(next_state)])
        self.q_table[tuple(state)][action] += self.alpha * (target - current)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save(self, filepath):
        np.save(filepath, self.q_table)
        print(f"Q-table saved to {filepath}")

    def load(self, filepath):
        if os.path.exists(filepath):
            self.q_table = np.load(filepath)
            print(f"Q-table loaded from {filepath}")
        else:
            raise FileNotFoundError(f"No file found at {filepath}")