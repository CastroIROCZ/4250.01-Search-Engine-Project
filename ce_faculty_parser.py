from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download()

'''
Parser file that creates an inverted index of each term and their respective documents
of the Civil Engineering faculty pages

'''

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

db = connectDataBase()

pages = db.pages
inverted_index = db.invertedIndex

def parse_text_pages(col, index, url_pattern):
    '''
    Parsing function that stores term objects into the invertedIndex collection.
    
    Parameters
    ----------

    col: MongoDB collection
        The collection of all of the previously crawled pages
        that are already stored in the database

    index: MondoDB collection
        The collection to store all of the parsed terms and
        a list of their documents present in

    url_pattern: dict
        A dictionary represented in the pages collection to
        extract all of the pages only of the faculty members

    '''
    faculty = list(col.find(url_pattern))
    
    text = []
    doc_terms = []
    
    for member in faculty:
        id = member['_id']
        html = member['html']
        bs = BeautifulSoup(html, 'html.parser')
        main_section = bs.find_all('div', class_='blurb')
        side_bar = bs.find_all('div', class_= 'accolades')
        main_section.extend(side_bar)

        for cell in main_section:
            
            cleaned_lemmatized_text = filter_text(cell)

            text.append(cleaned_lemmatized_text)
            doc_terms.append([id] + [cleaned_lemmatized_text])

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
    ''' 
    Adds a term object (dictionary) to the collection,
    where the object is the term, and a list of its documents

    Parameters
    ----------
    col: MongoDB collection
        Database collection for objects to be stored in

    term_dicionary: dict
        A dictionary to represent a term object of the term
        and its documents present in

    '''

    for term, documents in term_dictionary.items():
        term_object = {
            "term" : term,
            "documents" : documents
        }

        col.insert_one(term_object)

def filter_text(html_cell):
    '''
    Uses stopwords, lemmatizing, and regular expression
    filtering to clean the text to be ready to
    store in the inverted index 

    Parameters
    ----------

    html_cell: BeautifulSoup tag object
        A BeautifulSoup tag inputted to extract the text
        and filter it fully for the inverted index
     
    '''

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    text = html_cell.get_text().replace(u'\xa0', '').replace('\n', ' ').replace('\t', '')
    text = re.sub(r'https?://[^\s,]+', '', text)
    text = re.sub(r'[“”"(),\.*:&]', '', text)
    text = [word.lower() for word in text.split() if word.lower() not in stop_words]
    cleaned_lemmatized_text = [lemmatizer.lemmatize(word) for word in text]

    return cleaned_lemmatized_text


faculty_url_pattern = {'url': {'$regex': "^https:\/\/www\.cpp\.edu\/faculty\/.*"}}
parse_text_pages(pages, inverted_index, faculty_url_pattern)