from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import requests


class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def connectDataBase():
    # Creating a database connection object using psycopg2
    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")


def store_professors(name, title, office, phone, email, website):
    # Connecting to the database
    db = connectDataBase()
    # Creating a collection
    professors = db.professors

    # Value to be inserted
    professorsDoc = {
        "name": name,
        "title": title,
        "office": office,
        "phone": phone,
        "email": email,
        "website": website
    }

    # Insert the document
    professors.insert_one(professorsDoc)


# def parser(target_page_url):
    # Connecting to the database
db = connectDataBase()

document = db.pages.find_one({'url': 'https://www.cpp.edu/faculty/siddharthb/'})

req = requests.get(document['url'])
html = req.text
bs = BeautifulSoup(html, 'html.parser')
professor = bs.find_all('div', {'class': 'fac-staff'})


faculty_info = bs.find('div', {'class': 'span10'})
accolades = bs.find_all('div', {'class': 'accolades'})
sections = bs.find_all('div', {'class': 'section-text'})
section_menu = bs.find_all('div', {'class': 'section-menu'})

texts = []
facInfo = ""
facAccolade = ""
facHeading = ""
facMenu = ""


for info in faculty_info.find_all(string=True):
    facInfo += info.strip() + " "

for accolade in accolades:
    for element in accolade.find_all(string=True):
        facAccolade += element.strip() + " "

for section in sections:
    for element in section.find_all(string=True):
        facHeading += element.strip() + " "

for menu in section_menu:
    for element in menu.find_all(string=True):
        facMenu += element.strip() + " "

print(facInfo)
print(facAccolade)
print(facHeading)
print(facMenu)

# create the transform
vectorizer = CountVectorizer(tokenizer=LemmaTokenizer(), stop_words='english')
texts.append(facInfo)
texts.append(facAccolade)
texts.append(facHeading)
texts.append(facMenu)

# tokenize and build vocab
vectorizer.fit(texts)

myKeys = list(vectorizer.vocabulary_.keys())
myKeys.sort()
sorted_terms = {i: vectorizer.vocabulary_[i] for i in myKeys}
print(sorted_terms)


# summarize
# print(vectorizer.vocabulary_)

# encode document
vector = vectorizer.transform(texts)

# summarize encoded vector
print(vector.shape)
# print(vector.toarray())