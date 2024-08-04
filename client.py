import paho.mqtt.client as mqtt
import configparser

import win_control
import time


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
    
    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
    
    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("rc: " + str(reason_code))
        self.subscribe("hass/desktop/win_vol")

    def on_message(self, mqttc, obj, msg):
        print(f"{msg.topic}: {msg.payload}")
        try:
            if msg.topic.endswith("win_vol"):
                win_control.set_volume(int(msg.payload))
        except Exception as e:
            print(e)

    def start(self, config_file, forever=False):
        init = get_login_secret(config_file)
        self.username_pw_set(*init[0])
        self.connect(*init[1])
        if forever:
            self.loop_forever()
        else:
            self.loop_start()

    def stop(self):
        self.loop_stop()
        self.disconnect()





