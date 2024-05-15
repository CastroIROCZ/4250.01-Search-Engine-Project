from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import re
from nltk import WordNetLemmatizer
from pymongo import MongoClient
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MongoDB Database
def connect_database():
    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(DB_HOST, DB_PORT)
        return client[DB_NAME]
    except Exception as e:
        print("Failed to connect to database:", e)
        return None

db = connect_database()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'results': []})

    pages = db.pages
    inverted_index = db.invertedIndex
    faculty_index = db.faculty_index

    # Process query and documents
    def parse(text):
        lemmatizer = WordNetLemmatizer()
        bs = BeautifulSoup(text, 'html.parser')
        new_text = bs.get_text(separator=' ', strip=True)
        new_text = new_text.lower()
        new_text = re.sub(r'[^a-zA-Z0-9\s]', '', new_text)
        new_text = re.sub(r'\s+', ' ', new_text)
        tokens = [lemmatizer.lemmatize(word) for word in new_text.split()]
        lemmatized_text = ' '.join(tokens)
        return lemmatized_text

    def parse_query(text):
        lemmatizer = WordNetLemmatizer()
        text = text.lower()
        tokens = [lemmatizer.lemmatize(word) for word in text.split()]
        lemmatized_text = ' '.join(tokens)
        return lemmatized_text

    # Get relevant documents from inverted index
    relevant_docs = set()
    queries = parse_query(query)
    query_terms = queries.split()
    for term in query_terms:
        doc = inverted_index.find_one({'term': term})
        if doc:
            relevant_docs.update(doc['documents'])

    fac_documents = [pages.find_one({'_id': doc_id}) for doc_id in relevant_docs]

    # Prepare documents and query for TF-IDF
    docs = [parse(doc['html']) for doc in fac_documents if doc]
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    tfidf_wm = tfidfvectorizer.fit_transform(docs + [queries])
    query_vector = tfidf_wm[-1]
    document_vectors = tfidf_wm[:-1]

    # Calculate cosine similarity
    similarities = cosine_similarity(query_vector, document_vectors).flatten()
    ranked_docs = sorted(zip(similarities, fac_documents), reverse=True, key=lambda x: x[0])

    # Formulate results
    results = []
    for sim, doc in ranked_docs[:5]:  # Limit to top 5 results
        faculty_data = faculty_index.find_one({'page_id': doc['_id']})
        if faculty_data:
            results.append({
                'name': faculty_data.get('name', 'No Name'),
                'email': faculty_data.get('email', 'No Email'),
                'phone': faculty_data.get('phone', 'No Phone'),
                'url': doc['url'],
                'image_url': faculty_data.get('image_url', url_for('static', filename='default_image.jpg')),
                #'image_url': faculty_data.get('image_url', '/static/images/default.jpg'),  # Default image
                'similarity': sim
            })

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
