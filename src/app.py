
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smartcar
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Smartcar Python SDK
client = smartcar.AuthClient(
    client_id=os.environ.get('SMARTCAR_CLIENT_ID'),
    client_secret=os.environ.get('SMARTCAR_CLIENT_SECRET'),
    redirect_uri=os.environ.get('SMARTCAR_REDIRECT_URI'),
    scope=['read_vehicle_info'],
    test_mode=True
)

access = None

@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return jsonify({'url': auth_url})

@app.route('/exchange', methods=['GET'])
def exchange():
    global access
    code = request.args.get('code')
    access = client.exchange_code(code)
    return '', 200

@app.route('/vehicle', methods=['GET'])
def vehicle():
    global access
    if not access:
        return jsonify({'error': 'Not authorized'}), 401

    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    info = vehicle.info()
    return jsonify(info)

from agent.fleet_management_agent import FleetManagementAgent

@app.route('/insights', methods=['POST'])
def insights():
    global access
    if not access:
        return jsonify({'error': 'Not authorized'}), 401

    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    agent = FleetManagementAgent(access['access_token'])
    insights = agent.get_llama_insights(user_question)
    return jsonify({'insights': insights})

if __name__ == '__main__':
    app.run(port=8000)
