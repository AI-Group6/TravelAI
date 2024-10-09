import logo from './logo.svg';
import './App.css';
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './Components/Home';


function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;