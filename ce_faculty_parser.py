from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download()

def connectDataBase():

    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db
    except:
        print("Database not connected successfully")

# database
db = connectDataBase()

pages = db.pages
inverted_index = db.invertedIndex

def parse_text_pages(col, index, query):
    faculty = list(col.find(query))
    
    text = []
    doc_terms = []
    
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    for member in faculty:
        id = member['_id']
        html = member['html']
        bs = BeautifulSoup(html, 'html.parser')
        main_section = bs.find_all('div', class_='blurb')
        side_bar = bs.find_all('div', class_= 'accolades')
        main_section.extend(side_bar)

        for cell in main_section:
            get_text = cell.get_text().replace(u'\xa0', '').replace('\n', ' ').replace('\t', '')
            clean_text = re.sub(r'https?://[^\s,]+', '', get_text)
            clean_text = re.sub(r'[“”"(),\.*:&]', '', clean_text)
            clean_text = [word.lower() for word in clean_text.split() if word.lower() not in stop_words]
            clean_text = [lemmatizer.lemmatize(word) for word in clean_text]

            text.append(clean_text)
            doc_terms.append([id] + [clean_text])

    words = list(set(word for doc in text for word in doc))

    for word in words:
        doc_list = []
        documents_visited = []
        for id, terms in doc_terms:
            if (word in terms) and (id not in documents_visited):
                doc_list.append(id)
                documents_visited.append(id)
    
        termdict = {word: doc_list}
        add_term_object(index, termdict)


def add_term_object(col, term_dictionary):
    for term, documents in term_dictionary.items():
        indexTerm = {
            "term" : term,
            "documents" : documents
        }

        col.insert_one(indexTerm)


seed_url_query = {'url': {'$regex': "^https:\/\/www\.cpp\.edu\/faculty\/.*"}}
parse_text_pages(pages, inverted_index, seed_url_query)
