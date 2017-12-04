from flask import Flask
from flask import request
import json
app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    data = request.data
    dataDict = json.loads(data)
    print(dataDict)

    tempResponse = json.dumps(
        {'woff': 'https://s3.ap-northeast-2.amazonaws.com/fontto/example/UhBeeKang-Ja.woff'}
    )
    response = app.response_class(
        response=tempResponse,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)