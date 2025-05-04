import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from scipy import spatial
import networkx as nx
nltk.download('stopwords')
nltk.download('punkt')
testing_text = """Alphabet Inc.’s Google waived a 1.1 billion-pound loan ($1.5 billion) to DeepMind Technologies Ltd. in 2019 after the U.K.-based artificial intelligence lab continued to ramp up the scale of its research and development.
Revenue jumped 158% in 2019, DeepMind said in a financial filing this week. Sales were 265.5 million pounds, up from 102.8 million pounds a year earlier. Its losses also widened, increasing 1.4% to 476.6 million pounds.
DeepMind’s parent has agreed to continue funding the company for at least a year after the report’s approval. Alphabet’s Google Ireland unit waived repayments and interest from the loan to help cover DeepMind’s losses.
Google acquired DeepMind in 2014 in a 400 million-pound acquisition that gave the Silicon Valley search giant access to cutting edge AI research. DeepMind Chief Executive Officer Demis Hassabis’s goal is to produce general-purpose intelligence that can solve an array of problems. It develops products used by its parent company -- like its system for making data centers more energy efficient and a program to improve the accuracy of travel times on Google Maps -- as well as AI with broader applications.
The company’s technology for predicting the shape of proteins, which has potential uses for everything from drug research to designing enzymes that can break down pollutants, came first in a scientific competition devoted to the topic in November. DeepMind’s CASP victory may open the way for it to make its tool, called AlphaFold, more broadly available to researchers.
“During the period covered by these accounts, DeepMind laid the foundations for our groundbreaking results in protein structure prediction,” a DeepMind spokesperson said in a statement. “Our teams were involved in a huge range of projects, from improving the predictability of wind power to accelerating ecological research in the Serengeti.”"""

def summarize(filepath='None', paragraph='blank'):
    if filepath != 'None':
        f = open(filepath, "r", encoding="utf8")
        text = f.read()
        Broken_in_sentences = sent_tokenize(text)
    else:
        Broken_in_sentences = sent_tokenize(paragraph)

    Broken_in_sentences_clean = [re.sub(r'[^\w\s]', '', sentence.lower()) for sentence in Broken_in_sentences]
    Unnecessary_words = stopwords.words('english')
    Tokenized_sentence = [[words for words in sentence.split(' ') if words not in Unnecessary_words] for sentence in
                          Broken_in_sentences_clean]
    w2v = Word2Vec(Tokenized_sentence, vector_size=1, min_count=1, epochs=1000)
    sentence_embedded_value = [[w2v.wv[word][0] for word in words if word in w2v.wv] for words in Tokenized_sentence]
    max_len = max([len(tokens) for tokens in Tokenized_sentence])
    sentence_embedded_value = [np.pad(embedding, (0, max_len - len(embedding)), 'constant') for embedding in
                                sentence_embedded_value]
    similarity_matrix = np.zeros([len(Tokenized_sentence), len(Tokenized_sentence)])
    for i, row_embedding in enumerate(sentence_embedded_value):
        for j, column_embedding in enumerate(sentence_embedded_value):
            similarity_matrix[i][j] = 1 - spatial.distance.cosine(row_embedding, column_embedding)
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    top_sentence = {sentence: scores[index] for index, sentence in enumerate(Broken_in_sentences)}
    top = dict(sorted(top_sentence.items(), key=lambda x: x[1], reverse=True)[:3])
    summarized_text = [sent for sent in Broken_in_sentences if sent in top.keys()]
    print(" ".join(summarized_text))
    return summarized_text  # Returns list
