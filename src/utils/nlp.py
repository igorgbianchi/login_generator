import unicodedata
from logging import Logger

import nltk
from nltk.corpus import stopwords


class NLP:
    def __init__(self, logger: Logger) -> None:
        nltk.download("stopwords")
        nltk.download("punkt")
        self.stop_words = set(stopwords.words("portuguese"))
        self.logger = logger

    def remove_stop_words(self, text: str) -> str:
        words = nltk.word_tokenize(text)
        return " ".join([word for word in words if word not in self.stop_words])

    def remove_accent_marks(self, text: str) -> str:
        unidecode = unicodedata.normalize("NFD", text)
        text_bytes = unidecode.encode("ascii", "ignore")

        return str(text_bytes.decode("utf8"))

    def normalize(self, text: str) -> str:
        self.logger.debug(f"Original text: {text}")
        normalized_text = self.remove_stop_words(text)
        self.logger.debug(f"Stop words removed: {normalized_text}")
        normalized_text = self.remove_accent_marks(normalized_text)
        self.logger.debug(f"Accent marks removed: {normalized_text}")
        normalized_text = normalized_text.upper().strip()

        return normalized_text
