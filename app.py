from flask import Flask, request, jsonify, render_template
from client import MqttClient

app = Flask(__name__)

SECRET_PATH = "./secret.ini"
client = MqttClient()
client.start(SECRET_PATH)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/button-click', methods=['POST'])
def button_click():
    data = request.get_json()
    try:
        value = int(data.get('value'))
        client.publish("hass/web/win_vol", value, 0)
    except Exception as e:
        print(e)
        try:
            value = str(data.get('value'))
            client.publish("hass/web/ctrl", value, 0)
        except Exception as e:
            print(e)

    return jsonify({'message': 'Button click registered'})


@app.route('/key-press', methods=['POST'])
def key_press():
    data = request.get_json()
    key = data.get('key')
    try:
        client.publish("hass/web/kb", key, 0)
    except Exception as e:
        print(e)
    return jsonify({'message': 'Key press registered'})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5432)
