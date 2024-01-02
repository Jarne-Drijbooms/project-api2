import requests
import json

def test_players():
    response = requests.get('http://127.0.0.1:8000/players/me')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)

def test_player():
    response = requests.get('http://127.0.0.1:8000/players')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_player_id():
    response = requests.get('http://127.0.0.1:8000/players/{speler_id}')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_single():
    response = requests.get('http://127.0.0.1:8000/single/')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)


def test_dubble():
    response = requests.get('http://127.0.0.1:8000/dubble/')
    assert response.status_code == 200
    response_dictionary = json.loads(response.text)