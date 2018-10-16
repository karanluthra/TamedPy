from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/run", methods=['POST'])
def run():
    if request.method == 'POST':
        code = request.form['code']
        output = runcode(code)
        print("Executed code, output is: ")
        print(output)
        return output
    return 'Expected POST request with data {"code": ""}'

def runcode(code):
    with open("unsafe.py", "w") as f:
        f.write(code)
    # exec python unsafe.py
    completedProc = subprocess.run(
        ["python", "unsafe.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = ''
    if completedProc.returncode == 0:
        output = completedProc.stdout
    else:
        output = "Error: {}".format(completedProc.returncode)
        output += str(completedProc.stdout)
    return output

if __name__ == '__main__':

#     print(runcode("print(2**12)"))
#     code = '''import math
# print(math.sqrt(2500))
#     '''
#     print(runcode(code))
#     code = '''import os
# print(os.environ['PATH'])
#     '''
#     print(runcode(code))

    app.run(host="0.0.0.0", port=3000)
