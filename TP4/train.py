from TP4.env import CyberAttackEnv
from TP4.q_learning import QLearningAgent

env = CyberAttackEnv()
agent = QLearningAgent((2, 2, 2), 3)  # 3 bits d’état, 3 actions

n_episodes = 1000
reward_history = []

for episode in range(n_episodes):
    state, _ = env.reset()
    total_reward = 0

    while True:
        action = agent.choose_action(state)
        next_state, reward, done, truncated,  _ = env.step(action)

        if truncated:
            reward = agent.q_table[tuple(state)][action]

        agent.update(state, action, reward, next_state)
        state = next_state
        total_reward += reward

        if done or truncated:
            break

    agent.decay_epsilon()
    reward_history.append(total_reward)

    if episode % 100 == 0:
        print(f"Épisode {episode} - Récompense totale: {total_reward}")

agent.save("agent.npy")
