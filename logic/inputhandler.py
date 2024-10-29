import spacy
from jptranscription import Katakanizer, IPATranscription
from models.phonetizer_model import PhonetizerInput


# ID for NUM POS tag
NUM_PROPN = 92
NUM_POS = 93


# Convert basic user input string to a list of objects for phonetizer and katakanizer
class InputHandler:
    def __init__(self):
        self.nlp = spacy.load('de_core_news_sm')
        self.katakanizer = Katakanizer()
        self.phonetizer = IPATranscription()

    
    def get_phonetics(self, x: PhonetizerInput):
        words = self._handle_input(x)
        for i in range(len(words)):
            (word, pos) = words[i]
            words[i] += (self.phonetizer.lookup_word(word, pos),)
        print(words)
        return words
    
    def get_katakana(self, x: PhonetizerInput):
        words = self.get_phonetics(x)
        for i in range(len(words)):
            (word, pos, ipa) = words[i]
            words[i] += (self.katakanizer.transcribe_word(ipa),)
        return words

    def _handle_input(self, x: PhonetizerInput):
        if not x.user_input:
            return
        # NLP processing
        doc = self.nlp(x.user_input)
        words = [(token.text, token.pos_) for token in doc]

        # Custom rule processing
        InputHandler._st_rule(words)
        # TODO: number to word
        # TODO: kg to Kilogramm 

        return words

    def _st_rule(words):
        for i, (word, pos) in enumerate(words):
            if word.lower() == 'st.':
                if  i != 0 and words[i-1][1] == 'NUM':  # st. preceded by a number
                    words[i] = ('Stück', pos)
                elif i != len(words)-1 and words[i+1][1] == 'PROPN':  # st. preceded by a noun with no number before
                    words[i] = ('Sankt', pos)

    