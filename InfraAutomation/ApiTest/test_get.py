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

class PageOutputDTO:
    def __init__(self, page):
        self.result = {"page": page}
    def to_json(self):
        return self.data

def test_baba():
    url = Data.GetData.loaded_data[VarData.BaseApiUrl] +"users?page=2"
    headers = Data.GetData.get_headers()
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    
    response_data = response.json()
    output_dto = PageOutputDTO(response_data['page'])
    assert output_dto.result['page']==2

from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route('/execute', methods=['POST'])
def test_request():
    try:
        request_data = request.json
        # Perform checks on the request data
        endpoint = request_data['endpoint']
        expected_status = request_data['expectedStatus']
        expected_response_data = request_data['expectedData']
        url = Data.GetData.loaded_data[VarData.BaseApiUrl] + endpoint
        headers = Data.GetData.get_headers()
        response = requests.get(url, headers=headers, verify=False)
        response_data = response.json()
        if not expected_status:
            expected_status = 200
        if not response.status_code == int(expected_status):
            return jsonify({'error': 'expected_status is not the return status'})
        for key,val in expected_response_data.items():
            if not key in response_data:
                return jsonify({'error': 'expected key is not the return data'})
            if not val == "":
                output_dto = PageOutputDTO(response_data[key])
                if not str(output_dto.result[key])==val:
                    return jsonify({'error': 'expected val is not the return data'})
        return jsonify({'success': 'the get test is success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# backend.py



# Function to retrieve tests from the database and format them
def get_tests():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']  # Replace 'mydatabase' with your database name
    tests = db['tests']  # Create or get collection named 'config'
    tests = tests.find({})
    formatted_tests = []
    for test in tests:
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

# Route to retrieve tests
@app.route('/tests', methods=['GET'])
def get_tests_route():
    tests = get_tests()
    return jsonify(tests)

# Route to create a new test
@app.route('/create_test', methods=['POST'])
def create_test():
    data = request.json
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']  # Replace 'mydatabase' with your database name
    tests = db['tests']  # Create or get collection named 'config'
    tests.insert_one(data)
    return jsonify({'message': 'Test created successfully'}), 201

def test_request(test):
    try:
        request_data = test
        # Perform checks on the request data
        endpoint = request_data['endpoint']
        expected_status = request_data['expectedStatus']
        expected_response_data = request_data['expectedData']
        url = Data.GetData.loaded_data[VarData.BaseApiUrl] + endpoint
        headers = Data.GetData.get_headers()
        response = requests.get(url, headers=headers, verify=False)
        response_data = response.json()
        if not expected_status:
            expected_status = 200
        if not response.status_code == int(expected_status):
            return jsonify({'error': 'expected_status is not the return status'}), 500
        for key,val in expected_response_data.items():
            if not key in response_data:
                return jsonify({'error': 'expected key is not the return data'}), 500
            if not val == "":
                output_dto = PageOutputDTO(response_data[key])
                if not str(output_dto.result[key])==val:
                    return jsonify({'error': 'expected val is not the return data'}), 500
        return jsonify({'success': 'the get test is success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to execute a test
@app.route('/tests/<test_id>/execute', methods=['POST'])
def execute_test(test_id):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']  # Replace 'mydatabase' with your database name
    tests = db['tests']  # Create or get collection named 'config'
    tests = tests.find_one({'_id': ObjectId(test_id)})
    return test_request(tests)
    # Logic to execute the test based on test_id
    # This could involve sending requests to external APIs or performing actions
    # For simplicity, let's just return a success message
    # return jsonify({'message': f'Test with ID {test_id} executed successfully'})
# Route to delete a test
@app.route('/tests/<test_id>/delete', methods=['POST'])
def delete_test(test_id):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']  # Replace 'mydatabase' with your database name
    tests = db['tests']  # Create or get collection named 'config'
    tests = tests.delete_one({'_id': ObjectId(test_id)})
    return jsonify({'message': f'Test with ID {test_id} deleted successfully'})
if __name__ == '__main__':
    app.run(debug=True)

