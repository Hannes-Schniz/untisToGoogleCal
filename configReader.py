import json


class configExtract:
    conf = None
    def __init__(self):
        with open("config.json","r") as conf:
           self.conf = json.load(conf) 