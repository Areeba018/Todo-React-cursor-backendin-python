import React, { useState } from 'react';
import { login as apiLogin } from './api';

function Login({ onLogin, switchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      // const res = await fetch('http://localhost:5000/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ username, password })
      // });
      // const data = await res.json();
      // if (!res.ok) throw new Error(data.message || 'Login failed');
      // localStorage.setItem('token', data.token);
      // onLogin(data.token, data.username);
      const data = await apiLogin(username, password);
    localStorage.setItem('token', data.token);
    onLogin(data.token, data.username);
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
        }}>Login</h2>
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
        <div style={{ position: 'relative', marginBottom: 0 }}>
          <input
            type={showPassword ? 'text' : 'password'}
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            style={{
              padding: '12px 44px 12px 14px',
              borderRadius: 8,
              border: '1.5px solid #b2ebf2',
              fontSize: '1.08em',
              background: '#f8f8f8',
              width: '100%',
              boxSizing: 'border-box',
              outline: 'none',
              transition: 'border 0.18s',
            }}
          />
          <span
            onClick={() => setShowPassword(v => !v)}
            style={{
              position: 'absolute',
              right: 16,
              top: '50%',
              transform: 'translateY(-50%)',
              cursor: 'pointer',
              fontSize: 20,
              color: '#00bcd4',
              userSelect: 'none',
              background: 'transparent',
              padding: 0,
              lineHeight: 1,
              display: 'flex',
              alignItems: 'center',
              height: 24,
              width: 24,
              justifyContent: 'center',
            }}
            title={showPassword ? 'Hide password' : 'Show password'}
            tabIndex={0}
            role="button"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17.94 17.94A10.06 10.06 0 0 1 12 20c-5.05 0-9.27-3.11-11-7.5a12.32 12.32 0 0 1 2.92-4.19M6.1 6.1A9.94 9.94 0 0 1 12 4c5.05 0 9.27 3.11 11 7.5a12.32 12.32 0 0 1-2.92 4.19M1 1l22 22" /></svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00bcd4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12S5 5 12 5s11 7 11 7-4 7-11 7S1 12 1 12z" /><circle cx="12" cy="12" r="3" /></svg>
            )}
          </span>
        </div>
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
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <div style={{
          textAlign: 'center',
          color: '#888',
          fontSize: '1em'
        }}>
          Don't have an account?{' '}
          <span
            onClick={switchToRegister}
            style={{
              color: '#00bcd4',
              cursor: 'pointer',
              fontWeight: 600,
              marginLeft: 4,
              textDecoration: 'underline'
            }}
          >Register</span>
        </div>
      </form>
    </div>
  );
}

export default Login; 