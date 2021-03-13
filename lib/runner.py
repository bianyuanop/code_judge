import os
import subprocess
import threading
from termcolor import colored


if not os.path.exists('tmp'):
	os.mkdir("tmp")


class Runner(threading.Thread):
	'''
	a code runner 
	'''
	
	def __init__(self, lang, code, p_in, limit, subId=0):
		'''
		limit parse
			- time
			- mem
		'''
		threading.Thread.__init__(Runner)

		self.prefix = 'tmp/'
		self.result = {}
		self.p_in = p_in
		if lang == 'cpp':
			self.filename = 'temp' + str(subId) + '.cpp'
		elif lang == 'python':
			self.filename = 'temp' + str(subId) + '.py'
		elif lang == 'go':
			self.filename = 'temp' + str(subId) + '.go'
		elif lang == 'c':
			self.filename = 'temp' + str(subId) + '.c'

		with open(self.prefix + self.filename, 'w') as f:
			f.write(code)

		self.lang = lang
		self.timeLimit = limit['time']
		self.memLimit = limit['mem']

	def getResult(self):
		'''This function must be called after join()'''
		return self.result
	
	def sub(self, cmd, p_in=None):
		p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if p_in:
			out, err = p.communicate(input=p_in, timeout=self.timeLimit)
			if err:
				return 1, out, err
			else:
				return 0, out, err

		err_code = p.wait()
		retval = p.stdout.read().decode('utf8')
		errmess = p.stderr.read().decode('utf8')

		return err_code, retval, errmess

	def run(self):
		'''
		using ulimit for mem and time limit
		and using subprocess for error code, stdout, error message check
		example:
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			errcode = p.wait()
			retval = p.stdout.read()
			errmess = p.stderr.read()
		'''
	
		try:

			if self.lang.lower() == 'python':
				cmd = ['python', self.prefix + self.filename]
				err_code, retval, errmess = self.sub(cmd, self.p_in)
			elif self.lang.lower() == 'go':
				cmd = ['go', 'build', self.prefix + self.filename]
				err_code, retval, errmess = self.sub(cmd, self.p_in)
				if not err_code:
					cmd = ['./' + self.filename.split('.')[0]]
					err_code, retval, errmess = self.sub(cmd, self.p_in)

			elif self.lang.lower() == 'cpp':
				cmd = ['g++', self.prefix + self.filename, '-o', self.filename.split('.')[0]]
				err_code, retval, errmess = self.sub(cmd, self.p_in)
				if not err_code:
					cmd = ['./' + self.filename.split('.')[0]]
					err_code, retval, errmess = self.sub(cmd, self.p_in)
					
			elif self.lang.lower() == 'c':
				cmd = ['gcc' , self.prefix + self.filename , '-o' , self.filename.split('.')[0]]
				err_code, retval, errmess = self.sub(cmd, self.p_in)
				if not err_code:
					cmd = ['./' + self.filename.split('.')[0]]
					err_code, retval, errmess = self.sub(cmd, self.p_in)
		except Exception as e:
			print(colored('[ERROR]', 'red'), "Something wrong happend: ", e)
			return

		self.result['err_code'] = err_code
		self.result['retval'] = retval
		self.result['errmess'] = errmess
