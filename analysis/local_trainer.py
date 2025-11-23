import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_local():
    print("🚀 Starting Local Training...")
    
    # 1. Load Data
    try:
        df = pd.read_csv('final_train.csv')
    except FileNotFoundError:
        print("❌ ERROR: 'final_train.csv' not found.")
        print("Please download it from your Google Drive folder and place it here.")
        return

    # 2. Prep Data
    X = df['text'].astype(str)
    y = df['label']
    
    # 3. Create & Train Vectorizer
    print("... Vectorizing Data")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)
    X_vec = vectorizer.fit_transform(X) # This creates the .idf_ attribute locally
    
    # 4. Train SVM
    print("... Training SVM Model")
    model = LinearSVC(class_weight='balanced', random_state=42)
    model.fit(X_vec, y)
    
    # 5. Save Files (Overwriting the broken Colab ones)
    print("... Saving working artifacts")
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("\n✅ SUCCESS! New 'model.pkl' and 'vectorizer.pkl' generated.")
    print("Try running 'debug_engine.py' again.")

if __name__ == "__main__":
    train_local()