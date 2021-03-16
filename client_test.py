import socket
import queue
import json
from time import sleep
from main import recv_all

def getAMsg(sock , location=('localhost', 5000)):
	data = recv_all(sock)
	return data.decode('utf8')

def putAMsg(sock, msg, location=('localhost', 5000)):
	if type(msg) is bytes:
		toPut = msg
	else:
		msg = json.dumps(msg)
		toPut = msg.encode('utf8')
	sock.sendall(toPut)
	
toSendCpp = {
	'jId': 1,
	'code': '''#include <iostream>
using namespace std;
int main() {
cout << "Hello, cpp" << endl;
return 0;
}''',
	'lang': 'cpp',
	'suppose': 'Hello, cpp\n',
	'input': None } 
toSendPy = {
	'jId': 2,
	'code': '''print("Hello, python")''',
	'lang': 'python',
	'suppose': 'Hello, python\n',
	'input': None
}

toSendGo = {
	'jId': 3,
	'code': '''package main
import "fmt"
func main() {
fmt.Println("Hello, go")
}
''',
	'lang': 'go',
	'suppose': 'Hello, go\n',
	'input': None
}

toSendC = {
	'jId': 4,
	'code': r'''#include <stdio.h>
int main() {
printf("Hello, go\n");
return 0;
}''',
	'lang': 'c',
	'suppose': 'Hello, go\n',
	'input': None
}
	

if __name__ == '__main__':
	addr, port = 'localhost', 5000

	q = queue.Queue()

	q.put(toSendCpp)
	q.put(toSendPy)
	q.put(toSendGo)
	q.put(toSendC)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.connect((addr, port))

	while True:
		if not q.empty():
			toPut = q.get()	
			putAMsg(sock, toPut)
			print("MSG PUT: ", toPut)
		else:
			putAMsg(sock, b'')

		msgGot = getAMsg(sock)
		if msgGot:
			print("MSG GOT: ", msgGot)
	
