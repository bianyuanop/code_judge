import os
import subprocess
from termcolor import colored


Errors = {
    0: "RE",
    1: "TLE",
    2: "WA",
    3: "",
}
class Runner:
    '''
    a code runner 
    '''
    
    def __init__(self, lang, code, limit):
        '''
        limit parse
            - time
            - mem
        '''
        with open("temp.cpp", 'w') as f:
            f.write(code)

        self.filename = 'temp.cpp'
        self.lang = lang
        self.timeLimit = limit['time']
        self.memLimit = limit['mem']

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
        if self.lang.lower() == 'python':
            cmd = ['python', self.filename]
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            err_code = p.wait()
            retval = p.stdout.read().decode('utf8')
            errmess = p.stderr.read().decode('utf8')

            if err_code:
                print(colored('[INFO]', 'red'), 'error occured, error code: {0}, error message: {1}'.format(err_code, errmess))
            else:
                print(colored('[INFO]', 'green'), "running finished ", retval)
                return retval

        if self.lang.lower() == 'go':
            cmd = ['go run', self.filename]
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            err_code = p.wait()
            retval = p.stdout.read().decode('utf8')
            errmess = p.stderr.read().decode('utf8')

            if err_code:
                print(colored('[INFO]', 'red'), 'error occured, error code: {0}, error message: {1}'.format(err_code, errmess))
            else:
                print(colored('[INFO]', 'green'), "running finished ", retval)
                return retval

        if self.lang.lower() == 'c':
            cmd = ['gcc', self.filename, '-o', 'start', '&', './start']
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            err_code = p.wait()
            retval = p.stdout.read().decode('utf8')
            errmess = p.stderr.read().decode('utf8')

            if err_code:
                print(colored('[INFO]', 'red'), 'error occured, error code: {0}, error message: {1}'.format(err_code, errmess))
            else:
                print(colored('[INFO]', 'green'), "running finished ", retval)
                return retval

        if self.lang.lower() == 'cpp':
            cmd = ['g++', self.filename, '-o', 'start', '&', './start']
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            err_code = p.wait()
            # retval = p.stdout.read().decode('utf8')
            retval = p.stdout.read()
            errmess = p.stderr.read()

            if err_code:
                print(colored('[INFO]', 'red'), 'error occured, error code: {0}, error message: {1}'.format(err_code, errmess))
            else:
                print(colored('[INFO]', 'green'), "running finished ", retval)
                return retval

if __name__ == '__main__':
    limit = {
        'time': None,
        'mem': None
    }
    lang = 'cpp'
    code = '''#include <iostream>\nusing namespace std;\n
int main(){\ncout << "Hello, world" << endl;\nreturn 0;\n}'''
    r = Runner(lang, code, limit)
    r.run()