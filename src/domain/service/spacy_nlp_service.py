from typing import Dict, List, Optional, Tuple

import spacy
from spacy.language import Language


class SpacyNLPService:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initializes the SpacyService with a specific spaCy model.
        :param model_name: Name of the spaCy model to load (default is 'en_core_web_sm').
        """
        try:
            self.nlp: Language = spacy.load(model_name)
            print(f"Loaded spaCy model '{model_name}' successfully.")
        except Exception as e:
            print(f"Failed to load spaCy model '{model_name}': {str(e)}")
            self.nlp = None

    def process_text(self, text: str) -> Dict:
        """
        Processes the given text and returns various NLP features like tokens, lemmas, and entities.
        :param text: The text to process.
        :return: A dictionary containing tokens, lemmas, entities, and noun chunks.
        """
        if not self.nlp:
            raise ValueError("spaCy model is not loaded.")

        doc = self.nlp(text)
        return {
            "tokens": [token.text for token in doc],
            "lemmas": [token.lemma_ for token in doc],
            "entities": [(entity.text, entity.label_) for entity in doc.ents],
            "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        }

    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """
        Extracts keywords from the given text using noun chunks and named entities.
        :param text: The text from which to extract keywords.
        :param num_keywords: The number of top keywords to return.
        :return: A list of keywords.
        """
        doc = self.nlp(text)
        keywords = {
            chunk.text.lower() for chunk in doc.noun_chunks
        }  # Using sets for uniqueness
        keywords.update({ent.text.lower() for ent in doc.ents})
        # Return the first 'num_keywords' keywords
        return list(keywords)[:num_keywords]

    def find_similar_words(self, word: str, topn: int = 10) -> List[Tuple[str, float]]:
        """
        Finds similar words to the given word based on the loaded model's vocabulary.
        Note: This function will only work if the loaded spaCy model has vector information.
        :param word: The word to find similarities for.
        :param topn: The number of similar words to return.
        :return: A list of tuples containing the similar words and their similarity scores.
        """
        if not self.nlp:
            raise ValueError("spaCy model is not loaded.")
        if not self.nlp.vocab.vectors:
            raise ValueError("The loaded spaCy model does not contain vector information for similarity checks.")

        token = self.nlp.vocab[word]
        if not token.has_vector:
            return []  # The word does not have a vector representation in the model

        # Find tokens with vectors and calculate similarity
        similar_tokens = sorted(
            [t for t in self.nlp.vocab if t.has_vector and t.is_lower == token.is_lower],
            key=lambda t: token.similarity(t),
            reverse=True
        )

        # Remove duplicates and self references, then return the topn similar words
        seen = set()
        filtered_tokens = []
        for t in similar_tokens:
            if t.text != word and t.text not in seen:
                seen.add(t.text)
                filtered_tokens.append((t.text, token.similarity(t)))
                if len(filtered_tokens) >= topn:
                    break

        return filtered_tokens
