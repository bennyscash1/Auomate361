// Home.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { executeTest, deleteTest } from './api';
import './App.css'; // Import the CSS file

const Home = () => {
  const [tests, setTests] = useState([]);
  const [count, setCount] = useState([]);

  useEffect(() => {
    fetchTests();
  }, [count]);

  const fetchTests = async () => {
    try {
      const response = await axios.get('http://localhost:5000/tests');
      setTests(response.data);
    } catch (error) {
      console.error('Error fetching tests:', error);
    }
  };

  const handleDelete = (testId) => {
    deleteTest(testId)
    setCount(prevCount => prevCount + 1);
  };
  const handleViewErrorDetails = (errorDetails) => {
    alert(errorDetails); // For simplicity, display error details in an alert
  };
  const handleExecuteTest = async (testId) => {
    try {
      const result = await executeTest(testId);
      // Update the test object with the result
      setTests(prevTests => prevTests.map(prevTest => {
        if (prevTest.id === testId) {
          return { ...prevTest, result: 'success' };
        }
        return prevTest;
      }));
    } catch (error) {
      console.error('Error executing test:', error);
      // Update the test object with the error and error message
      const errorMessage = error.response.data.error;
      console.log('Error details:', errorMessage);
      setTests(prevTests => prevTests.map(prevTest => {
        if (prevTest.id === testId) {
          return { ...prevTest, result: 'error', errorDetails: errorMessage };
        }
        return prevTest;
      }));
    }
  };
  return (
    <div>
      <h1>Test Management</h1>
      <button onClick={() => window.location.href='/new-test'}>Create New Test</button>
      <table>
        <thead>
          <tr>
            <th>Test Name</th>
            <th>Test Type</th>
            <th>Endpoind</th>
            <th>Expected Status</th>
            <th>Expected Data</th>
            <th>Data to Send</th>
            <th>Action</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {tests.map(test => (
            <tr key={test.id}>
              <td>{test.name}</td>
              <td>{test.type}</td>
              <td>{test.endpoint}</td>
              <td>{test.expectedStatus}</td>
              <td>{JSON.stringify(test.expectedData)}</td>
              <td>{test.type === 'POST' ? JSON.stringify(test.dataToSend) : 'N/A'}</td>
              <td><button onClick={async () => {
                  const result = await handleExecuteTest(test.id);
                  // Update the test object with the result
                }}>Execute</button></td>
                <td>
                {test.result === 'success' && <span style={{ color: 'green' }}>✓</span>}
                {test.result === 'error' && (
                <span style={{ color: 'red' }}>
                ✗{' '}
                <button onClick={() => handleViewErrorDetails(test.errorDetails)}>
                View Details
                </button>
                </span>
                )}
              </td>
              <td><button onClick={() => handleDelete(test.id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Home;
