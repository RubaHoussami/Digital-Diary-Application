import os
import spacy
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.crew.base.base_extractor import BaseExtractor


class EventExtractor(BaseExtractor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventExtractor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.spacy_model = spacy.load("en_core_web_trf")
            model_path = self._get_model_path()
            assert os.path.exists(model_path), f"Model path does not exist: {model_path}"
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.initialized = True

    @staticmethod
    def _get_model_path():
        return 'src\models\event_extractor'

    def extract_core_events(self, text: str) -> dict:
        doc = self.spacy_model(text)

        characters = []
        actions = []
        locations = []
        times = []
        objects = []
        subjects = []
        adjectives = []
        adverbs = []
        organizations = []
        events = []

        for ent in doc.ents:
            if ent.label_ in {"PERSON"}:
                characters.append(ent.text)
            elif ent.label_ in {"GPE", "LOC"}:
                locations.append(ent.text)
            elif ent.label_ in {"DATE", "TIME"}:
                times.append(ent.text)

        for token in doc:
            if token.dep_ == "nsubj":
                subjects.append(token.text)
            elif token.pos_ == "VERB":
                actions.append(token)
            elif token.pos == "ADV":
                adverbs.append(token.text)
            elif token.dep_ == "dobj":
                objects.append(token.text)
            elif token.pos_ == "ADJ":
                adjectives.append(token.text)
            elif token.dep_ == "advmod":
                adverbs.append(token.text)
            elif ent.label_ == "ORG":
                organizations.append(ent.text)
            elif ent.label == "EVENT":
                events.append(ent.text)

        return {
            "characters": characters,
            "actions": actions,
            "times": times,
            "locations": locations,
            "objects": objects,
            "subjects": subjects,
            "adjectives": adjectives,
            "adverbs": adverbs,
            "organizations": organizations,
            "events": events
        }

    def tokenize(self, text: str) -> dict:
        return self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

    def extract(self, text: str) -> dict:
        tokenized_text = self.tokenize(text)
        events = self.extract_core_events(text)

        with torch.no_grad():
            outputs = self.model(**tokenized_text)
            logits = outputs.logits

        predicted_class_id = torch.argmax(logits, dim=1).tolist()
        extracted_topics = self.model.config.id2label[predicted_class_id[0]]

        events["topics"] = [extracted_topics]

        return events
