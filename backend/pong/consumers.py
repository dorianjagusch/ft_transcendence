# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class GameConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


import json
import time
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))



class PongConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # some class init values are set here
        # self.a =b
        # some  init are set in the upper class or superclass, i.e WebsocketConsumer
        super().__init__(*args, **kwargs)

    def connect(self):
        print(self.scope["path"])
        self.game = self.scope["path"].strip("/").replace(" ", "_")
        print(self.game)

    def disconnect(self):
        pass

    def receive(self):
        pass
 
    def propagate_state(self):
        pass

    def stream_state(self):
        pass




class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        # some class init values are set here
        # self.a =b
        # some  init are set in the upper class or superclass, i.e WebsocketConsumer
        super().__init__(*args, **kwargs)
        print('ChatConsumer *******')

    def connect(self):
        print('ChatConsumer connect *******')
        print(self.scope["path"])
        self.accept()

    def disconnect(self, close_code):
        print('ChatConsumer disconnect *******')
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print('ChatConsumer receive *******')
        for i in range(10):
            self.send(text_data=json.dumps({"message": "you said " + message}))
            print('ChatConsumer receive *******')
            time.sleep(60)