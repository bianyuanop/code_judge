import os
import json
import queue
import socket
from termcolor import colored
from lib.runner import Runner


class JudgeHoster:
	
	'''
	using a tcp socket to get data transmission and put this in docker, that will be relatively safe
	'''
	def __init__(self, host='localhost', port=5000):
		self.max_thread = 1000
		self.count = 0

		self.judgeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.judgeServer.bind((host, port))
		self.judgeServer.listen(1)

		self.runnerThreads = queue.Queue()
		self.supposeDict = {}

	def run(self):
		while True:
			r_id, runner = self.runnerThreads.get()		
			if runner.is_alive():
				self.runnerThreads.put((r_id, runner))
			else:
				result = runner.getResult()
				if result['err_code']:
					msg = self.writeMsg(
						err_code = result['err_code'],
						error = result['errmess'],
						output = result['retval'],
						right = self.outputRight(result['retval'], self.supposeDict[r_id])
					)
					self.send(msg)
					self.supposeDict.pop(r_id)
					self.count -= 1

			if self.count >= self.max_thread:
				continue

			msg = self.receive()
			self.supposeDict[msg['jId']] = msg['suppose']
			runner = Runner(msg['lang'], msg['code'], msg['p_in'], limit={'time': 10, 'mem': None})
			runner.start()
			self.runnerThreads.put((msg['jId'], runner))
			self.count += 1
					
			
	def send(self, msg):
		if type(msg) is not str:
			print(colored('[ERRO]', 'red'), "msg to client is not str")
			return

		conn, addr= self.judgeServer.accept()
		conn.sendall(msg)

	def receive(self):
		conn, addr= self.judgeServer.accept()
		print(colored('[INFO]', 'cyan'), "Addr:" + addr + " connected.")

		data = recv_all(conn).decode('utf8')
		dataJson = self.parseMsg(data)

		return dataJson
		
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
            
        # Interface return
        # - error : err_code and errmess {'err_code': 1, 'errmess'}
        # - output : 
	def writeMsg(self, err_code, error, output, right):
		return str({
			'err_code': err_code,
			'error': error,
			'output': output,
			'right': right
			})

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


if __name__ == '__main__':
	j = JudgeHoster()
	print(j.writeMsg(1, "something", "output", True))
	supposeIn = {
		'jId':1,
		'code':"Code",
		'lang':'go',
		'suppose':'\n',
		'input':'input',
	}
	print(j.parseMsg(json.dumps(supposeIn)))
	
