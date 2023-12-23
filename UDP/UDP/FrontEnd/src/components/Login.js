import React, { useState } from 'react';
import 'animate.css';
import contactImg from "../assets/img/contact-img.svg";
import { Container, Row, Col } from "react-bootstrap";

const Login = ({ onClose, onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const token = "1!4@27*9#"; // The token for successful login

  const handleLogin = async () => {
    // ... your existing code for login

    if ((username === "admin" && password === "admin") || (username === "admin2" && password === "admin2")) {
      localStorage.setItem('token', token); // Set the token in localStorage
      setTimeout(() => {
        window.alert("Logged in Successfully");
        onLogin(); // Trigger the onLogin callback to update the App's state
      }, 5000); // Delay execution for 2 seconds (2000 milliseconds)
    } else {
      setTimeout(() => {
        window.alert("Invalid Credentials");
      }, 5000);
    }
  };

  const handleLogin1 = async () => {
    // Send a POST request to your Flask backend to authenticate the user
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: JSON.stringify({ username, password }),
    });
    
    if (response.status === 200) {
      const data = await response.json();
      localStorage.setItem('token', data.token);
      onLogin();
    } else {
      // Handle authentication failure here and provide user feedback
      console.error('Authentication failed');
    }
  };

  return (
    <div className="contact" id="connect">
      <Container>
        <Row className="align-items-center">
          <Col size={12} md={6}>
            <img className="animate__animated animate__zoomIn" src={contactImg} alt="Contact Us" />
          </Col>
          <Col size={12} md={6}>
            <div className="animate__animated animate__fadeIn">
              <h2>Login</h2>
              <input style={{borderRadius:"5px"}}
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input style={{borderRadius:"5px"}}
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button onClick={handleLogin} style={{borderRadius:"5px",backgroundColor:"lightBlue"}}>Login</button>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Login;
