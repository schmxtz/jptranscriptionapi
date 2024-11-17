import spacy
from jptranscription import Katakanizer, IPATranscription
from models.phonetizer_model import PhonetizerInput
from num2words import num2words
import re


PUNCT_MAPPINGS = {
    ',': '、',
    '.': '。',
    '."': '」',
    '".': '「',
    '.\'': '」',
    '\'.': '「',
    ':': ':',
}

DOT_REPLACE_PATTERN = (re.compile(r'(\d*)(\.)(\d*\,\d*)'), r'\1\3')


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
        return words
    
    def get_katakana(self, x: PhonetizerInput):
        words = self.get_phonetics(x)
        quotation_counter = 0
        for i in range(len(words)):
            (word, pos, ipa) = words[i]
            try:
                if pos == 'PUNCT':
                    if word == '\"':
                        transcription = PUNCT_MAPPINGS['.'+word] if quotation_counter % 2 == 0 else PUNCT_MAPPINGS[word+'.'] 
                        quotation_counter += 1
                    transcription = PUNCT_MAPPINGS.get(word) if PUNCT_MAPPINGS.get(word) else word
                else:
                    transcription = self.katakanizer.transcribe_word(ipa)
                words[i] += (transcription,)
            except Exception as e:
                print(e)
                words[i] += ('',)
        return words

    def _handle_input(self, x: PhonetizerInput):
        if not x.user_input:
            return
        
        user_input = x.user_input
        
        # Custom rule pre-processing
        # Iteratively removes preceding dots in decimal number (with comma)
        while len(user_input) != len(user_input := re.sub(DOT_REPLACE_PATTERN[0], DOT_REPLACE_PATTERN[1], user_input)): pass

        # NLP processing
        doc = self.nlp(user_input)
        words = [(token.text, token.pos_) for token in doc]

        # Custom rule post-processing
        for i, (word, pos) in enumerate(words):
            InputHandler._st_rule(words, i, word, pos)
            InputHandler._num_rule(words, i, word, pos)
            InputHandler._symbol_rule(words, i, word, pos)
        # TODO: kg to Kilogramm 

        return words

    def _st_rule(words, i, word, pos):
        if word.lower() == 'st.':
            if  i != 0 and words[i-1][1] == 'NUM':  # st. preceded by a number
                words[i] = ('Stück', pos)
            elif i != len(words)-1 and words[i+1][1] == 'PROPN':  # st. preceded by a noun with no number before
                words[i] = ('Sankt', pos)
    
    def _num_rule(words, i, word, pos):
        if pos == 'NUM':
            try:
                words[i] = (num2words(word.replace(',', '.'), lang='de'), pos)
            except:
                pass  # number is already in text form

    def _symbol_rule(words, i, word, pos):
        match word:
            case '€':
                words[i] = ('Euro', pos)
            case '$':
                words[i] = ('Dollar', pos)
            case '%':
                words[i] = ('Prozent', pos)
    