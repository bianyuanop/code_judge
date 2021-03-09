import os
import json
import socket


class JudgeHoster:
    
    '''
    using a port of tcp to get data transmission and put this in docker, that will be relatively safe
    '''
    def __init__(self, host, port):
        self.max_thread = 100
        self.judgeServer = socket.socket((host, port))
    

    def run(self):
        while True:
            pass

    def send(self, msg):
        pass

    def receive(self, msg):
        pass

    def parseCmd(self, cmd):
        pass

    def writeCmd(self, cmd):
        pass
