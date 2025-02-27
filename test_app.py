from flask import Flask
import pytest
import requests
import time
from threading import Thread

app = Flask(__name__)

def run_app():
    app.run(host='0.0.0.0', port=5001, debug=False)

@pytest.fixture(scope="module")
def flask_server():
    server = Thread(target=run_app)
    server.daemon = True
    server.start()
    time.sleep(2)
    yield

def test_health_check(flask_server):
    response = requests.get('http://flask-app-service/health', timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "operational"
    assert "pipeline" in response.json()["message"]

if __name__ == '__main__':
    run_app()