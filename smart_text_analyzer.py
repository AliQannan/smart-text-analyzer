import string
from collections import defaultdict, Counter

class SmartTextAnalyzer:
    def __init__(self):
        self.text = []
        self.sentences = []
        self.word_counts = Counter()
        self.char_counts = Counter()
        self.vocabulary = set()
        self.stop_words = {'the', 'a', 'is', 'and', 'of', 'to', 'in'}
        self.bigrams = defaultdict(Counter)
        self.positive_words = {'good', 'happy', 'great', 'excellent', 'love', 'wonderful'}
        self.negative_words = {'bad', 'sad', 'terrible', 'awful', 'hate', 'horrible'}

    def load_text(self):
        print("Welcome to The Intelligent Text Processor!")
        choice = input("Do you want to load text from a file (f) or enter it directly (d)? [f/d]: ").strip().lower()
        if choice == 'f':
            path = input("Please enter the full path to your text file: ")
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    raw_text = file.read()
            except FileNotFoundError:
                print("File not found.")
                return
        elif choice == 'd':
            print("Please enter your text. Type '$$END_TEXT$$' on a new line when you are finished:")
            lines = []
            while True:
                line = input()
                if line.strip() == '$$END_TEXT$$':
                    break
                lines.append(line)
            raw_text = '\n'.join(lines)
        else:
            print("Invalid input.")
            return

        self.preprocess_text(raw_text)

    def preprocess_text(self, raw_text):
        raw_text = raw_text.lower()
        for p in string.punctuation:
            raw_text = raw_text.replace(p, '')
        self.sentences = raw_text.split('.')
        self.text = raw_text.split()
        self.word_counts = Counter(self.text)
        self.char_counts = Counter(''.join(self.text))
        self.vocabulary = set(self.text)
        self.build_bigrams()
        print("Text loaded and preprocessed successfully!")

    def build_bigrams(self):
        for i in range(len(self.text) - 1):
            self.bigrams[self.text[i]][self.text[i + 1]] += 1

    def word_statistics(self):
        print(f"Total words: {len(self.text)}")
        print(f"Unique words: {len(self.vocabulary)}")
        print("Most frequent words:")
        for word, freq in self.word_counts.most_common(10):
            print(f"{word}: {freq}")

    def character_statistics(self):
        print(f"Total characters (excluding spaces): {sum(self.char_counts.values())}")
        print("Character frequencies:")
        for char, freq in self.char_counts.items():
            print(f"{char}: {freq}")

    def search_word(self):
        target = input("Enter the word or phrase to search: ").lower()
        results = []
        for i, sentence in enumerate(self.sentences):
            words = sentence.strip().split()
            for j, word in enumerate(words):
                if target == word:
                    results.append((i + 1, j + 1))
        if results:
            print(f"Occurrences of '{target}':")
            for sent_no, word_index in results:
                print(f"Sentence {sent_no}, Word {word_index}")
        else:
            print("Word not found.")

    def replace_word(self):
        old = input("Enter the word to replace: ").lower()
        new = input("Enter the new word: ").lower()
        if old in self.text:
            self.text = [new if w == old else w for w in self.text]
            self.word_counts = Counter(self.text)
            self.vocabulary = set(self.text)
            self.build_bigrams()
            print(f"Word '{old}' replaced successfully with '{new}'!")
        else:
            print(f"Word '{old}' not found in text.")

    def autocomplete(self):
        prefix = input("Enter prefix: ").lower()
        suggestions = [word for word in self.vocabulary if word.startswith(prefix)]
        print("Suggestions:", suggestions[:10])

    def predict_next_word(self):
        phrase = input("Enter word or phrase: ").lower().split()
        if not phrase:
            print("No input provided.")
            return
        last_word = phrase[-1]
        predictions = self.bigrams.get(last_word, {})
        if predictions:
            most_common = predictions.most_common(3)
            print("Next word suggestions:")
            for word, freq in most_common:
                print(f"{word} ({freq})")
        else:
            print("No suggestions available.")

    def spell_suggest(self):
        word = input("Enter a potentially misspelled word: ").lower()
        if word in self.vocabulary:
            print("Word is correct.")
            return

        def edits(w):
            letters = 'abcdefghijklmnopqrstuvwxyz'
            splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)

        candidates = edits(word)
        suggestions = [w for w in candidates if w in self.vocabulary]
        print("Did you mean:", suggestions[:5])

    def sentiment_analysis(self):
        sentence = input("Enter a sentence: ").lower()
        words = sentence.split()
        score = 0
        for word in words:
            if word in self.positive_words:
                score += 1
            elif word in self.negative_words:
                score -= 1
        if 'not' in words:
            score = -score
        sentiment = 'Neutral'
        if score > 0:
            sentiment = 'Positive'
        elif score < 0:
            sentiment = 'Negative'
        print(f"Sentiment: {sentiment}")

    def keyword_extraction(self):
        filtered = [w for w in self.text if w not in self.stop_words]
        freq = Counter(filtered)
        print("Top keywords:")
        for word, count in freq.most_common(10):
            print(f"{word}: {count}")

    def wordcloud_data(self):
        filtered = [w for w in self.text if w not in self.stop_words]
        freq = Counter(filtered)
        max_freq = max(freq.values())
        wordcloud = [(word, round(count / max_freq, 2)) for word, count in freq.items()]
        print("Word Cloud Data:")
        for word, norm_freq in wordcloud[:10]:
            print(f"{word}: {norm_freq}")

    def menu(self):
        while True:
            print("""
--- Smart Text Analyzer ---
1. Word Statistics
2. Character Statistics
3. Search Word
4. Replace Word
5. Autocomplete
6. Predict Next Word
7. Spell Suggestion
8. Sentiment Analysis
9. Keyword Extraction
10. Word Cloud Data
0. Exit
            """)
            choice = input("Select an option: ").strip()
            if choice == '1':
                self.word_statistics()
            elif choice == '2':
                self.character_statistics()
            elif choice == '3':
                self.search_word()
            elif choice == '4':
                self.replace_word()
            elif choice == '5':
                self.autocomplete()
            elif choice == '6':
                self.predict_next_word()
            elif choice == '7':
                self.spell_suggest()
            elif choice == '8':
                self.sentiment_analysis()
            elif choice == '9':
                self.keyword_extraction()
            elif choice == '10':
                self.wordcloud_data()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
            input("Press Enter to return to the main menu...")

if __name__ == '__main__':
    analyzer = SmartTextAnalyzer()
    analyzer.load_text()
    analyzer.menu()
