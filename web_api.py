import flask
import requests
import json
from flask import Flask, request
import random
from PyWordle import PyWordle
import pickle

ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'
API_KEY = 'Oqpbmxqw09Zv5GTxV1K2TUJfOhD3e1OxCi4aOzoioMbThP48Cn1OixovopqAZVHr'


def db_insert(payload: dict):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}
    payload = {
          "dataSource": "My-Cluster",
          "database": "PyWordle-API-Main",
          "collection": "storage",
          "document": {
            payload
          }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.text

def db_read(game_id: str) -> dict:
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}
    payload = {"dataSource": "My-Cluster", "database": "PyWordle-API-Main", "collection": "storage",
               "filter": {"game_id": game_id}}
    r = requests.post(ENDPOINT + '/action/findOne', headers = headers, data = json.dumps(payload))
    return r.json()


app = Flask(__name__)


@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = random.randint(15, 64)
    new_game = PyWordle()
    new_game_pickled = pickle.dumps(new_game, 0).decode()
    db_insert({'game_id': game_id, 'game_obj': new_game_pickled})
    return flask.jsonify({'game_id': game_id}, 201)

@app.route('/make_guess', methods=['POST'])
def make_guess():
    try:
        game_id = request.form['game_id']
        guess = request.form['guess']

        game = db_read(game_id)['document']['game_obj']
        game = pickle.loads(game.encode())

        game.make_guess(guess)

    except:
        return flask.jsonify(400)

