from typing import Any, SupportsFloat

import gymnasium
from gymnasium import spaces
import numpy as np
import random

from gymnasium.core import ObsType, ActType


class CyberAttackEnv(gymnasium.Env):
    def __init__(self):
        super(CyberAttackEnv, self).__init__()

        # Observation space: ping_ok, port_open, vuln_known
        self.observation_space = spaces.MultiBinary(3)

        # Action space: 0 = rien, 1 = scan, 2 = attaque
        self.action_space = spaces.Discrete(3)

        self.duration = 0
        self.target_duration = 80

        self.state = None
        self.done = False

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        self.state = np.array([
            random.choice([0, 1]),  # ping_ok
            random.choice([0, 1]),  # port_open
            0  # vuln_known (au départ inconnu)
        ])
        self.duration = 0
        self.done = False
        return self.state, {}


    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        reward = 0

        if self.done:
            return self.state, 0, self.done, False, {}

        ping_ok, port_open, vuln_known = self.state

        if action == 0:
            reward = 0  # Ne rien faire
        elif action == 1:  # Scanner
            if ping_ok and port_open:
                self.state[2] = 1  # vuln_known devient vrai après scan
                reward = 1
            else:
                reward = -1
        elif action == 2:  # Attaque
            if vuln_known:
                reward = 10
            else:
                reward = -5
            self.done = True  # Fin de l’épisode après l’attaque

        self.duration += 1

        return self.state, reward, self.done, self.duration >= self.target_duration, {}

    def render(self, mode='human'):
        print(f"État actuel: {self.state}")
