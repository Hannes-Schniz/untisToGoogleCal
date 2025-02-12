import json
import re


class configExtract:
    conf = None
    def __init__(self):
        with open("config.json","r") as conf:
           conf = json.load(conf)
        try:
            #self.configCheck(conf) 
            self.conf = conf
            #print(conf)
        except Exception as e:
            print(repr(e))
            raise Exception("Failed to load config")
        
           
           

    def configCheck(self,conf):
        if conf['group'] not in ["A","B"]:
            raise Exception("Group not configured")
        if re.match(conf['classID'], "[0-9][0-9][0-9][0-9]") == None or len(conf['classID']) != 4:
            raise Exception("No valid class ID configured")
        if re.match(conf['weeksAhead'], "[0-9]") == None or len(conf['weeksAhead']) != 1:
            raise Exception("No valid weeks lookahead configured")