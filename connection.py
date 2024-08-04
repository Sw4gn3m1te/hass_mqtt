import paho.mqtt.client as mqtt
import configparser


def get_login_secret(path):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    user = cfg["DEFAULT"]["user"]
    password = cfg["DEFAULT"]["password"]
    ip = cfg["DEFAULT"]["ip"]
    port = cfg["DEFAULT"]["port"]
    keepalive = cfg["DEFAULT"]["keepalive"]
    return (user, password), (ip, int(port), int(keepalive))


class MqttClient(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("rc: " + str(reason_code))
        self.subscribe("homeassistant/#")

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def run(self, config_file):
        init = get_login_secret(config_file)
        self.username_pw_set(*init[0])
        self.connect(*init[1])
        self.loop_forever()


if __name__ == '__main__':

    SECRET_PATH = "./secret.ini"
    client = MqttClient(mqtt.CallbackAPIVersion.VERSION2).run(SECRET_PATH)


