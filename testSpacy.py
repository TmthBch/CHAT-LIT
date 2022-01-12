import spacy
from spacy.lang.lt.examples import sentences

nlp = spacy.load("lt_core_news_md")
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.morph, token.shape_)