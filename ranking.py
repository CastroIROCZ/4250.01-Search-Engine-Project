from nltk import WordNetLemmatizer, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bs4 import BeautifulSoup
import pandas as pd
import re

def connectDataBase():
    '''
    Connects to project database

    '''

    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db
    except:
        print("Database not connected successfully")

def parse(text):
    bs = BeautifulSoup(text, 'html.parser')
    new_text = bs.get_text(separator= '\n', strip=True)
    new_text = new_text.lower()
    new_text = re.sub(r'[^a-zA-Z0-9\s]', '', new_text)
    new_text = re.sub(r'\s+', ' ', new_text)
    return new_text

def parse_query(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def search(query):
    relevant_docs = set()
    terms = query.split()

    # gets the docs that have the query terms
    for term in terms:
        result = inverted_index.find_one({'term': term})
        if result:
            for doc_id in result['documents']:
                relevant_docs.add(doc_id)

    # get the faculty pages from pages collection
    documents = []
    for doc_id in relevant_docs:
        document = pages.find_one({'_id': doc_id})
        if document:
            documents.append(document)

    # parse the text from documents to calculate tf-idf vectors
    docs = [parse(doc['html']) for doc in documents]
    queries = parse_query(query)
    # print(docs)
    # print(queries)

    # instantiate the vectorizer object
    tfidfvectorizer = TfidfVectorizer(analyzer= 'word', stop_words='english')

    # convert the training set into a matrix.
    tfidf_matrix = tfidfvectorizer.fit_transform(docs + [queries])

    # store the last row(queries) of TF-IDF matrix
    query_vector = tfidf_matrix[-1]
    # store all rows(docs) except last one of TF-IDF matrix
    document_vectors = tfidf_matrix[:-1]

    # get the cosine similarity scores between the query vector and docs vector
    similarities = cosine_similarity(query_vector, document_vectors).flatten()

    # combine cosine similarities with docs and sort in desc order
    ranked_docs = sorted(zip(similarities, documents), reverse=True)

    return ranked_docs


db = connectDataBase()

pages = db.pages
inverted_index = db.invertedIndex
query = input("Enter a search query: ")
ranked_docs = search(query)

for i, (similarity, doc) in enumerate(ranked_docs, 1):
    print(f"{i}. {doc['url']} | Similarity: {similarity}")
