import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import GetTest from './Api/GetTest';
import PostTest from './Api/PostTest';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/get" element={<GetTest />} />
          <Route path="/post" element={<PostTest />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;