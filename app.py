from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__, static_folder='assets', static_url_path='/assets')

# Configure API key here
# Replace with your SerpApi API key
api_key = "818c4f46c18863dc42339978de60c9a512b269e51ab8309b74baaa91db83e232"

# Home page with the form


@app.route('/assets/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'assets'), filename)


@app.route('/')
def index():
    return render_template('index.html')

# Route to process the form


# Route to process the form
@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']
    answer = generate_answer(question)
    return jsonify(answer=answer)

# Function to perform search using SerpApi


def serpapi_search(query):
    url = f"https://serpapi.com/search"
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
        "num": 10  # Number of search results to retrieve
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    return data

# Function to extract relevant content from search results


def extract_content(search_results):
    organic_results = search_results.get('organic_results', [])
    content = [result['snippet'] for result in organic_results]
    return content

# Function to generate an answer based on search results


def generate_answer(question):
    # Perform search using SerpApi
    search_results = serpapi_search(question)
    content = extract_content(search_results)

    if len(content) > 0:
        answer = "\n".join(content)  # Concatenate all content with line breaks
    else:
        answer = "No answer found."

    return answer


if __name__ == '__main__':
    app.run(debug=True)
