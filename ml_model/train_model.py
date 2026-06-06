# ─────────────────────────────────────────────
#  Level 4 — Train Diabetes Prediction Model
#  Dataset: Pima Indians Diabetes Dataset
# ─────────────────────────────────────────────

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("=" * 50)
print("  Blood Glucose Monitor — ML Model Training")
print("=" * 50)

# ── Step 1: Load Dataset ─────────────────────
print("\n📂 Loading dataset...")
df = pd.read_csv("diabetes.csv")
print(f"✅ Dataset loaded — {df.shape[0]} patients, {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")

# ── Step 2: Explore Data ─────────────────────
print("\n📊 Dataset Summary:")
print(df.describe().round(2))

print(f"\nDiabetic patients    : {df['Outcome'].sum()}")
print(f"Non-diabetic patients: {len(df) - df['Outcome'].sum()}")

# ── Step 3: Clean Data ───────────────────────
print("\n🧹 Cleaning data...")

# These columns cannot be 0 in real life — replace 0 with median
zero_not_valid = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in zero_not_valid:
    median = df[col].median()
    df[col] = df[col].replace(0, median)
    print(f"  Fixed {col} — replaced 0s with median ({median})")

# ── Step 4: Prepare Features ─────────────────
print("\n⚙️  Preparing features...")
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

feature_names = list(X.columns)
print(f"Features: {feature_names}")

# ── Step 5: Split Data ───────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

# ── Step 6: Scale Features ───────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── Step 7: Train Model ──────────────────────
print("\n🤖 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train_scaled, y_train)
print("✅ Model trained successfully!")

# ── Step 8: Evaluate Model ───────────────────
print("\n📈 Model Evaluation:")
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred,
      target_names=["No Diabetes", "Diabetes"]))

# ── Step 9: Feature Importance ───────────────
print("🔍 Feature Importance (what matters most):")
importances = model.feature_importances_
for name, imp in sorted(zip(feature_names, importances),
                         key=lambda x: x[1], reverse=True):
    bar = "█" * int(imp * 50)
    print(f"  {name:<20} {bar} {imp:.3f}")

# ── Step 10: Save Model ──────────────────────
print("\n💾 Saving model and scaler...")
joblib.dump(model,  "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(feature_names, "features.pkl")
print("✅ Saved: model.pkl, scaler.pkl, features.pkl")

print("\n" + "=" * 50)
print("  Training Complete!")
print(f"  Final Accuracy: {accuracy * 100:.2f}%")
print("=" * 50)