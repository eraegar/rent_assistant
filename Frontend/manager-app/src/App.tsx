import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { managerTheme } from './theme';
import LoginScreen from './components/LoginScreen';
import Dashboard from './components/Dashboard';
import { useManagerStore } from './stores/useManagerStore';

const AuthWrapper: React.FC = () => {
  const { isAuthenticated, loading, refreshProfile } = useManagerStore();

  useEffect(() => {
    const token = localStorage.getItem('manager_token');
    if (token) {
      refreshProfile();
    }
  }, [refreshProfile]);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        Загрузка...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginScreen />;
  }

  return <Dashboard />;
};

const App: React.FC = () => (
  <ThemeProvider theme={managerTheme}>
    <CssBaseline />
    <Router>
      <Routes>
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/" element={<AuthWrapper />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  </ThemeProvider>
);

export default App; 