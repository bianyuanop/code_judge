import os
import threading

class Runner(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(Runner)

    def run(self, limit):
        pass