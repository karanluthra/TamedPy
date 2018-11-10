from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/run", methods=['POST'])
def run():
    if request.method == 'POST':
        code = request.get_json().get('code')
        output = runcode(code)
        print("Executed code, output is: ")
        print(output)
        return output
    return 'Expected POST request with data {"code": ""}'

@app.route("/run/<execid>", methods=['POST'])
def run_one(execid):
    print(execid)
    # print(os.listdir("."))
    # print(os.listdir("/tmp/py"))
    os.chdir("/tmp/py")

    if request.method == 'POST':
        code = request.get_json().get('code')
        output = runcode(code)
        print("Executed code, output is: ")
        print(output)
        shutdown_server()
        return output
    shutdown_server()
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

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    print(os.listdir("/tmp/py"))

    app.run(host="0.0.0.0", port=3000)
