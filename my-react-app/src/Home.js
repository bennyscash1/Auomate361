import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/get">GET Page</Link></li>
        <li><Link to="/post">POST Page</Link></li>
      </ul>
    </nav>
    <div>
    <h1>Welcome to the Home Page!</h1>
    <p>This is the home page content.</p>
  </div>
  </div>
  );
};

export default Home;
