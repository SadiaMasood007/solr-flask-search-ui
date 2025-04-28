from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)


SOLR_URL = 'http://localhost:8983/solr/lab11_task1/select'

@app.route('/', methods=['GET'])
def search_page():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '*')
    filters = request.args.getlist('fq')

   
    params = {
        
        'q': f'(category:{query}* OR title:{query}*)',
        'fl': 'id,category,title,published,author',  
        'wt': 'json', 
    }

    if filters:
        params['fq'] = filters

    try:
        solr_response = requests.get(SOLR_URL, params=params)
        solr_response.raise_for_status()
        data = solr_response.json()
        docs = data.get('response', {}).get('docs', [])
        return jsonify(docs)
    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


