import pickle
import csv
import os
import datetime
from rules import RuleBasedSystem

class InferenceEngine:
    def __init__(self):
        print("Initializing Inference Engine...")
        
        # Load System A
        self.rule_system = RuleBasedSystem()
        
        # Load System B
        self.ml_ready = False
        try:
            with open('vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            self.ml_ready = True
        except FileNotFoundError:
            print("⚠️ System B missing. Defaulting to Rules.")

        # Logger
        self.log_file = 'experiment_logs.csv'
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'user_id', 'text', 'prediction', 'system', 'feedback'])

    def predict(self, text, user_id):
        """
        Deterministic A/B Routing:
        - Even User IDs -> System A (Rules)
        - Odd User IDs -> System B (ML)
        """
        # 1. Assign System based on User ID (Consistent Experience)
        if not self.ml_ready:
            system_choice = 'System A (Rules)'
        elif user_id % 2 == 0:
            system_choice = 'System A (Rules)'
        else:
            system_choice = 'System B (SVM)'
            
        prediction = "NEUTRAL_DISTRESS"
        
        try:
            if 'Rules' in system_choice:
                prediction = self.rule_system.analyze(text)
            elif 'SVM' in system_choice:
                vec_text = self.vectorizer.transform([text])
                prediction = self.model.predict(vec_text)[0]
        except Exception as e:
            print(f"Prediction Error: {e}")
            
        return prediction, system_choice

    def log_interaction(self, user_id, text, label, system, feedback):
        timestamp = datetime.datetime.now().isoformat()
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_id, text, label, system, feedback])