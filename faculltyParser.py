from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin  

# Database configuration
DB_NAME = 'pages'
DB_HOST = 'localhost'
DB_PORT = 27017
DB_COLLECTION = 'pages'
DB_INDEX = 'faculty_index'

# Connect to MongoDB
client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
pages_collection = db[DB_COLLECTION]
faculty_index_collection = db[DB_INDEX]
print("Connected to MongoDB and selected appropriate database and collections.")

def is_faculty_page(url):
    return "/faculty/" in url

def extract_faculty_info(faculty_page):
    url = faculty_page['url']
    html_content = faculty_page['html']

    if not is_faculty_page(url):
        print(f"Skipping non-faculty page: {url}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    print(f"Processing faculty page: {url}")

    fac_info_container = soup.find('div', class_='fac-info')
    if not fac_info_container:
        print("Faculty information container not found.")
        return

    image_tag = fac_info_container.find('img')
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']
        # Ensure the image URL is absolute
        if not image_url.startswith('http'):
            image_url = urljoin(url, image_url)
    else:
        image_url = "default_image.jpg"  # Fallback image

    # Extracting faculty details
    name = fac_info_container.h1.get_text(strip=True) if fac_info_container.h1 else "Not Available"
    email = fac_info_container.find('a', {'href': re.compile(r'mailto:')}).get_text(strip=True) if fac_info_container.find('a', {'href': re.compile(r'mailto:')}) else "Not Available"
    phone = fac_info_container.find('p', class_='phoneicon').get_text(strip=True) if fac_info_container.find('p', class_='phoneicon') else "Not Available"

    print(f"Extracted Name: {name}")
    print(f"Extracted Email: {email}")
    print(f"Extracted Phone: {phone}")
    print(f"Extracted Image URL: {image_url}")

    faculty_member_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'url': url,
        'page_id': faculty_page['_id'],
        'image_url': image_url
    }
    faculty_index_collection.insert_one(faculty_member_data)
    print(f"Indexed faculty member: {name}")

def process_faculty_pages():
    faculty_pages = pages_collection.find()
    for faculty_page in faculty_pages:
        extract_faculty_info(faculty_page)

    client.close()
    print("MongoDB connection closed and processing complete.")

if __name__ == '__main__':
    process_faculty_pages()
