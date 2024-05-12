from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

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

def parseFaculty():
    query = {'url': {'$regex': "^https:\/\/www\.cpp\.edu\/faculty\/.*$"}}

    faculty_links = list(pages.find(query))
    print(faculty_links)

parseFaculty()