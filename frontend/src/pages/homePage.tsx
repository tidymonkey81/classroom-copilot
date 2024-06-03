import { Link } from 'react-router-dom';
import { Button, Container, Typography, TextField } from '@mui/material';
import { useAuth } from './services/userContext'; // Import useAuth
import React, { useState } from 'react';

export default function Home() {
  const { user, login, logout } = useAuth(); // Destructure the necessary methods and state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      alert("Login successful!");
    } catch (error) {
      alert("Failed to login: " + error.message);
    }
  };

  return (
    <Container style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
      <Typography variant="h2" component="div" gutterBottom>
        Classroom Copilot
      </Typography>
      <Typography variant="h6" component="div" gutterBottom>
        {user ? `Welcome, ${user.email}` : "Not logged in"}
      </Typography>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        {!user && (
          <>
            <TextField
              label="Email"
              variant="outlined"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ margin: '10px' }}
            />
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ margin: '10px' }}
            />
            <Button variant="contained" onClick={handleLogin} style={{ margin: '10px' }}>
              Login
            </Button>
          </>
        )}
        {user && (
          <Button variant="contained" onClick={logout} style={{ margin: '10px' }}>
            Logout
          </Button>
        )}
      </div>
    </Container>
  );
}