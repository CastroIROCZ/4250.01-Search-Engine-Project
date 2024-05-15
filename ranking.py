from nltk import WordNetLemmatizer, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from bs4 import BeautifulSoup
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
    lemmatizer = WordNetLemmatizer()
    bs = BeautifulSoup(text, 'html.parser')
    new_text = bs.get_text(separator=' ', strip=True)
    new_text = new_text.lower()
    new_text = re.sub(r'[^a-zA-Z0-9\s]', '', new_text)
    new_text = re.sub(r'\s+', ' ', new_text)

    tokens = [lemmatizer.lemmatize(word) for word in new_text.split()]
    lemmatized_text = ' '.join(tokens)
    print(lemmatized_text)

    return lemmatized_text

def parse_query(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = [lemmatizer.lemmatize(word) for word in text.split()]
    lemmatized_text = ' '.join(tokens)
    print(lemmatized_text)
    return lemmatized_text

def search(query):
    relevant_docs = set()
    queries = parse_query(query)
    query_terms = queries.split()

    # gets the docs that have the query terms
    for term in query_terms:
        inverted_index_doc = inverted_index.find_one({'term': term})
        if inverted_index_doc:
            for doc_id in inverted_index_doc['documents']:
                relevant_docs.add(doc_id)

    if len(relevant_docs) == 0:
        return relevant_docs

    # get the faculty pages from pages collection
    fac_documents = []
    for doc_id in relevant_docs:
        document = pages.find_one({'_id': doc_id})
        if document:
            fac_documents.append(document)

    # parse the text from documents to calculate tf-idf vectors
    docs = [parse(doc['html']) for doc in fac_documents]

    # instantiate the vectorizer object
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')

    # convert the training set into a matrix.
    tfidf_matrix = tfidfvectorizer.fit_transform(docs + [queries])

    # store the last row(queries) of TF-IDF matrix
    query_vector = tfidf_matrix[-1]
    # store all rows(docs) except last one of TF-IDF matrix
    document_vectors = tfidf_matrix[:-1]

    # get the cosine similarity scores between the TF-IDF query vector and TF-IDF docs vector
    similarities = cosine_similarity(query_vector, document_vectors).flatten()

    # combine cosine similarities with docs and sort in desc order
    ranked_docs = sorted(zip(similarities, fac_documents), reverse=True)

    return ranked_docs

db = connectDataBase()

pages = db.pages
inverted_index = db.invertedIndex
faculty_index = db.faculty_index  # Add faculty_index collection

query = input("Enter a search query: ")
ranked_docs = search(query)

if len(ranked_docs) > 0:
    for i, (similarity, doc) in enumerate(ranked_docs, 1):
        faculty_data = faculty_index.find_one({'page_id': doc['_id']})
        if faculty_data:
            print(f"Result {i}:")
            print(f"Name: {faculty_data.get('name', 'No Name')}")
            print(f"Email: {faculty_data.get('email', 'No Email')}")
            print(f"Phone: {faculty_data.get('phone', 'No Phone')}")
            print(f"URL: {doc['url']}")
            print(f"Similarity: {similarity}")
            print()
else:
    print("No results found") 
