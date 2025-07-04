import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Tab,
  Tabs,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  styled,
} from '@mui/material';
import {
  Phone,
  Lock,
  Person,
  Visibility,
  VisibilityOff,
  Login,
  PersonAdd,
} from '@mui/icons-material';
import { useAuthStore } from '../stores/useAuthStore';
import { EnhancedPaper, clientGradients } from '../styles/gradients';

// Styled components for enhanced design
const WelcomeContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  background: clientGradients.header,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(2),
}));

const AuthCard = styled(EnhancedPaper)(({ theme }) => ({
  padding: theme.spacing(4),
  maxWidth: 450,
  width: '100%',
  background: clientGradients.card,
  boxShadow: '0 25px 50px rgba(0, 0, 0, 0.25)',
}));

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
};

const WelcomeScreen: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loginData, setLoginData] = useState({ phone: '', password: '' });
  const [registerData, setRegisterData] = useState({ name: '', phone: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuthStore();

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setError(null);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const success = await login(loginData.phone, loginData.password);
      if (!success) {
        setError('Неверный телефон или пароль');
      }
    } catch (error) {
      setError('Произошла ошибка при входе');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const success = await register(registerData.name, registerData.phone, registerData.password);
      if (!success) {
        setError('Ошибка регистрации. Возможно, этот номер уже зарегистрирован');
      }
    } catch (error) {
      setError('Произошла ошибка при регистрации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <WelcomeContainer>
      <Container maxWidth="sm">
        <AuthCard>
          {/* Header */}
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="primary">
              🎯 Ассистент в Аренду
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Ваш персональный помощник для любых задач
            </Typography>
          </Box>

          {/* Tabs */}
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            centered
            indicatorColor="primary"
            textColor="primary"
            sx={{ mb: 2 }}
          >
            <Tab 
              label="Вход" 
              icon={<Login />} 
              iconPosition="start"
              sx={{ fontWeight: 600 }}
            />
            <Tab 
              label="Регистрация" 
              icon={<PersonAdd />} 
              iconPosition="start"
              sx={{ fontWeight: 600 }}
            />
          </Tabs>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Login Tab */}
          <TabPanel value={tabValue} index={0}>
            <Box component="form" onSubmit={handleLogin}>
              <TextField
                fullWidth
                label="Номер телефона"
                variant="outlined"
                margin="normal"
                value={loginData.phone}
                onChange={(e) => setLoginData({ ...loginData, phone: e.target.value })}
                placeholder="+7 (900) 123-45-67"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Phone color="primary" />
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Пароль"
                type={showPassword ? 'text' : 'password'}
                variant="outlined"
                margin="normal"
                value={loginData.password}
                onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock color="primary" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 3 }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading || !loginData.phone || !loginData.password}
                startIcon={loading ? <CircularProgress size={20} /> : <Login />}
                sx={{
                  py: 1.5,
                  background: clientGradients.primary,
                  '&:hover': {
                    background: clientGradients.primary,
                    transform: 'translateY(-1px)',
                    boxShadow: '0 6px 20px rgba(102, 126, 234, 0.3)',
                  }
                }}
              >
                {loading ? 'Вход...' : 'Войти'}
              </Button>
            </Box>
          </TabPanel>

          {/* Register Tab */}
          <TabPanel value={tabValue} index={1}>
            <Box component="form" onSubmit={handleRegister}>
              <TextField
                fullWidth
                label="Ваше имя"
                variant="outlined"
                margin="normal"
                value={registerData.name}
                onChange={(e) => setRegisterData({ ...registerData, name: e.target.value })}
                placeholder="Иван Иванов"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Person color="primary" />
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Номер телефона"
                variant="outlined"
                margin="normal"
                value={registerData.phone}
                onChange={(e) => setRegisterData({ ...registerData, phone: e.target.value })}
                placeholder="+7 (900) 123-45-67"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Phone color="primary" />
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Пароль"
                type={showPassword ? 'text' : 'password'}
                variant="outlined"
                margin="normal"
                value={registerData.password}
                onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock color="primary" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 3 }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading || !registerData.name || !registerData.phone || !registerData.password}
                startIcon={loading ? <CircularProgress size={20} /> : <PersonAdd />}
                sx={{
                  py: 1.5,
                  background: clientGradients.secondary,
                  '&:hover': {
                    background: clientGradients.secondary,
                    transform: 'translateY(-1px)',
                    boxShadow: '0 6px 20px rgba(240, 147, 251, 0.3)',
                  }
                }}
              >
                {loading ? 'Регистрация...' : 'Зарегистрироваться'}
              </Button>
            </Box>
          </TabPanel>

          {/* Footer */}
          <Box sx={{ textAlign: 'center', mt: 4, pt: 3, borderTop: '1px solid', borderColor: 'divider' }}>
            <Typography variant="body2" color="text.secondary">
              Присоединяйтесь к тысячам довольных клиентов
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Безопасно • Надежно • Профессионально
            </Typography>
          </Box>
        </AuthCard>
      </Container>
    </WelcomeContainer>
  );
};

export default WelcomeScreen; 