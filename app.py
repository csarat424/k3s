from flask import Flask, jsonify
import pytest
import requests
import time
from threading import Thread

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    # A subtle nod to chasing a DevOps role and building a career
    return jsonify({
        "status": "operational",
        "message": "Scanning the horizon for the perfect pipeline... crafting systems, one deployment at a time."
    }), 200

def run_app():
    app.run(host='0.0.0.0', port=5001, debug=False)

@pytest.fixture(scope="module")
def flask_server():
    server = Thread(target=run_app)
    server.daemon = True
    server.start()
    time.sleep(2)  # Increased delay for reliability
    yield
    # No explicit stop needed due to daemon thread and CI termination

def test_health_check(flask_server):
    response = requests.get('http://flask-app-service/health', timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "operational"
    assert "pipeline" in response.json()["message"]  # Check for DevOps flavor

if __name__ == '__main__':
    run_app()