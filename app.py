from flask import Flask, jsonify
from algo import get_times
from flask_cors import CORS
from flask import request
import os

port = int(os.environ.get('PORT', 5001))
app = Flask(__name__)
app.port = port
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    times = get_times()
    return jsonify(times)


@app.route('/api/schedule_patient', methods=['GET'])
def schedule_patient():
    data_str = request.data  # Decode bytes to string
    return jsonify(data_str)

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
