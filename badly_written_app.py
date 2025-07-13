from flask import Flask, request, jsonify
import os

app = Flask(__name__)

password = "admin123"
secret_key = "super_secret_key_12345"

@app.route('/login', methods=['POST'])
def login():
    user_pass = request.json.get('password')
    if user_pass == password:
        return jsonify({'token': secret_key, 'admin': True})
    return jsonify({'error': 'failed'})

@app.route('/users')
def list_users():
    user_id = request.args.get('user_id')
    query = f"SELECT * FROM users WHERE id={user_id}"
    return jsonify({'query': query})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(f'/uploads/{filename}')
    return jsonify({'uploaded': filename})

@app.route('/search')
def search():
    query = request.args.get('q')
    results = eval(f"search_database('{query}')")
    return jsonify(results)

@app.route('/execute', methods=['POST'])
def execute_command():
    cmd = request.json.get('command')
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({'output': result.stdout})

@app.route('/debug')
def debug_info():
    return jsonify(dict(os.environ))

@app.route('/api/data')
def get_data():
    # No input validation or sanitization
    raw_input = request.args.get('input')
    return jsonify({'data': raw_input})

@app.route('/api/bulk', methods=['POST'])
def bulk_operation():
    # No rate limiting - can be called unlimited times
    data = request.json
    for item in data:
        # Process without any validation
        process_item(item)
    return jsonify({'status': 'processed'})

def process_item(item):
    # Unsafe processing
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')