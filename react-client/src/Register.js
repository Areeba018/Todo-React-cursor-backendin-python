import React, { useState } from 'react';
import { register as apiRegister } from './api';


function Register({ onRegisterSuccess, switchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await apiRegister(username, email, password);
      onRegisterSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#e6efe6'
    }}>
      <form
        onSubmit={handleSubmit}
        style={{
          background: '#fff',
          borderRadius: 16,
          boxShadow: '0 4px 32px rgba(0,0,0,0.13)',
          padding: '36px 32px 28px 32px',
          minWidth: 340,
          display: 'flex',
          flexDirection: 'column',
          gap: 18,
          alignItems: 'stretch'
        }}
      >
        <h2 style={{
          margin: '0 0 8px 0',
          fontSize: '2rem',
          fontWeight: 700,
          color: '#00bcd4',
          textAlign: 'center'
        }}>Register</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
          style={{
            padding: '12px 14px',
            borderRadius: 8,
            border: '1.5px solid #b2ebf2',
            fontSize: '1.08em',
            background: '#f8f8f8',
            marginBottom: 0
          }}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          style={{
            padding: '12px 14px',
            borderRadius: 8,
            border: '1.5px solid #b2ebf2',
            fontSize: '1.08em',
            background: '#f8f8f8',
            marginBottom: 0
          }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{
            padding: '12px 14px',
            borderRadius: 8,
            border: '1.5px solid #b2ebf2',
            fontSize: '1.08em',
            background: '#f8f8f8',
            marginBottom: 0
          }}
        />
        {error && <div style={{
          color: '#ff5252',
          background: '#fff0f0',
          borderRadius: 6,
          padding: '8px 12px',
          fontSize: '1em',
          textAlign: 'center'
        }}>{error}</div>}
        <button
          type="submit"
          disabled={loading}
          style={{
            background: 'linear-gradient(90deg, #b2ebf2 60%, #00bcd4 100%)',
            color: '#222',
            fontWeight: 700,
            fontSize: '1.1em',
            border: 'none',
            borderRadius: 8,
            padding: '12px 0',
            marginTop: 8,
            cursor: 'pointer',
            transition: 'background 0.18s, color 0.18s'
          }}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
        <div style={{
          textAlign: 'center',
          color: '#888',
          fontSize: '1em'
        }}>
          Already have an account?{' '}
          <span
            onClick={switchToLogin}
            style={{
              color: '#00bcd4',
              cursor: 'pointer',
              fontWeight: 600,
              marginLeft: 4,
              textDecoration: 'underline'
            }}
          >Login</span>
        </div>
      </form>
    </div>
  );
}

export default Register; 