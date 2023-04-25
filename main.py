import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.chunk.regexp import RegexpParser
import random

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def get_wordnet_pos(treebank_pos):
    if treebank_pos.startswith('J'):
        return wordnet.ADJ
    elif treebank_pos.startswith('V'):
        return wordnet.VERB
    elif treebank_pos.startswith('N'):
        return wordnet.NOUN
    elif treebank_pos.startswith('R'):
        return wordnet.ADV
    else:
        return None

def paraphrase_sentence(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    synonyms = []
    lemmatizer = WordNetLemmatizer()
    for token, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        lemma = lemmatizer.lemmatize(token, pos=wordnet_pos)
        synsets = wordnet.synsets(lemma, pos=wordnet_pos)
        if synsets:
            synonyms.append(random.choice(synsets).lemmas()[0].name())
        else:
            synonyms.append(token)
    paraphrase = ' '.join(synonyms)
    return paraphrase

def print_syntax_tree(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    grammar = r"""
        NP: {<DT|JJ|NN.*>+}          # Noun phrase
        VP: {<VB.*><NP|PP|CLAUSE>+$} # Verb phrase
        PP: {<IN><NP>}               # Prepositional phrase
        CLAUSE: {<NP><VP>}           # Clause
    """

    parser = RegexpParser(grammar)
    tree = parser.parse(pos_tags)
    return tree


def paraphrase_syntax_tree(tree):
    grammar = r"""
        NP: {<DT|JJ|NN.*>+}          # Noun phrase
        VP: {<VB.*><NP|PP|CLAUSE>+$} # Verb phrase
        PP: {<IN><NP>}               # Prepositional phrase
        CLAUSE: {<NP><VP>}           # Clause
    """

    parser = RegexpParser(grammar)

    for subtree in tree.subtrees():
        if subtree.label() == 'NP' or subtree.label() == 'VP':
            tokens = [token for token, pos in subtree]
            pos_tags = pos_tag(tokens)
            synonyms = []
            lemmatizer = WordNetLemmatizer()
            for token, pos in pos_tags:
                wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
                lemma = lemmatizer.lemmatize(token, pos=wordnet_pos)
                synsets = wordnet.synsets(lemma, pos=wordnet_pos)
                if synsets:
                    synonyms.append(random.choice(synsets).lemmas()[0].name())
                else:
                    synonyms.append(token)
            for i in range(len(tokens)):
                subtree[i] = (synonyms[i], pos_tags[i][1])

    return tree
