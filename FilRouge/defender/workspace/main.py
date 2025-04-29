# agent_defenseur.py
import time
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import subprocess

# Charger modèle pré-entrainé
model = joblib.load("modele_random_forest.pkl")  # A créer/entraîner avant

log_file = "/var/log/suricata/fast.log"
blocked_ips = set()

def extract_features_from_log(line):
    """Extrait les features basiques depuis une ligne de log"""
    features = {
        "is_scan": int("ET SCAN" in line),
        "is_bruteforce": int("BruteForce" in line),
        "port_21": int(":21" in line),
        "port_22": int(":22" in line),
        "port_80": int(":80" in line),
        "port_445": int(":445" in line),
        "port_5432": int(":5432" in line),
        "ip_src": line.split(" ")[2] if len(line.split(" ")) > 2 else "0.0.0.0"
    }
    return features

def block_ip(ip):
    if ip not in blocked_ips:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        blocked_ips.add(ip)
        print(f"[DEFENSE] IP bloquée : {ip}")

# Surveillance continue
print("[IA Défenseur] Surveillance démarrée...")
with open(log_file, "r") as f:
    f.seek(0,2)  # Aller à la fin du fichier
    while True:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue
        features = extract_features_from_log(line)
        if features["ip_src"] == "0.0.0.0":
            continue
        
        df = pd.DataFrame([{
            "is_scan": features["is_scan"],
            "is_bruteforce": features["is_bruteforce"],
            "port_21": features["port_21"],
            "port_22": features["port_22"],
            "port_80": features["port_80"],
            "port_445": features["port_445"],
            "port_5432": features["port_5432"]
        }])
        
        prediction = model.predict(df)[0]
        if prediction == 1:
            block_ip(features["ip_src"])
