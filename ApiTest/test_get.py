import json
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



# from flask import Flask, jsonify
# import urllib.parse
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Add this line to enable CORS for all routes

# @app.route('/<path:endpoint>')
# def test_endpoint(endpoint):
#     decoded_endpoint = urllib.parse.unquote(endpoint)
#     url = Data.GetData.loaded_data[VarData.BaseApiUrl] + decoded_endpoint
#     print(url)
#     headers = Data.GetData.get_headers()
#     response = requests.get(url, headers=headers, verify=False)
#     assert response.status_code == 200
#     response_data = response.json()
#     output_dto = PageOutputDTO(response_data['page'])
#     page_index = [idx for idx,s in enumerate(decoded_endpoint.split("=")) if 'page' in s.lower()][0]
#     page_num = int(decoded_endpoint.split("=")[page_index + 1])
#     assert output_dto.result['page']==int(page_num)
#     return jsonify({'message': f'Endpoint {decoded_endpoint} is okay!'})



from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route('/test-request', methods=['POST'])
def test_request():
    try:
        request_data = request.json
        # Perform checks on the request data
        endpoint = request_data['endpoint']
        expected_status = request_data['expectedStatus']
        expected_response_data = request_data['expectedResponseData']
        ret = jsonify({'success': 'the get test is success'})
        url = Data.GetData.loaded_data[VarData.BaseApiUrl] + endpoint
        headers = Data.GetData.get_headers()
        response = requests.get(url, headers=headers, verify=False)
        response_data = response.json()
        if not expected_status:
            expected_status = 200
        if not response.status_code == int(expected_status):
            ret = jsonify({'error': 'expected_status is not the return status'})
            return ret
        for key,val in expected_response_data.items():
            if not key in response_data:
                ret = jsonify({'error': 'expected key is not the return data'})
                return ret
            if not val == "":
                output_dto = PageOutputDTO(response_data[key])
                if not str(output_dto.result[key])==val:
                    ret = jsonify({'error': 'expected val is not the return data'})
                    return ret
        return ret
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
