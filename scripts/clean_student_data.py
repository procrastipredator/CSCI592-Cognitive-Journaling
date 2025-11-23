import pandas as pd
import re
import sys
from tqdm import tqdm

# --- CONFIGURATION ---
INPUT_FILE = 'channel_messages.csv'  # Your raw export
OUTPUT_FILE = 'gold_standard_dataset.csv' # The final clean file

# --- 1. KEYWORD LISTS (CONFIGURATION) ---

# A. SIGNAL WORDS (Must contain at least one to be considered emotional)
KEEP_KEYWORDS = [
    # ALL-OR-NOTHING
    'always', 'never', 'everyone', 'nobody', 'everything', 'nothing', 'total', 
    'complete', 'failure', 'ruined', 'hopeless', 'useless', 'forever', 'perfect',
    'всегда', 'никогда', 'все', 'никто', 'ничего', 'полный', 'провал', 'испорчено', 
    'безнадежно', 'бесполезно', 'вечно', 'идеально', 'конченный',
    'ешқашан', 'бәрі', 'ештеңе', 'түк', 
    # MIND READING
    'they think', 'she thinks', 'he thinks', 'knows that', 'hate me', 'laughing at', 
    'judging', 'staring', 'talk about me', 'looks at me', 'everyone sees', 
    'думают', 'ненавидят', 'смеются', 'осуждают', 'смотрят', 'обсуждают', 
    'презирают', 'косо смотрят', 'ойлайды', 'жек көреді', 'күледі',
    # EMOTIONAL DISTRESS
    'depressed', 'anxious', 'lonely', 'tired', 'kill myself', 'die', 'suicide', 
    'cry', 'crying', 'tears', 'scared', 'afraid', 'ugly', 'fat', 'stupid', 'exhausted',
    'overwhelmed', 'give up', 'hate myself', 'mental', 'burnout',
    'депрессия', 'устала', 'устал', 'умереть', 'суицид', 'плачу', 'слезы', 'рыдаю',
    'страшно', 'боюсь', 'урод', 'тупой', 'ненавижу себя', 'менталка', 'выгорание', 
    'сдохнуть', 'заебало', 'пиздец', 'хреново', 'сил нет',
    'шаршадым', 'жылап', 'қорқамын', 'өлу', 'қайғы'
]

# B. NOISE LISTS (If any match, drop the row)
# Combining all your lists into logical groups for readability

NOISE_TECH = [
    'laptop', 'macbook', 'iphone', 'android', 'samsung', 'sim card', 'wifi', 'vpn',
    'headphones', 'airpods', 'charger', 'battery', 'keyboard', 'mouse', 'screen',
    'ноутбук', 'телефон', 'айфон', 'зарядка', 'наушники', 'вайфай', 'симка',
    'samsung', 'apple', 'pc', 'комп'
]

NOISE_ENTERTAINMENT = [
    'game', 'play', 'movie', 'series', 'anime', 'manga', 'netflix',
    'игра', 'играть', 'фильм', 'сериал', 'аниме', 'манга', 'нетфликс'
]

NOISE_BEGGING = [
    'give me', 'send me', 'anyone has', 'looking for', 
    'дайте', 'скиньте', 'у кого есть', 'ищу', 'посоветуйте', 'recommend', 'advice on'
]

NOISE_LOGISTICS = [
    'found', 'lost', 'keys', 'card', 'id card', 'student id', 'driver', 'taxi', 'bus', 
    'delivery', 'parcel', 'left', 'right', 'floor', 'block', 'cabinet', 'office',
    'потерял', 'нашел', 'ключи', 'карту', 'студак', 'удос', 'водитель', 'такси', 
    'посылка', 'блок', 'этаж', 'кабинет', 'лифт', 'постомат', 'жоғалтып', 'таудым', 
    'кілт', 'карта', 'жүргізуші', 'посылка', 'gym', 'library', 'atrium', 'shower', 
    'kitchen', 'lift', 'elevator', 'canteen', 'coffee', 'printer', 'paper', 'ticket', 
    'flight', 'train', 'вокзал', 'поезд', 'билет', 'автобус'
]

NOISE_COMMERCE = [
    'selling', 'buying', 'price', 'rent', 'roommate', 'flat', 'apartment', 'deposit', 
    'kaspi', 'kzt', 'tg', 'tenge', 'condition', 'new', 'used', 'check-out', 'check out',
    'продам', 'куплю', 'цена', 'аренда', 'сдаю', 'ищу соседа', 'подселение', 'квартира', 
    'депозит', 'каспи', 'тенге', 'состояние', 'б/у', 'выселение', 'заселение',
    'сатып', 'аламын', 'бағасы', 'пәтер', 'теңге', 'жалға', 'cost', 'shop', 'store', 
    'order', 'магазин', 'доставка', 'заказ', 'bank', 'jusan', 'halyk', 'swift', 
    'счет', 'оплата', 'комиссия'
]

NOISE_ACADEMIC = [
    'syllabus', 'canvas', 'moodle', 'registrar', 'schedule', 'transcript', 'reference',
    'gpa', 'grade', 'midterm', 'final', 'quiz', 'retake', 'probation', 'dismissal', 
    'stipend', 'bursar', 'tuition', 'grant', 'major', 'transfer', 'internship',
    'силлабус', 'мудл', 'расписание', 'транскрипт', 'справка', 'оценка', 'мидка', 
    'файнал', 'квиз', 'ретейк', 'проба', 'отчисление', 'стипендия', 'грант', 'стажка',
    'баға', 'емтихан', 'оқу', 'deadline', 'assignment', 'exam', 'withdrawal', 
    'дедлайн', 'ассайнмент', 'экзамен', 'виздроу', 'scholarship', 'calc', 'calculus', 
    'physics', 'coding', 'python', 'java', 'essay', 'report', 'nuet', 'ielts', 'sat', 'foundation'
]

NOISE_SERVICES = [
    'green food', 'greenfood', 'gfood', 'daily cup', 'drinkit', 'umc', 'clinic', 
    'checkup', 'check-up', 'medical', 'doctor', 'hospital', 'pharmacy', 'haircut',
    'грин фуд', 'гринфуд', 'умс', 'клиника', 'чекап', 'врач', 'доктор', 'больница', 
    'аптека', 'парикмахерская', 'стоматолог', 'терапевт', 'флюра', 'dentist', 
    'dermatologist', 'ocular', 'therapist', 'surgery', 'операция', 'barber', 'salon', 
    'nails', 'manicure', 'brows', 'lashes', 'ногти', 'маникюр', 'брови', 'ресницы',
    'vitamin', 'protein', 'creatine', 'workout', 'trainer'
]

NOISE_SPAM_POLITICS = [
    'vote', 'link', 'form', 'registration', 'concert', 'club', 'awards', 'party', 
    'orchestra', 'ybs', 'kpop', 'dance', 'hacknu', 'debate', 'volunteer', 'giveaway',
    'голосуйте', 'ссылка', 'форма', 'регистрация', 'концерт', 'клуб', 'билет', 
    'вечеринка', 'розыгрыш', 'дауыс', 'bishimbayev', 'saltanat', 'israel', 'palestine', 
    'ukraine', 'russia', 'putin', 'biden', 'trump', 'news', 'бишимбаев', 'салтанат', 
    'израиль', 'палестина', 'украина', 'россия', 'путин', 'новости', 'government', 
    'president', 'minister', 'law', 'policy', 'corruption', 'bribe', 'правительство', 
    'закон', 'коррупция', 'muslim', 'islam', 'christian', 'atheist', 'god', 'religion', 
    'haram', 'halal', 'feminism', 'feminist', 'men', 'women', 'gender', 'patriarchy',
    'dota', 'counter strike', 'cs:go'
]

# Consolidate all noise into one set for O(1) lookup
MASTER_NOISE_SET = set(
    NOISE_LOGISTICS + NOISE_COMMERCE + NOISE_ACADEMIC + 
    NOISE_SERVICES + NOISE_SPAM_POLITICS + NOISE_TECH + 
    NOISE_ENTERTAINMENT + NOISE_BEGGING
)

# C. INTROSPECTION MARKERS (Row must contain at least one)
# Combining your First Person and Self Tokens lists
INTROSPECTION_MARKERS = [
    ' i ', "i'", ' my ', ' me ', ' myself ', ' am ', ' im ', "i'm",
    ' я ', ' мне ', ' меня ', ' мной ', ' мой ', ' моя ', ' мое ', ' мои ',
    ' мен ', ' маган ', ' мени ', ' менин ', ' озим '
]

# --- 2. COMPILED REGEX ---

# Detects URLs
URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.|t\.me|forms\.gle')

# Detects Crowdsourcing/Functional Questions (Who/Where/When/Does anyone)
# Combined from your CROWD_PATTERN and QUESTION_REGEX
FUNCTIONAL_Q_PATTERN = re.compile(
    r'^(who|where|when|does|is|has|anyone|can someone|can i|can anyone|is there|what is|how to|'
    r'кто|где|когда|есть|подскажите|может|можно ли|почему не|'
    r'кім|қайда|қашан|қалай|бар ма)', 
    re.IGNORECASE
)

# --- 3. HELPER FUNCTIONS ---

def clean_text(text):
    if pd.isna(text): return ""
    return str(text).strip().lower()

def has_noise(text):
    """Returns True if text contains any word from the Master Noise Set."""
    # We iterate the set because checking inclusion in string is faster than strict token matching for this volume
    # Optimization: Check set membership if we tokenized, but for broad catch, substring is safer for Russian morphology
    for word in MASTER_NOISE_SET:
        if word in text:
            return True
    return False

def has_signal(text):
    """Returns True if text contains any word from the Keep/Signal list."""
    for word in KEEP_KEYWORDS:
        if word in text:
            return True
    return False

def is_introspective(text):
    """Returns True if text contains self-referencing pronouns."""
    # Pad with spaces to ensure we match " i " not "idiot"
    padded_text = " " + text + " "
    for marker in INTROSPECTION_MARKERS:
        if marker in padded_text:
            return True
    return False

def is_functional_question(text):
    """Returns True if text looks like a logistics question."""
    return bool(FUNCTIONAL_Q_PATTERN.match(text))

# --- 4. MAIN PIPELINE ---

def run_pipeline():
    print(f"--- STARTING PIPELINE ---")
    print(f"Loading {INPUT_FILE}...")
    
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Column normalization (handle 'txt' or 'text')
    if 'txt' in df.columns:
        df.rename(columns={'txt': 'text'}, inplace=True)
    
    initial_count = len(df)
    print(f"Original Row Count: {initial_count}")
    
    clean_rows = []
    
    # We use iterrows or a loop for granular control and debugging if needed, 
    # but for 45k rows, a list comprehension loop is fast enough.
    
    print("Processing messages...")
    for raw_text in tqdm(df['text']):
        
        # 0. Normalization
        norm_text = clean_text(raw_text)
        
        # FILTER 1: Length (Must be substantial, > 40 chars)
        # Exception: Urgent keywords like 'suicide' are kept even if short
        is_urgent = any(w in norm_text for w in ['suicide', 'kill myself', 'суицид', 'умереть'])
        if len(norm_text) < 40 and not is_urgent:
            continue
            
        # FILTER 2: Regex Checks (URLs and Questions)
        if URL_PATTERN.search(norm_text):
            continue
        if is_functional_question(norm_text):
            continue
            
        # FILTER 3: The Noise List (The "Kill" Filter)
        if has_noise(norm_text):
            continue
            
        # FILTER 4: The Signal List (The "Keep" Filter)
        # Must contain at least one emotional keyword
        if not has_signal(norm_text):
            continue
            
        # FILTER 5: Introspection (The "I" Filter)
        # Must be about the self
        if not is_introspective(norm_text):
            continue
            
        # If we passed all gauntlets, keep the ORIGINAL text
        clean_rows.append(raw_text)

    # Compile Final DataFrame
    result_df = pd.DataFrame(clean_rows, columns=['text'])
    
    # Deduplicate
    result_df.drop_duplicates(inplace=True)
    
    final_count = len(result_df)
    print(f"--- PIPELINE COMPLETE ---")
    print(f"Original: {initial_count}")
    print(f"Final:    {final_count}")
    print(f"Retention Rate: {round((final_count/initial_count)*100, 2)}%")
    
    print(f"Saving to {OUTPUT_FILE}...")
    result_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == "__main__":
    run_pipeline()