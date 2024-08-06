import paho.mqtt.client as mqtt
import configparser
import os

if os.name == "nt":
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
        if os.name == "nt":
            self.win_controller = win_control.WinController()
        else:
            self.win_controller = None
    
    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("rc: " + str(reason_code))
        self.subscribe("hass/desktop/win_vol")
        self.subscribe("hass/desktop/kb")
        self.subscribe("hass/desktop/ctrl")

    def on_message(self, mqttc, obj, msg):
        print(f"{msg.topic}: {msg.payload}")

        try:
            data = int(msg.payload)
        except Exception as e:
            try:
                data = str(msg.payload.decode("utf-8").lower())
            except Exception as e:
                print(e)

        try:
            if msg.topic.endswith("win_vol") and os.name == "nt":
                current_volume = self.win_controller.get_volume()
                new_volume = current_volume + data
                self.win_controller.set_volume(new_volume)

            elif msg.topic.endswith("ctrl") and os.name == "nt":
                if data == "shutdown":
                    self.win_controller.shutdown()

            elif msg.topic.endswith("kb") and os.name == "nt":
                print(f"sending key {data}")
                self.win_controller.press_key(data)

            else:
                pass

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





