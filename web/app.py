from flask import Flask, request, jsonify, render_template
from client import MqttClient
import win_control

app = Flask(__name__)

SECRET_PATH = "../secret.ini"
client = MqttClient()
client.start(SECRET_PATH)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/button-click', methods=['POST'])
def button_click():
    data = request.get_json()
    value = int(data.get('value'))
    current_volume = win_control.get_volume()
    new_volume = current_volume + value
    client.publish("hass/web/win_vol", new_volume, 0)
    return jsonify({'message': 'Button click registered'})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5432)
