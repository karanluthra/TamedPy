from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

from src.driver.driver import Driver
from src.driver.result import Result

driver = Driver()
driver.turnup()

class SandboxExecuter(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('srccode')
        args = parser.parse_args()
        srccode = args['srccode']
        print(srccode)

        result = driver.execute(srccode)

        response = {
            "stdout": result.stdout(),
            "stderr": result.stderr()
        }
        return response

##
## Actually setup the Api resource routing here
##
api.add_resource(SandboxExecuter, '/exec/')


if __name__ == '__main__':
    app.run(debug=True)
