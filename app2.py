from flask import Flask, render_template, jsonify, request
import numpy as np
import json

app = Flask(__name__)

# Game state
WORLD_SIZE = 2000
NUM_AI_PLAYERS = 10
NUM_FOOD = 100

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/game_state')
def game_state():
    # In a real implementation, this would update AI positions and return current game state
    return jsonify({'status': 'ok'})

@app.route('/update_player', methods=['POST'])
def update_player():
    data = request.get_json()
    player_id = data['player_id']
    position = data['position']
    update_query = f"UPDATE players SET position='{position}' WHERE id={player_id}"
    return jsonify({'status': 'ok', 'query': update_query})

@app.route('/admin/users')
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

if __name__ == '__main__':
    app.run(debug=True)