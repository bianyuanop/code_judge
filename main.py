import os
import json
import queue
import socket
from termcolor import colored
from lib.runner import Runner


class JudgeHoster:
	
	'''
	using a tcp socket to get data transmission and put this in docker, that will be relatively safe
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # use this for long term of socket using for client socket
	'''
	def __init__(self, host='localhost', port=5000):
		self.max_thread = 1000
		self.count = 0

		self.judgeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.judgeServer.bind((host, port))

		self.runnerThreads = queue.Queue()
		self.supposeDict = {}

	def run(self):
		self.judgeServer.listen(1)
		conn, addr = self.judgeServer.accept()
		while True:
			# in one loop, just one type of instruction will be execute
			# send or recv, once one of them been executed, then continue next loop

			# Check those already done tasks
			toSend = None
			print("is empty: ", self.runnerThreads.empty())
			while not self.runnerThreads.empty():
				r_id, runner = self.runnerThreads.get()
				if runner.is_alive():
					self.runnerThreads.put((r_id, runner))
					continue	

				runResult = runner.getResult()
				print(runResult)
				toSend = {
					'jId': r_id,
					'err_code': runResult['err_code'],
					'error': runResult['errmess'],
					'output': runResult['retval'],
					'right': self.outputRight(runResult['retval'], self.supposeDict[r_id])
				}
				self.supposeDict.pop(r_id)
				break
			
			# if no process is done or judge list empty socket send b''
			if toSend:
				conn.sendall(json.dumps(toSend).encode('utf8'))
				continue
			else:
				conn.send(b'')

			# Producer must send b'' then loop can go on if there is no judgement any more
			msg = recv_all(conn)
			print("MSG: ", msg)
			if not msg:
				continue	

			msgJson = self.parseMsg(msg)	
			r_id = msgJson['jId']
			runner = Runner(msgJson['lang'], msgJson['code'], msgJson['p_in'],{'time':10, 'mem': None})
			runner.start()
			self.supposeDict[r_id] = msgJson['suppose']

			self.runnerThreads.put((r_id, runner))

					
		
	def parseMsg(self, msg):
        # Interface structure
		# - jId : judge id -> int
        # - code : string
        # - lang : string
        # - suppose : string
		# - input : string
		try:
			msgJson = json.loads(msg)
		except Exception as e:
			print(colored('[WARN]', 'red'), "Wrong format json input.")
			return
		
		jId = msgJson['jId']
		code = msgJson['code']
		lang = msgJson['lang']
		suppose = msgJson['suppose']
		p_in = msgJson['input']

		return {
			"jId": jId,
			"code": code,
			"lang": lang,
			"suppose": suppose,
			"p_in": p_in
		}
            
	def outputRight(self, output, suppose):
		return output == suppose


def recv_all(sock):
	BUFF_SIZE = 4096 # 4 KiB
	data = b''
	while True:
		part = sock.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	
	return data
