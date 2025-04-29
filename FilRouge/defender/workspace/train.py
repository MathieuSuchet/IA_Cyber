# train_random_forest.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Exemple de dataset synthétique : 100 lignes
# 0 = normal, 1 = attaque
data = {
    "is_scan": [0, 1, 0, 1, 0, 1] * 16 + [1, 0, 1, 0],
    "is_bruteforce": [0, 0, 1, 1, 0, 1] * 16 + [1, 1, 0, 0],
    "port_21": [0, 1, 0, 0, 1, 0] * 16 + [1, 0, 1, 0],
    "port_22": [0, 0, 1, 0, 0, 1] * 16 + [0, 1, 0, 1],
    "port_80": [1, 0, 1, 0, 1, 0] * 16 + [0, 1, 1, 0],
    "port_445": [0, 0, 0, 1, 1, 0] * 16 + [1, 1, 0, 0],
    "port_5432": [0, 0, 0, 0, 1, 1] * 16 + [1, 0, 1, 0],
    "label": [0, 1, 1, 1, 0, 1] * 16 + [1, 0, 1, 0]
}

# Créer un DataFrame
df = pd.DataFrame(data)

# Séparer en X et y
X = df.drop(columns=["label"])
y = df["label"]

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle
joblib.dump(model, "modele_random_forest.pkl")

print("✅ Modèle Random Forest entraîné et sauvegardé sous 'modele_random_forest.pkl'")
