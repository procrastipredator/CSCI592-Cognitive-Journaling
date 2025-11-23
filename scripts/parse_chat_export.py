import json
import csv

def extract_text_content(text_obj):
    """
    Flattens Telegram's polymorphic text field into a single string.
    """
    if isinstance(text_obj, str):
        return text_obj
    elif isinstance(text_obj, list):
        full_text = []
        for item in text_obj:
            if isinstance(item, str):
                full_text.append(item)
            elif isinstance(item, dict) and 'text' in item:
                full_text.append(item['text'])
        return "".join(full_text)
    return ""

def parse_telegram_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    messages = data.get('messages', [])
    
    # Single header column
    headers = ['txt']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        count = 0
        for msg in messages:
            if msg.get('type') != 'message':
                continue

            clean_text = extract_text_content(msg.get('text', ''))

            # Write to CSV only if there is actual content
            if clean_text.strip():
                writer.writerow([clean_text])
                count += 1

    print(f"Extracted {count} messages to '{output_file}'.")

if __name__ == "__main__":
    # Input/Output definitions
    INPUT_FILENAME = 'result.json' 
    OUTPUT_FILENAME = 'channel_messages.csv'
    
    parse_telegram_json(INPUT_FILENAME, OUTPUT_FILENAME)