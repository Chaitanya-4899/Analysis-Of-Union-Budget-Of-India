# analysis/nlp_model.py

import spacy
from pdfminer.high_level import extract_text

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def extract_budget_allocations(text):
    doc = nlp(text)
    allocations = []
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            sentence = ent.sent
            allocations.append(sentence.text)
    return allocations
