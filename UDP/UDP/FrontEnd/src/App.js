import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import { NavBar } from './components/NavBar';
import { Banner } from './components/Banner';
import { Projects } from './components/Projects';
import { Footer } from './components/Footer';
import Login from './components/Login';

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const toggleLoginModal = () => {
    setShowLogin(!showLogin);
  };
  const handleLogout = () => {
    localStorage.removeItem('token'); 
    window.location.reload();
  };

  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem('token'));
  }, []);

  return (
    <div className="App">
      {isLoggedIn && (
        <div>
          <NavBar />
          <Banner />
          <Projects />
          <Footer />
        </div>
      )} 
      <br/><br/>
      <div style={centeredContainerStyle}>
      <button onClick={toggleLoginModal} style={loginButtonStyle}>Login</button>
      <button style={{marginRight:"5px",marginLeft:"5px"}}></button>
      <button onClick={handleLogout} style={loginButtonStyle}>Logout</button>
      </div>
      {!isLoggedIn && showLogin && (
        <Login
          onClose={toggleLoginModal}
          onLogin={() => {
            setIsLoggedIn(true);
            toggleLoginModal();
          }}
        />
      )}
    </div>
  );
}
const loginButtonStyle = {
  backgroundColor: '#007BFF',
  color: 'white',
  padding: '10px 20px',
  borderRadius: '5px',
  cursor: 'pointer',
  
};
const centeredContainerStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  height: '0vh',
};

export default App;
