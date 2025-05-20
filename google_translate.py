from googletrans import Translator
import MeCab
import pykakasi

def get_romaji_reading(text):
    tagger = MeCab.Tagger("-Ochasen")
    node = tagger.parseToNode(text)
    kakasi = pykakasi.kakasi()
    romaji_words = []

    while node:
        features = node.feature.split(',')
        surface = node.surface
        # Get reading or fallback
        reading = features[7] if len(features) > 7 and features[7] != '*' else surface

        # Convert this reading to romaji
        result = kakasi.convert(reading)
        romaji_word = ''.join([item['hepburn'] for item in result])
        if romaji_word:  # skip empty
            romaji_words.append(romaji_word)
        node = node.next

    return ' '.join(romaji_words)

def translate_text():
    translator = Translator()
    
    print("Welcome to the Python Google Translate App!")
    print("Type 'exit' to stop.")

    while True:
        text = input("\nEnter text to translate: ")
        if text.lower() == 'exit':
            print("Goodbye!")
            break
        
        target_lang = "en"

        try:
            translated = translator.translate(text, dest=target_lang)
            print(f"Translated ({target_lang}): {translated.text}")
            # If input contains Japanese, show romaji with spacing
            if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in text):
                romaji = get_romaji_reading(text)
                print(f"Pronunciation (romaji): {romaji}")
            else:
                print(f"Pronunciation ({target_lang}): {translated.pronunciation}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    translate_text()
