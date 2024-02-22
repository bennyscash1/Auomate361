// api.js
import axios from 'axios';

export const executeTest = async (testId) => {
  try {
    const response = await axios.post(`http://localhost:5000/tests/${testId}/execute`);
    return JSON.stringify(response.data);
  } catch (error) {
    console.error('Error executing test:', error);
    throw error;
  }
};

export const deleteTest = async (testId) => {
    try {
      const response = await axios.post(`http://localhost:5000/tests/${testId}/delete`);
      return JSON.stringify(response.data);
    } catch (error) {
      console.error('Error executing test:', error);
      throw error;
    }
  };
  