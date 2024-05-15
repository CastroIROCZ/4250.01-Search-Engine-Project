Faculty Search Engine:

Overview
This project is a local faculty search engine that allows users to saerch for faculty information based on various research interests, publications, and more.
The backend is developed in Python using Flask, and the frontend using a simple HTML/CSS/JavaScript stack application. 

Installation
1. Clone the repository
2. Navigate to the project directory.
3. Install the required Python packages:
   pip install flask flask-cors pymongo beautifulsoup4 sklearn nltk
4. You may need to clear previous databases created during the testing phase.
5. Ensure MongoDB is set up properly and is installed successfully on your computer
6. Ensure your MongoDB port matches that of the code 

Running the Application:
1. Run the app.py file
2. An HTTP link will be displayed in the terminal. Click or copy that link into your browser (CHROME OR MICROSOFT EDGE HAS BEEN VERIFIED TO WORK)
3. The web app should appear on your browser. Type in a query into the search bar like "California" or "Professional Engineer". Results will include
   a. Faculty professional picture
   b. Faculty name
   c. Faculty email
   d. Faculty phone number
   e. Link to Faculty webpage

Additional Notes:
This app is made to run locally and is not intended to run on live servers 
