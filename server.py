from flask import Flask
from flask import request
import json
from back_processing import back_processing
from utils import set_logging

app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():
    data = request.data
    dataDict = json.loads(data)

    # set log
    set_logging('server_log.txt')

    userId = dataDict['userId']
    unicodes = dataDict['unicodes']
    count = dataDict['count']
    env = dataDict['env']

    woff_addr = back_processing(userId, count, unicodes, env)
    tempResponse = json.dumps(
        {
            'woff': woff_addr
        }
        # {'woff': 'https://s3.ap-northeast-2.amazonaws.com/fontto/example/UhBeeKang-Ja.woff'}
    )
    response = app.response_class(
        response=tempResponse, status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
