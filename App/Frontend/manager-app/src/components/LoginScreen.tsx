import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Chip,
  Grid,
  Card,
  CardContent,
  Tab,
  Tabs,
  styled,
} from '@mui/material';
import { BusinessCenter as BusinessIcon } from '@mui/icons-material';
import { useManagerStore } from '../stores/useManagerStore';
import { managerGradients, managerTheme } from '../theme';
import { formatPhoneNumber, getCleanPhoneNumber, isValidPhoneNumber } from '../utils/phoneFormatter';

const GradientPaper = styled(Paper)(({ theme }) => ({
  background: managerGradients.header,
  color: 'white',
  padding: theme.spacing(6),
  marginBottom: theme.spacing(4),
  textAlign: 'center',
  borderRadius: 20,
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(255, 255, 255, 0.1)',
    backdropFilter: 'blur(10px)',
  },
  '& > *': {
    position: 'relative',
    zIndex: 1,
  },
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  transition: 'all 0.3s ease-in-out',
  background: managerGradients.card,
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 40px rgba(25, 118, 210, 0.15)',
  },
}));

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const LoginScreen: React.FC = () => {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const { login, loading } = useManagerStore();

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handlePhoneChange = (value: string) => {
    setPhone(formatPhoneNumber(value));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!phone || !password) {
      setError('Пожалуйста, заполните все поля');
      return;
    }

    if (!isValidPhoneNumber(phone)) {
      setError('Пожалуйста, введите корректный номер телефона');
      return;
    }

    const cleanPhone = getCleanPhoneNumber(phone);
    const success = await login(cleanPhone, password);
    if (!success) {
      setError('Неверный телефон или пароль');
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <GradientPaper elevation={0}>
        <Typography variant="h2" component="h1" gutterBottom align="center" sx={{ fontWeight: 700, color: 'white' }}>
          📊 Панель управления
        </Typography>
        <Typography variant="h5" align="center" sx={{ opacity: 0.9, fontWeight: 400, color: 'white' }}>
          Комплексная аналитика и управление бизнес-процессами
        </Typography>
      </GradientPaper>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <FeatureCard elevation={3} sx={{ height: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange} centered>
                <Tab label="Авторизация" />
                <Tab label="О системе" />
              </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}

              <form onSubmit={handleSubmit}>
                <TextField
                  fullWidth
                  label="Телефон"
                  value={phone}
                  onChange={(e) => handlePhoneChange(e.target.value)}
                  margin="normal"
                  type="tel"
                  autoComplete="tel"
                  placeholder="+7 (999) 123-45-67"
                  helperText={phone && !isValidPhoneNumber(phone) ? "Введите корректный номер телефона" : ""}
                  error={phone !== '' && !isValidPhoneNumber(phone)}
                />
                <TextField
                  fullWidth
                  label="Пароль"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  margin="normal"
                  autoComplete="current-password"
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="large"
                  sx={{ mt: 3, mb: 2 }}
                  disabled={loading || !phone || !password || !isValidPhoneNumber(phone)}
                >
                  {loading ? 'Вход...' : 'Войти в систему'}
                </Button>
              </form>

              <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
                <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                  💼 <strong>Доступ для менеджеров</strong> с корпоративными учетными записями.
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Обратитесь к администратору для получения учетных данных.
                </Typography>
              </Box>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <Box sx={{ textAlign: 'center' }}>
                <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom color="primary">
                  Управленческие инструменты
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Профессиональная платформа для управления командой ассистентов и анализа бизнес-показателей.
                </Typography>
                <Chip 
                  label="Менеджер" 
                  color="primary" 
                  sx={{ mt: 1 }} 
                />
              </Box>
            </TabPanel>
          </FeatureCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <FeatureCard>
                <CardContent sx={{ textAlign: 'center', p: 3 }}>
                  <Box
                    sx={{
                      width: 64,
                      height: 64,
                      borderRadius: 2,
                      background: managerTheme.palette.primary.main,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 16px',
                    }}
                  >
                    <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                      📊
                    </Typography>
                  </Box>
                  <Typography variant="h6" gutterBottom color="primary">
                    Аналитика
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Детальная статистика по задачам, ассистентам и клиентам
                  </Typography>
                </CardContent>
              </FeatureCard>
            </Grid>

            <Grid item xs={12}>
              <FeatureCard>
                <CardContent sx={{ textAlign: 'center', p: 3 }}>
                  <Box
                    sx={{
                      width: 64,
                      height: 64,
                      borderRadius: 2,
                      background: managerTheme.palette.secondary.main,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 16px',
                    }}
                  >
                    <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                      👥
                    </Typography>
                  </Box>
                  <Typography variant="h6" gutterBottom color="secondary">
                    Управление
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Контроль работы ассистентов и управление назначениями
                  </Typography>
                </CardContent>
              </FeatureCard>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LoginScreen; 