import pandas as pd
import re

def clean_text(text):
    # Convert to string just in case
    text = str(text)
    # Lowercase
    text = text.lower()
    # Keep Cyrillic, Latin, numbers, and basic punctuation
    # Remove newlines
    text = text.replace('\n', ' ')
    return text

def normalize_label(label):
    label = str(label).strip().upper()
    
    # Map All-or-Nothing variations
    if 'ALL-OR-NOTHING' in label or 'ALL_OR_NOTHING' in label:
        return 'ALL_OR_NOTHING'
    
    # Map Mind Reading variations
    elif 'MIND READING' in label or 'MIND_READING' in label:
        return 'MIND_READING'
    
    # Map Distress/Neutral/Venting to a single "OTHER" or "DISTRESS" class
    # For this project, let's keep DISTRESS as the control group for negative emotion
    elif 'DISTRESS' in label or 'VENTING' in label or 'NEUTRAL' in label:
        return 'NEUTRAL_DISTRESS'
    
    else:
        return 'UNKNOWN'

def run_pipeline():
    print("Loading datasets...")
    # Load Real Data (handling potential bad lines)
    df_real = pd.read_csv('student_dataset_labeled.csv', on_bad_lines='skip')
    # Keep only text and label
    df_real = df_real[['text', 'label']]
    
    # Load Synthetic Data
    df_synth = pd.read_csv('synthetic_dataset_labeled.csv', on_bad_lines='skip')
    # Synthetic might not have headers or different headers, ensure consistency
    # If your copy-paste had headers, good. If not, this safeguards it.
    if 'text' not in df_synth.columns:
        df_synth.columns = ['text', 'label']
    
    # Merge
    full_df = pd.concat([df_real, df_synth], ignore_index=True)
    
    # Normalize Labels
    full_df['label'] = full_df['label'].apply(normalize_label)
    
    # Remove UNKNOWN or Garbage labels
    full_df = full_df[full_df['label'] != 'UNKNOWN']
    
    # Clean Text
    full_df['text'] = full_df['text'].apply(clean_text)
    
    # Shuffle the data
    full_df = full_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    full_df.to_csv('final_train.csv', index=False)
    
    print(f"Pipeline Complete. Saved 'final_train.csv' with {len(full_df)} rows.")
    print("Class Distribution:")
    print(full_df['label'].value_counts())

if __name__ == "__main__":
    run_pipeline()