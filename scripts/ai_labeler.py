import google.generativeai as genai
import pandas as pd
import json
import time
import os
from tqdm import tqdm

# --- CONFIGURATION ---
# Replace with your actual API Key
API_KEY = "AIzaSyDv6HbeMs9xvRb3VOD2PmJ3u1Et59GlK-k"

# Input/Output files
INPUT_FILE = "gold_standard_dataset.csv"
OUTPUT_FILE = "ai_labeled_dataset.csv"

# Batch size (sending 20 rows at a time is efficient for Gemini Flash)
BATCH_SIZE = 20

# Configure Gemini
genai.configure(api_key=API_KEY)

# We use 1.5 Flash for speed and cost-efficiency. 
# It handles English, Russian, and Kazakh contexts well.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"response_mime_type": "application/json"}
)

# --- THE PSYCHOLOGICAL PROMPT ---
SYSTEM_INSTRUCTION = """
You are a Senior Psychologist and Data Annotator. Your task is to analyze text messages from university students and identify specific cognitive distortions.

The texts are in English, Russian, or Kazakh (often mixed).

Classify each message into one of the following labels:

1. "ALL_OR_NOTHING": The user speaks in absolutes (always, never, everyone, nothing). They view a situation as black-and-white, total failure, or total perfection. 
   - Example: "I am a total failure," "Everyone hates me," "My life is ruined forever."
   
2. "MIND_READING": The user assumes they know what others are thinking about them (usually negative), without evidence.
   - Example: "They think I'm stupid," "She is definitely laughing at me," "Everyone is judging me."

3. "DISTRESS": The user is venting genuine emotional pain, depression, or anxiety, but it does not strictly fit the definitions above.
   - Example: "I feel so lonely and tired," "I want to cry," "I can't take this anymore."

4. "NOISE": The message is situational complaining, asking for advice, external anger, or irrelevant. 
   - Example: "I hate this professor," "Why is the bus late?", "I failed the exam" (without self-labeling), "Does anyone have a charger?"

Output a JSON list of objects. Each object must have:
- "id": The ID provided in the prompt.
- "label": One of [ALL_OR_NOTHING, MIND_READING, DISTRESS, NOISE].
- "reason": A brief (3-5 word) explanation.
"""

def process_batch(batch_df):
    """Sends a batch of rows to the LLM."""
    
    # Construct the prompt payload
    messages_text = []
    for index, row in batch_df.iterrows():
        messages_text.append(f"ID: {index}\nText: {row['text']}")
    
    prompt = f"{SYSTEM_INSTRUCTION}\n\nAnalyze the following messages:\n" + "\n---\n".join(messages_text)

    try:
        # Safety settings: BLOCK_NONE is required because the dataset 
        # contains references to self-harm/suicide (the signal we want to keep).
        response = model.generate_content(
            prompt,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error in batch: {e}")
        # Return empty list on failure to keep the loop going (you can retry manually later)
        return []

def main():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_FILE)
    
    # Prepare columns for results
    df['label'] = None
    df['reason'] = None
    
    total_rows = len(df)
    print(f"Processing {total_rows} rows...")

    # Process in batches
    for start_idx in tqdm(range(0, total_rows, BATCH_SIZE)):
        end_idx = min(start_idx + BATCH_SIZE, total_rows)
        batch = df.iloc[start_idx:end_idx]
        
        results = process_batch(batch)
        
        # Map results back to the dataframe
        for item in results:
            row_id = item.get('id')
            if row_id is not None and start_idx <= row_id < end_idx:
                df.at[row_id, 'label'] = item.get('label')
                df.at[row_id, 'reason'] = item.get('reason')
        
        # Rate limit protection (free tier is ~15 requests per minute)
        time.sleep(4) 

    # --- POST PROCESSING ---
    print("Filtering and Saving...")
    
    # We discard "NOISE". We keep specific distortions and general distress.
    # If you ONLY want distortions for your SVM, filter out 'DISTRESS' too.
    final_df = df[df['label'].isin(['ALL_OR_NOTHING', 'MIND_READING', 'DISTRESS'])]
    
    # Save the labeled file
    df.to_csv("full_labeled_history.csv", index=False, encoding='utf-8-sig') # Saves everything including Noise
    final_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig') # Saves only the Gold data
    
    print(f"Finished. Found {len(final_df)} usable training examples.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()