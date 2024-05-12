from urllib.parse import urlparse
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import requests


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


def storePage(url, html):
    pagesDoc = {
        "url": url,
        "html": html
    }
    # Insert the document
    pages.insert_one(pagesDoc)


def target_page(bs):
    stop_criteria = bs.find('div', {'class': 'fac-staff'})
    stop_criteria1 = bs.find('div', {'class': 'fac-info'})
    stop_criteria2 = bs.find('div', {'class': 'accolades'})
    if stop_criteria and stop_criteria1 and stop_criteria2:
        return True


def get_crawler_thread(frontier, num_targets):
    faculty_page = True
    targets_found = 0
    while frontier:
        url = frontier.pop(0)
        req = requests.get(url)
        html = req.text
        bs = BeautifulSoup(html, 'html.parser')
        stop_faculty = bs.find('h2', string="Faculty")
        includeCPPUrl = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)  # https://www.cpp.edu
        print(url)
        storePage(url, html)

        if stop_faculty and faculty_page:
            faculty_page = False
            frontier.clear()
            frontier.append(url)
            pagesSet.add(url)
            print('Found')
        else:
            if target_page(bs):
                targets_found += 1
                target_page_docs.append(url)
                print('Found')
                if targets_found == num_targets:
                    print('10 found')
                    frontier.clear()
                    return target_page_docs
            else:
                for link in bs.find_all('a', href=re.compile('^(/|.*' + includeCPPUrl + ')')):
                    if 'href' in link.attrs:
                        if link.attrs['href'] not in pagesSet:
                            if link.attrs['href'].startswith('/'):
                                frontier.append(includeCPPUrl + link.attrs['href'])
                                pagesSet.add(includeCPPUrl + link.attrs['href'])
                            else:
                                newPage = link.attrs['href']
                                frontier.append(newPage)
                                pagesSet.add(newPage)


if __name__ == '__main__':
    frontier = ['https://www.cpp.edu/engineering/ce/index.shtml']
    # Connecting to the database
    db = connectDataBase()

    # Creating a collection
    pages = db.pages
    pagesSet = set()
    target_page_docs = []
    target_page_url = get_crawler_thread(frontier, 10)
