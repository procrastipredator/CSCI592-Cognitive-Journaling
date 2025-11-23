**Role:**
Act as a University Student Mental Health Data Generator.

**Objective:**
Generate a training dataset of 150 distinct text entries for a text classification model.

**Context:**
The texts should simulate short, informal journal entries or Telegram messages written by university students. The tone should be casual, sometimes stressed, sometimes sad, and can include minor grammatical errors or slang common in Gen Z speech (e.g., "idk," "gonna," "super tired").

**The Classes (Labels):**
You must generate 50 entries for EACH of the following 3 categories:

1. **All-or-Nothing Thinking**
   * *Definition:* Viewing situations in absolute, black-and-white terms. Using words like "always," "never," "every," "total," "complete," "forever."
   * *Examples:* "I failed the quiz, I'm a total idiot.", "I'll never get a job.", "Everyone is better than me.", "My life is completely ruined."
2. **Mind Reading**
   * *Definition:* Assuming you know what others are thinking (usually negative) or predicting the future negatively without evidence.
   * *Examples:* "She definitely hates me after what I said.", "The professor thinks I'm lazy.", "I know I'm going to fail the final.", "They are laughing at me."
3. **Neutral / Venting**
   * *Definition:* Expressing negative emotions (stress, sadness, anger) or describing difficult situations **WITHOUT** using the specific logic flaws above. It is crucial that these are NOT positive. They should be complaints or sad facts, but  *rationally phrased* .
   * *Examples:* "I'm really tired today.", "I got a C on the exam, I need to study more next time.", "I miss my family.", "The bus was late again.", "I don't know what to do about this assignment."

**Instructions:**

* Vary the length (some short 5-word sentences, some longer 2-sentence rants).
* Vary the topics: Grades, relationships, loneliness, sleep, money, professors.
* **CRITICAL:** Do NOT make the "Neutral" entries happy. They must be stressed or venting, but *without* the cognitive distortions.
* Output the data as a clean CSV format with headers `text,label`.

**Output Format:**
text,label
"I am completely useless at coding.",All-or-Nothing Thinking
"The cafeteria food was cold today.",Neutral
"He didn't text back, he must be angry at me.",Mind Reading
... (continue for 150 rows)
