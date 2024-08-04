from client import MqttClient


if __name__ == '__main__':

    SECRET_PATH = "./secret.ini"
    client = MqttClient()
    client.start(SECRET_PATH, forever=True)
    # sender = MqttClient()
    # sender.start(SECRET_PATH)

    # try:
    #     while True:
    #         msg = input("Enter MSG")
    #         try:
    #             msg = int(msg)
    #         except:
    #             continue
    #         if msg == 1337:
    #             break
    #         sender.publish("hass/web/win_vol", msg, 0)
    # except Exception as e:
    #     print(f"{e} in client.py")

    # client.stop()
    # sender.stop()
