import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

data = pickle.load(open('paper_docs.p', 'rb'))
data_as_arr = [d for d in data]
folders = [data[d]['folder'] for d in data]
text = [data[d]['text'] for d in data]

vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(text)
similarity_matrix = (tfidf * tfidf.T).A

# Ignore self matches
np.fill_diagonal(similarity_matrix, 0)


def most_similar_document(index):
    print "looking for document most similar to:"
    print data_as_arr[index]
    print "---"
    print similarity_matrix[index].argmax()
