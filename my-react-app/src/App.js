// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import NewTestForm from './Api/GetTest';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element ={<Home />} />
          <Route path="/new-test" element ={<NewTestForm />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
