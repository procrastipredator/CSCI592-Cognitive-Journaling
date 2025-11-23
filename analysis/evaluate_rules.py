import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from rules import RuleBasedSystem

# 1. Load Data
df = pd.read_csv('final_train.csv')
X = df['text'].astype(str)
y = df['label']

# 2. Split exactly like the SVM (Random State 42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Run Rules on X_test
rules = RuleBasedSystem()
y_pred_rules = [rules.analyze(text) for text in X_test]

# 4. Print Report
print("=== System A (Rule-Based) Report ===")
print(classification_report(y_test, y_pred_rules))