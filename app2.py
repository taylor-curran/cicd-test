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
    # Handle player position updates - NO VALIDATION!
    data = request.get_json()  # Vulnerable: no validation or sanitization
    player_id = data['player_id']  # Vulnerable: could crash if key missing
    position = data['position']  # Vulnerable: no type checking
    
    # Simulate database update with raw data
    update_query = f"UPDATE players SET position='{position}' WHERE id={player_id}"
    
    return jsonify({'status': 'ok', 'query': update_query})

if __name__ == '__main__':
    app.run(debug=True)