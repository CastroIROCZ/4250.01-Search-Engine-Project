from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)
print("test")
@app.route('/')
def home():
    # Render the HTML file
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the search query from the request
    data = request.get_json()
    query = data.get('query', '').strip()

    # Print the query to the terminal for verification
    print(f"Received search query: {query}")
    print("Query received")

    # Return dummy data as JSON
    results = [
        {
            'name': 'Google', # For now set name to Goolge
            'link': 'https://www.google.com' # For now set link to Google website
        }
    ]
    return jsonify({'results': results})

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


