import re

class RuleBasedSystem:
    def __init__(self):
        """
        System A: Improved 'Glass Box'
        Separates single-word triggers (strict matching) from multi-word phrases (loose matching).
        """
        
        # === 1. ALL-OR-NOTHING THINKING ===
        
        # Phrases (No word boundary needed, safer for multi-word)
        self.aon_phrases = [
            "total failure", "waste of space", "no point", "nothing works",
            "perfect or nothing", "my life is over", "completely ruined",
            "никто не", "ничего не", "провал", "конец света",
            "түкке тұрғысыз", "ешкім емеспін"
        ]
        
        # Single Words (Need \b to avoid matching 'always' inside 'hallways')
        self.aon_words = [
            "always", "never", "everyone", "nobody", "nothing", "everything",
            "totally", "completely", "forever", "impossible",
            "всегда", "никогда", "все", "никто", "ничего", "абсолютно",
            "әрқашан", "ешқашан", "бәрі", "ешкім", "ештеңе", "мүлдем"
        ]
        
        # === 2. MIND READING ===
        
        self.mr_phrases = [
            "they think", "she thinks", "he thinks", "everyone thinks",
            "people think", "knows that i", "judging me", "laughing at me",
            "hate me", "hates me", "ignoring me", "mad at me",
            "они думают", "она думает", "он думает", "все думают",
            "меня осуждают", "смеются надо мной", "ненавидят меня",
            "ойлайды", "деп ойлайды", "мазақтайды", "жек көреді"
        ]
        
        self.mr_words = [
            "supposedly", "seemingly" 
            # Mind reading is usually phrases, rarely single words
        ]

    def analyze(self, text):
        text = text.lower()
        
        # 1. Check Mind Reading Phrases (Loose Match)
        for phrase in self.mr_phrases:
            if phrase in text:
                return "MIND_READING"
                
        # 2. Check Mind Reading Words (Strict Match)
        for word in self.mr_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                return "MIND_READING"

        # 3. Check All-or-Nothing Phrases (Loose Match)
        for phrase in self.aon_phrases:
            if phrase in text:
                return "ALL_OR_NOTHING"
                
        # 4. Check All-or-Nothing Words (Strict Match)
        for word in self.aon_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                return "ALL_OR_NOTHING"
                
        # Default
        return "NEUTRAL_DISTRESS"

# Test Logic
if __name__ == "__main__":
    rules = RuleBasedSystem()
    print(f"Test 'Everyone hates me': {rules.analyze('Everyone hates me')}") 
    # Should now capture 'everyone' (AON) or 'hates me' (MR) correctly.