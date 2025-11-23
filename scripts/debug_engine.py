from inference_engine import InferenceEngine

def debug():
    print("--- 🛠 DEBUGGING MODE ---")
    engine = InferenceEngine()
    
    test_text = "Everyone hates me"
    
    # Force Test System A (Rules)
    # We simulate an EVEN user_id (e.g., 102) to force System A
    print(f"\nTesting Input: '{test_text}'")
    
    print("\n--- FORCING SYSTEM A (RULES) ---")
    pred_a, sys_a = engine.predict(test_text, user_id=102)
    print(f"System: {sys_a}")
    print(f"Prediction: {pred_a}")
    
    if pred_a == "NEUTRAL_DISTRESS":
        print("❌ FAILURE: Rules System missed the trigger word 'Everyone'.")
    else:
        print("✅ SUCCESS: Rules System caught it.")

    # Force Test System B (SVM)
    # We simulate an ODD user_id (e.g., 101) to force System B
    print("\n--- FORCING SYSTEM B (SVM) ---")
    pred_b, sys_b = engine.predict(test_text, user_id=101)
    print(f"System: {sys_b}")
    print(f"Prediction: {pred_b}")

if __name__ == "__main__":
    debug()