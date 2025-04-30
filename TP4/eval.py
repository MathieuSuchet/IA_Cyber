from TP4.env import CyberAttackEnv
from TP4.q_learning import QLearningAgent

env = CyberAttackEnv()
agent = QLearningAgent((2, 2, 2), 3)  # 3 bits d’état, 3 actions
agent.load("agent.npy")

agent.epsilon = 0  # Évaluation

success = 0
for _ in range(100):
    state, _ = env.reset()
    while True:
        action = agent.choose_action(state)
        state, reward, done, truncated, _ = env.step(action)
        if done or truncated:
            print("Episode done")
            if int(float(reward)) > 0:
                success += 1
            break

print(f"Taux de réussite sur 100 essais : {success}%")
