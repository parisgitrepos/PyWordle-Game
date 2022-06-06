import flask
import requests
import json
from flask import Flask, request
import random
from PyWordle import PyWordle
import pickle

ENDPOINT = 'https://data.mongodb-api.com/app/data-kgmzc/endpoint/data/v1'
API_KEY = 'Oqpbmxqw09Zv5GTxV1K2TUJfOhD3e1OxCi4aOzoioMbThP48Cn1OixovopqAZVHr'


def serialize_game(game: PyWordle):
    return pickle.dumps(game, 0).decode()


def deserialize_game(game: str):
    return pickle.loads(game.encode())


def db_game_insert(game_id: str, game_obj: PyWordle):
    headers = {'Content-Type': 'application/json', 'Access-Control-Request-Headers': '*', 'api-key': API_KEY}
    payload = {
        "dataSource": "My-Cluster",
        "database": "PyWordle-API-Main",
        "collection": "storage",
        "document": {
            'game_id': game_id,
            'game_obj': serialize_game(game_obj)
        }
    }
    r = requests.post(ENDPOINT + '/action/insertOne', headers=headers, data=json.dumps(payload))
    return r.text


def db_game_read(game_id: str) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': API_KEY
    }
    payload = {
        "dataSource": "My-Cluster",
        "database": "PyWordle-API-Main",
        "collection": "storage",
        "filter":
            {
                "game_id": game_id
            }
    }
    r = requests.post(ENDPOINT + '/action/findOne', headers=headers, data=json.dumps(payload))
    return r.json()['document']['game_obj']


def db_game_update(game_id: str, updated_game: PyWordle):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': API_KEY
    }
    payload = {
        "dataSource": "My-Cluster",
        "database": "PyWordle-API-Main",
        "collection": "storage",
        "filter": {
                   "game_id": game_id
               },
        "update":
            {
            'game_id': game_id,
            'game_obj': serialize_game(updated_game)
            }
    }
    r = requests.post(ENDPOINT + '/action/updateOne', headers=headers, data=json.dumps(payload))
    return r.json()


app = Flask(__name__)


@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = str(random.randint(15, 64))
    new_game = PyWordle()
    db_game_insert(game_id = game_id, game_obj = new_game)
    return flask.jsonify({'game_id': game_id})


@app.route('/make_guess', methods=['POST'])
def make_guess():
    try:
        game_id = request.get_json(force = True)['game_id']
        # Must convert game_id to str when querying MongoDB
        game_id = str(game_id) if type(game_id) == int else game_id
        guess = request.get_json(force = True)['guess']

        game = db_game_read(game_id)
        game = deserialize_game(game)
        game_response = game.make_guess(guess)

        db_game_update(game_id, game)

        return flask.jsonify({'game_response': game_response})

    except:
        return flask.jsonify('Bad request')


@app.route('/game_info', methods = ['POST'])
def game_info():
    try:
        game_id = request.get_json(force = True)['game_id']
        # Must convert game_id to str when querying MongoDB
        game_id = str(game_id) if type(game_id) == int else game_id

        game = db_game_read(game_id)
        game = deserialize_game(game)
        game_info_response = game.get_info()

        return flask.jsonify({'game_response': game_info_response})

    except:
        return flask.jsonify('Bad request')


@app.route('/check_game_over', methods = ['POST'])
def check_game_over():
    try:
        game_id = request.get_json(force = True)['game_id']
        # Must convert game_id to str when querying MongoDB
        game_id = str(game_id) if type(game_id) == int else game_id

        game = db_game_read(game_id)
        game = deserialize_game(game)
        check_game_over_response = game.check_game_over()

        return flask.jsonify({'game_response': check_game_over_response})

    except:
        return flask.jsonify('Bad request')


if __name__ == '__main__':
    app.run()

