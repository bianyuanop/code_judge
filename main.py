import os
import json
import socket
from termcolor import colored


class JudgeHoster:
	
	'''
	using a port of tcp to get data transmission and put this in docker, that will be relatively safe
	'''
	def __init__(self, host, port):
		self.max_thread = 1000
		self.judgeServer = socket.socket((host, port))
	

	def run(self):
		while True:
                    pass

	def send(self, msg):
		pass

	def receive(self, msg):
		pass

        # Interface structure
        # - code : string
        # - lang : string
        # - suppose : string
	def parseMsg(self, msg):
            try:
                msgJson = json.loads(msg)
            except Exception as e:
                print(colored('[WARN]', 'red'), "Wrong format json input.")
                return
            
            code = msgJson['code']
            lang = msgJson['lang']
            suppose = msgJson['suppose']

            return code, lang, suppose
            
        # Interface return
        # - error : True or false
        # - output : True or false
	def writeMsg(self, error, ouput):
            return str({
                'error': error,
                'output': output
                })

        def outputRight(self, output, suppose):
            return output == suppose
