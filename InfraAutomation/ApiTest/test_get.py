import json
from bson import ObjectId
import pymongo
import requests
import sys
import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)
 
# importing
import Data.GetData
from Data.GetData import VarData, data

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
db_config =  db['config']
db_config = db_config.find_one()
db_tests = db['tests'] 

from flask_cors import CORS
from flask import Flask, request, jsonify
# Get test table 
def get_tests():
    test_table = db_tests.find({})
    formatted_tests = []
    for test in test_table:
        formatted_test = {
            'id': str(test['_id']),
            'name': test['testName'],
            'type': test['testType'],
            'endpoint': test['endpoint'],
            'expectedStatus': test['expectedStatus'],
            'expectedData': test.get('expectedData', {}),
            'dataToSend': test.get('dataToSend', {})
        }
        formatted_tests.append(formatted_test)
    return formatted_tests

app = Flask(__name__)
CORS(app)
@app.route('/execute', methods=['POST'])
def execute_new_test():
    return test_request(request.json)
    
def test_request(request_data):
    try:
        # Perform checks on the request data
        endpoint = request_data['endpoint']
        expected_status = request_data['expectedStatus']
        expected_response_data = request_data['expectedData']
        url = db_config["API"]["BaseApiUrl"] + endpoint
        headers = db_config["API"]["Headers"]
        response = requests.get(url, headers=headers, verify=False)
        response_data = response.json()
        if not expected_status:
            expected_status = 200
        if not response.status_code == int(expected_status):
            return jsonify({'error': f'The expected status is:{expected_status}, the response status code is: {response.status_code}'}), 500
        
        for key,val in expected_response_data.items():
            if not key in response_data:
                return jsonify({'error': 'expected key is not the return data'})
            if not val == "":
                if not str(response_data[key])==val:
                    return jsonify({'error': f'expected val {val}is not the return data{response_data[key]}'})
        return jsonify({'success': 'the get test is success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# backend.py
# Rout test data  from db
@app.route('/tests', methods=['GET'])
def get_tests_route():
    tests = get_tests()
    return jsonify(tests)

# Route to create a new test
@app.route('/create_test', methods=['POST'])
def create_test():
    data = request.json
    db_tests.insert_one(data)
    return jsonify({'message': 'Test created successfully'}), 201




# Route id from user and send request data
@app.route('/tests/<test_id>/execute', methods=['POST'])
def execute_test(test_id):
    tests = db_tests.find_one({'_id': ObjectId(test_id)})
    return test_request(tests)


@app.route('/tests/<test_id>/delete', methods=['POST'])
def delete_test(test_id):
    tests = db_tests.delete_one({'_id': ObjectId(test_id)})
    return jsonify({'message': f'Test with ID {test_id} deleted successfully'})
if __name__ == '__main__':
    app.run(debug=True)

