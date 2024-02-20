import React, { useState } from 'react';

const App = () => {
  const [endpoint, setEndpoint] = useState('');
  const [expectedStatus, setExpectedStatus] = useState('');
  const [expectedResponseData, setExpectedResponseData] = useState('');
  const [response, setResponse] = useState('');

  const handleTestRequest = async () => {
    try {
      const requestBody = {
        endpoint: endpoint,
        expectedStatus: expectedStatus,
        expectedResponseData: JSON.parse(expectedResponseData) // Parse response data string to JSON
      };
      const response = await fetch(`http://localhost:5000/test-request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      setResponse(JSON.stringify(data));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Test Backend Endpoint</h1>
      <div>
        <label htmlFor="endpointInput">Enter Endpoint URL:</label>
        <input
          id="endpointInput"
          type="text"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
          placeholder="e.g., /api/resource"
        />
      </div>
      <div>
        <label htmlFor="expectedStatusInput">Expected Response Status:</label>
        <input
          id="expectedStatusInput"
          type="text"
          value={expectedStatus}
          onChange={(e) => setExpectedStatus(e.target.value)}
          placeholder="e.g., 200"
        />
      </div>
      <div>
        <label htmlFor="expectedResponseDataInput">Expected Response Data (key-value pairs):</label>
        <textarea
          id="expectedrRsponseDataInput"
          value={expectedResponseData}
          onChange={(e) => setExpectedResponseData(e.target.value)}
          placeholder='e.g., {"key1": "value1", "key2": "value2"}'
        />
      </div>
      <button onClick={handleTestRequest}>Test Request</button>
      <div>
        <h2>Response:</h2>
        <pre>{response}</pre>
      </div>
    </div>
  );
};

export default App;
