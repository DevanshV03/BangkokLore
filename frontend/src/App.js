import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing/Landing';
import Feed from './pages/Feed/Feed';
import './styles/globals.css';
import Submit from './pages/Submit/Submit';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path='/feed' element={<Feed/>}/>
          <Route path="/submit" element={<Submit />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
