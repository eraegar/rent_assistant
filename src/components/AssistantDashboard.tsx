import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  Chip,
  List,
  ListItem,
  ListItemText,
  Switch,
  FormControlLabel,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import { 
  Dashboard as DashboardIcon,
  Assignment as TaskIcon,
  Store as MarketplaceIcon,
  TrendingUp as StatsIcon,
  CheckCircle as CompleteIcon,
  Work as WorkIcon
} from '@mui/icons-material';

interface AssistantStats {
  total_tasks: number;
  active_tasks: number;
  completed_tasks: number;
  average_rating: number;
  available_marketplace_tasks: number;
  status: string;
  specialization: string;
}

interface MarketplaceTask {
  id: number;
  title: string;
  description: string;
  type: string;
  client_name: string;
  created_at: string;
  deadline?: string;
  time_remaining: string;
}

interface AssignedTask {
  id: number;
  title: string;
  description: string;
  type: string;
  status: string;
  created_at: string;
  deadline?: string;
  claimed_at?: string;
  result?: string;
  completion_notes?: string;
  client_rating?: number;
  client_feedback?: string;
}

const AssistantDashboard: React.FC = () => {
  const [stats, setStats] = useState<AssistantStats | null>(null);
  const [marketplaceTasks, setMarketplaceTasks] = useState<MarketplaceTask[]>([]);
  const [assignedTasks, setAssignedTasks] = useState<AssignedTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isOnline, setIsOnline] = useState(false);
  const [selectedTask, setSelectedTask] = useState<MarketplaceTask | null>(null);
  const [completeDialogOpen, setCompleteDialogOpen] = useState(false);
  const [completingTask, setCompletingTask] = useState<AssignedTask | null>(null);
  const [completionSummary, setCompletionSummary] = useState('');
  const [detailedResult, setDetailedResult] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Нет токена авторизации');
        return;
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Load stats
      const statsResponse = await fetch('/api/v1/assistants/dashboard/stats', { headers });
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
        setIsOnline(statsData.status === 'online');
      }

      // Load marketplace tasks
      const marketplaceResponse = await fetch('/api/v1/assistants/tasks/marketplace', { headers });
      if (marketplaceResponse.ok) {
        const marketplaceData = await marketplaceResponse.json();
        setMarketplaceTasks(marketplaceData);
      }

      // Load assigned tasks
      const assignedResponse = await fetch('/api/v1/assistants/tasks/assigned', { headers });
      if (assignedResponse.ok) {
        const assignedData = await assignedResponse.json();
        setAssignedTasks(assignedData);
      }

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusToggle = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const newStatus = !isOnline ? 'online' : 'offline';
      
      const response = await fetch('/api/v1/assistants/profile/status', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
      });

      if (response.ok) {
        setIsOnline(!isOnline);
        if (stats) {
          setStats({ ...stats, status: newStatus });
        }
      } else {
        setError('Ошибка изменения статуса');
      }
    } catch (error) {
      console.error('Ошибка изменения статуса:', error);
      setError('Ошибка изменения статуса');
    }
  };

  const handleClaimTask = async (taskId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      
      const response = await fetch(`/api/v1/assistants/tasks/${taskId}/claim`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        // Reload data after claiming task
        loadDashboardData();
        setSelectedTask(null);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка взятия задачи');
      }
    } catch (error) {
      console.error('Ошибка взятия задачи:', error);
      setError('Ошибка взятия задачи');
    }
  };

  const handleCompleteTask = async () => {
    if (!completingTask) return;

    try {
      const token = localStorage.getItem('access_token');
      
      const response = await fetch(`/api/v1/assistants/tasks/${completingTask.id}/complete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          completion_summary: completionSummary,
          detailed_result: detailedResult
        })
      });

      if (response.ok) {
        setCompleteDialogOpen(false);
        setCompletingTask(null);
        setCompletionSummary('');
        setDetailedResult('');
        loadDashboardData();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка завершения задачи');
      }
    } catch (error) {
      console.error('Ошибка завершения задачи:', error);
      setError('Ошибка завершения задачи');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'default';
      case 'in_progress': return 'primary';
      case 'completed': return 'success';
      case 'approved': return 'success';
      case 'cancelled': return 'error';
      default: return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending': return 'Ожидает';
      case 'in_progress': return 'В работе';
      case 'completed': return 'Завершена';
      case 'approved': return 'Одобрена';
      case 'cancelled': return 'Отменена';
      default: return status;
    }
  };

  const getTypeText = (type: string) => {
    switch (type) {
      case 'personal': return 'Личное';
      case 'business': return 'Бизнес';
      default: return type;
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Панель ассистента
        </Typography>
        <FormControlLabel
          control={
            <Switch
              checked={isOnline}
              onChange={handleStatusToggle}
              color="success"
            />
          }
          label={isOnline ? "В сети" : "Не в сети"}
        />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Stats Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <WorkIcon color="primary" sx={{ mr: 2 }} />
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Активные задачи
                    </Typography>
                    <Typography variant="h4">
                      {stats.active_tasks}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <CompleteIcon color="success" sx={{ mr: 2 }} />
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Завершено
                    </Typography>
                    <Typography variant="h4">
                      {stats.completed_tasks}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <StatsIcon color="warning" sx={{ mr: 2 }} />
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Рейтинг
                    </Typography>
                    <Typography variant="h4">
                      {stats.average_rating}/5
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <MarketplaceIcon color="info" sx={{ mr: 2 }} />
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      Доступно задач
                    </Typography>
                    <Typography variant="h4">
                      {stats.available_marketplace_tasks}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Grid container spacing={3}>
        {/* Marketplace Tasks */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <MarketplaceIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Биржа задач
            </Typography>
            {marketplaceTasks.length === 0 ? (
              <Typography color="textSecondary">
                Нет доступных задач
              </Typography>
            ) : (
              <List>
                {marketplaceTasks.slice(0, 5).map((task) => (
                  <ListItem 
                    key={task.id} 
                    sx={{ 
                      border: '1px solid #e0e0e0', 
                      borderRadius: 1, 
                      mb: 1,
                      '&:hover': { backgroundColor: '#f5f5f5', cursor: 'pointer' }
                    }}
                    onClick={() => setSelectedTask(task)}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="subtitle1">{task.title}</Typography>
                          <Chip 
                            label={getTypeText(task.type)} 
                            size="small" 
                            color={task.type === 'business' ? 'primary' : 'default'}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            Клиент: {task.client_name}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            {task.time_remaining}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>

        {/* Assigned Tasks */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <TaskIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Мои задачи
            </Typography>
            {assignedTasks.length === 0 ? (
              <Typography color="textSecondary">
                Нет назначенных задач
              </Typography>
            ) : (
              <List>
                {assignedTasks.slice(0, 5).map((task) => (
                  <ListItem 
                    key={task.id}
                    sx={{ 
                      border: '1px solid #e0e0e0', 
                      borderRadius: 1, 
                      mb: 1 
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="subtitle1">{task.title}</Typography>
                          <Box>
                            <Chip 
                              label={getStatusText(task.status)} 
                              size="small" 
                              color={getStatusColor(task.status)}
                              sx={{ mr: 1 }}
                            />
                            {task.status === 'in_progress' && (
                              <Button
                                size="small"
                                variant="outlined"
                                onClick={() => {
                                  setCompletingTask(task);
                                  setCompleteDialogOpen(true);
                                }}
                              >
                                Завершить
                              </Button>
                            )}
                          </Box>
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            Тип: {getTypeText(task.type)}
                          </Typography>
                          {task.client_rating && (
                            <Typography variant="body2" color="textSecondary">
                              Оценка: {task.client_rating}/5 ⭐
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Task Details Dialog */}
      <Dialog open={!!selectedTask} onClose={() => setSelectedTask(null)} maxWidth="md" fullWidth>
        {selectedTask && (
          <>
            <DialogTitle>{selectedTask.title}</DialogTitle>
            <DialogContent>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body1" gutterBottom>
                  <strong>Описание:</strong>
                </Typography>
                <Typography variant="body2" paragraph>
                  {selectedTask.description}
                </Typography>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Chip 
                  label={getTypeText(selectedTask.type)} 
                  color={selectedTask.type === 'business' ? 'primary' : 'default'}
                  sx={{ mr: 1 }}
                />
                <Chip 
                  label={`Клиент: ${selectedTask.client_name}`} 
                  variant="outlined"
                />
              </Box>

              <Typography variant="body2" color="textSecondary">
                <strong>Время до дедлайна:</strong> {selectedTask.time_remaining}
              </Typography>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setSelectedTask(null)}>
                Отмена
              </Button>
              <Button 
                variant="contained" 
                onClick={() => handleClaimTask(selectedTask.id)}
                disabled={!isOnline}
              >
                Взять задачу
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Complete Task Dialog */}
      <Dialog open={completeDialogOpen} onClose={() => setCompleteDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Завершить задачу</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Краткое описание выполненной работы"
            fullWidth
            variant="outlined"
            multiline
            rows={3}
            value={completionSummary}
            onChange={(e) => setCompletionSummary(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Подробный результат"
            fullWidth
            variant="outlined"
            multiline
            rows={6}
            value={detailedResult}
            onChange={(e) => setDetailedResult(e.target.value)}
            placeholder="Опишите подробно что было сделано, какие результаты получены..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCompleteDialogOpen(false)}>
            Отмена
          </Button>
          <Button 
            variant="contained" 
            onClick={handleCompleteTask}
            disabled={!completionSummary.trim() || !detailedResult.trim()}
          >
            Завершить задачу
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AssistantDashboard; 