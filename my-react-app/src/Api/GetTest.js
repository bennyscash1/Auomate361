// NewTestForm.js
import React, { useState } from 'react';
import axios from 'axios';

const NewTestForm = () => {
  const [testName, setTestName] = useState('');
  const [testType, setTestType] = useState('');
  const [endpoint, setEndpoint] = useState('');
  const [expectedStatus, setExpectedStatus] = useState('');
  const [expectedData, setExpectedData] = useState('{"":""}');
  const [dataToSend, setDataToSend] = useState('{"":""}');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [loading2, setLoading2] = useState(false);
  const [result2, setResult2] = useState('');
  const executeTest = async () => {
    try {
      setLoading(true);
      const requestBody = {
        testName: testName,
        testType: testType,
        endpoint: endpoint,
        expectedStatus: expectedStatus,
        expectedData: JSON.parse(expectedData),
        dataToSend: JSON.parse(dataToSend)
      };
      const response = await axios.post('http://localhost:5000/execute', requestBody
      );
      setResult(JSON.stringify(response.data));
    } catch (error) {
      console.error('Error executing test:', error);
    } finally {
      setLoading(false);
    }
  };
  const saveTest = async () => {
    try {
      setLoading2(true);
      const requestBody = {
        testName: testName,
        testType: testType,
        endpoint:endpoint,
        expectedStatus: expectedStatus,
        expectedData: JSON.parse(expectedData),
        dataToSend: JSON.parse(dataToSend)
      };
      const response = await axios.post('http://localhost:5000/create_test', requestBody);
      setResult2(JSON.stringify(response.data));
    } catch (error) {
      console.error('Error save test:', error);
    } finally {
      setLoading2(false);
    }
  };

  return (
    <div>
      <h1>Create New Test</h1>
      <input type="text" placeholder="Test Name" value={testName} onChange={e => setTestName(e.target.value)} />
      <input type="text" placeholder="Test Type" value={testType} onChange={e => setTestType(e.target.value)} />
      <input type="text" placeholder="Endpoint" value={endpoint} onChange={e => setEndpoint(e.target.value)} />
      <input type="text" placeholder="Expected Status" value={expectedStatus} onChange={e => setExpectedStatus(e.target.value)} />
      <input type="text" placeholder='Expected Data e.g., {"key1": "value1", "key2": "value2"}' value={expectedData} onChange={e => setExpectedData(e.target.value)} />
      <input type="text" placeholder='Data to Send e.g., {"key1": "value1", "key2": "value2"}' value={dataToSend} onChange={e => setDataToSend(e.target.value)} />
      <button onClick={saveTest} disabled={loading2}>{loading2 ? 'Save...' : 'Save Test'}</button>
      <button onClick={executeTest} disabled={loading}>{loading ? 'Executing...' : 'Execute Test'}</button>
      {result && <div>{result}</div>}
      {result2 && <div>{result2}</div>}

    </div>
  );
};

export default NewTestForm;
