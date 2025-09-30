import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_PATH = os.path.join(BASE_DIR, "loan_clean_encoded.csv")

os.makedirs(MODEL_DIR, exist_ok=True)

# ----------------------
# Load dataset
# ----------------------
print("📂 Loading dataset...")
df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "loan_clean_encoded.csv"))


# ✅ Keep only required features
features = ["AnnualIncome", "LoanAmount", "EmploymentStatus", 
            "TotalAssets", "HomeOwnershipStatus", "CreditScore"]

X = df[features]
y = df["LoanApproved"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ----------------------
# Define models
# ----------------------
models = {
    "logistic_model": LogisticRegression(max_iter=1000),
    "decision_tree_model": DecisionTreeClassifier(random_state=42),
    "random_forest_model": RandomForestClassifier(n_estimators=100, random_state=42),
    "svm_model": SVC(probability=True, random_state=42),
}

# ----------------------
# Train and evaluate
# ----------------------
accuracies = {}
for name, model in models.items():
    print(f"🔄 Training {name} ...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    accuracies[name] = acc
    print(f"{name} Accuracy: {acc:.2f}")

    # Save model
    model_path = os.path.join(MODEL_DIR, f"{name}.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Saved {name} -> {model_path}")

# Save accuracies
with open(os.path.join(MODEL_DIR, "accuracies.pkl"), "wb") as f:
    pickle.dump(accuracies, f)

print("\n🎉 All models trained and saved successfully!")
