from flask import Flask, request
import json
from model import predict
from data import prepare_data
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Hiiiiiiii'


@app.route('/getlist', methods=['GET'])
def gettestlist():
    if request.method == 'GET':
        publisher = request.args.get('publisher')
        input1_csv_path = '../notebooks/Eye/headline-test-%s.csv' % (publisher)
        input2_csv_path = '../notebooks/Eye/output-%s.csv' % (publisher)
        data = pd.concat([pd.read_csv(input1_csv_path),
                          pd.read_csv(input2_csv_path)], axis=1)
        data = data.sample(100)
        data = data[['headline', 'Actual views',
                     'Predicted views', 'class']].to_dict('records')

        return json.dumps(data, ensure_ascii=False).encode('utf8')
    else:
        return []


@app.route('/get-predicted', methods=['GET'])
def getpredicted():
    input_path = '../notebooks/Eye/output-thaipbs.csv'
    data = pd.read_csv(input_path)
    print(data)
    return json.dumps([], ensure_ascii=False).encode('utf8')


@app.route('/popularity', methods=['POST'])
def popularity():
    if request.method == 'POST':
        result = gettestlist()
        # features = prepare_data(request.form['data'])
        # result = predict(features)
        return json.dumps(result)
