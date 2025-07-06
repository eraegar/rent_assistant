import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  CardContent,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  AppBar,
  Toolbar,
  Badge,
  Avatar,
  Menu,
  MenuItem,
  Alert,
  LinearProgress,
  styled,
} from '@mui/material';
import {
  Add,
  Visibility,
  NotificationsNone,
  AccountCircle,
  ExitToApp,
  Task,
  Assignment,
  CheckCircle,
  Schedule,
  RateReview,
  Edit,
  Star,
} from '@mui/icons-material';
import { useAuthStore } from '../stores/useAuthStore';
import { useTaskStore } from '../stores/useTaskStore';
import { Task as TaskType, TaskStatus } from '../types';
import ProfileModal from './ProfileModal';
import NewTaskModal from './NewTaskModal';
import TaskReviewModal from './TaskReviewModal';
import { StatsCard, EnhancedPaper, GradientChip, clientGradients } from '../styles/gradients';
import { apiService } from '../services/api';

const DashboardScreen: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { tasks, fetchTasks, createTask } = useTaskStore();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showNewTaskDialog, setShowNewTaskDialog] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [showTaskDetailDialog, setShowTaskDetailDialog] = useState(false);
  const [showTaskReviewModal, setShowTaskReviewModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState<TaskType | null>(null);
  const [taskTypePermissions, setTaskTypePermissions] = useState({
    allowed_types: ['personal', 'business'],
    plan_type: 'full',
    subscription_plan: 'full',
    can_choose_type: true,
    message: 'loading'
  });

  useEffect(() => {
    fetchTasks();
    loadTaskTypePermissions();
  }, [fetchTasks]);

  const loadTaskTypePermissions = async () => {
    try {
      const response = await apiService.getTaskTypePermissions();
      if (response.success && response.data) {
        setTaskTypePermissions(response.data);
      }
    } catch (error) {
      console.error('Failed to load task type permissions:', error);
    }
  };

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleOpenProfile = () => {
    setShowProfileModal(true);
    handleProfileMenuClose();
  };

  const handleLogout = () => {
    logout();
    handleProfileMenuClose();
  };

  const handleCreateTask = async (taskData: {
    title: string;
    description: string;
    task_type: 'personal' | 'business';
    deadline_hours: number;
  }) => {
    try {
      await createTask(taskData.title, taskData.description, taskData.task_type as any);
      setShowNewTaskDialog(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleViewTask = (task: TaskType) => {
    setSelectedTask(task);
    setShowTaskDetailDialog(true);
  };

  const handleReviewTask = (task: TaskType) => {
    setSelectedTask(task);
    setShowTaskReviewModal(true);
  };

  const handleTaskUpdated = () => {
    fetchTasks(); // Refresh tasks after approval/revision
  };

  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING: return 'warning';
      case TaskStatus.IN_PROGRESS: return 'info';
      case TaskStatus.COMPLETED: return 'success';
      case TaskStatus.APPROVED: return 'success';
      case TaskStatus.REVISION_REQUESTED: return 'warning';
      case TaskStatus.CANCELLED: return 'error';
      case TaskStatus.REJECTED: return 'error';
      default: return 'default';
    }
  };

  const getStatusText = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING: return 'Ожидает';
      case TaskStatus.IN_PROGRESS: return 'В работе';
      case TaskStatus.COMPLETED: return 'Выполнена';
      case TaskStatus.APPROVED: return 'Принята';
      case TaskStatus.REVISION_REQUESTED: return 'На доработке';
      case TaskStatus.CANCELLED: return 'Отменена';
      case TaskStatus.REJECTED: return 'Отклонена';
      default: return 'Неизвестно';
    }
  };

  const getStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING: return <Schedule />;
      case TaskStatus.IN_PROGRESS: return <Assignment />;
      case TaskStatus.COMPLETED: return <CheckCircle />;
      case TaskStatus.APPROVED: return <Star />;
      case TaskStatus.REVISION_REQUESTED: return <Edit />;
      default: return <Task />;
    }
  };

  const canReviewTask = (task: TaskType) => {
    return task.status === TaskStatus.COMPLETED;
  };

  const activeTasks = tasks.filter((task: TaskType) => 
    task.status === TaskStatus.PENDING || 
    task.status === TaskStatus.IN_PROGRESS ||
    task.status === TaskStatus.REVISION_REQUESTED
  );
  
  const completedTasks = tasks.filter((task: TaskType) => 
    task.status === TaskStatus.COMPLETED
  );

  const approvedTasks = tasks.filter((task: TaskType) => 
    task.status === TaskStatus.APPROVED
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* App Bar */}
      <AppBar position="static" sx={{ background: clientGradients.header }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'white', fontWeight: 600 }}>
            🎯 Ассистент в Аренду
          </Typography>
          
          <IconButton color="inherit" sx={{ mr: 2 }}>
            <Badge badgeContent={completedTasks.length} color="error">
              <NotificationsNone />
            </Badge>
          </IconButton>
          
          <IconButton
            color="inherit"
            onClick={handleProfileMenuOpen}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {user?.email?.charAt(0).toUpperCase()}
            </Avatar>
          </IconButton>
          
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleProfileMenuClose}
          >
            <MenuItem onClick={handleOpenProfile}>
              <AccountCircle sx={{ mr: 1 }} />
              Профиль
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <ExitToApp sx={{ mr: 1 }} />
              Выйти
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Welcome Section */}
        <Box mb={4} sx={{ textAlign: 'center' }}>
          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            Добро пожаловать, {user?.email?.split('@')[0]}! 👋
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Управляйте своими задачами и отслеживайте их выполнение
          </Typography>
        </Box>

        {/* Alert for completed tasks */}
        {completedTasks.length > 0 && (
          <Alert severity="success" sx={{ mb: 3 }}>
            У вас {completedTasks.length} выполненных задач ожидающих принятия! 
            Пожалуйста, оцените работу ассистентов.
          </Alert>
        )}

        {/* Stats Cards */}
        <Grid container spacing={3} mb={4}>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <Task sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {tasks.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      Всего задач
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </StatsCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <Assignment sx={{ fontSize: 40, color: 'warning.main', mr: 2 }} />
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {activeTasks.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      Активных задач
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </StatsCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <CheckCircle sx={{ fontSize: 40, color: 'success.main', mr: 2 }} />
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {completedTasks.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      Ожидают принятия
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </StatsCard>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard>
              <CardContent>
                <Box display="flex" alignItems="center">
                  <Star sx={{ fontSize: 40, color: 'info.main', mr: 2 }} />
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {approvedTasks.length}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      Принято
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </StatsCard>
          </Grid>
        </Grid>

        {/* Main Content */}
        <Grid container spacing={3}>
          {/* Recent Tasks */}
          <Grid item xs={12} md={8}>
            <EnhancedPaper sx={{ p: 3 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" fontWeight="bold">
                  Последние задачи
                </Typography>
              </Box>
              
              {isLoading ? (
                <LinearProgress />
              ) : tasks.length === 0 ? (
                <Alert severity="info">
                  Задач пока нет. Нажмите кнопку + чтобы создать первую задачу!
                </Alert>
              ) : (
                <List>
                  {tasks.slice(0, 5).map((task: TaskType) => (
                    <ListItem key={task.id} divider>
                      <ListItemText
                        primary={task.title}
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {task.description}
                            </Typography>
                            {task.client_rating && (
                              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                                <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
                                  Оценка:
                                </Typography>
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                  {[1, 2, 3, 4, 5].map((star) => (
                                    <Star 
                                      key={star}
                                      sx={{ 
                                        fontSize: 16, 
                                        color: star <= (task.client_rating || 0) ? 'warning.main' : 'grey.300' 
                                      }} 
                                    />
                                  ))}
                                  <Typography variant="caption" sx={{ ml: 1 }}>
                                    ({task.client_rating}/5)
                                  </Typography>
                                </Box>
                              </Box>
                            )}
                          </Box>
                        }
                      />
                      <Box sx={{ mr: 2 }}>
                        <GradientChip
                          label={getStatusText(task.status)}
                          color={getStatusColor(task.status) as any}
                          size="small"
                          icon={getStatusIcon(task.status)}
                        />
                      </Box>
                      <ListItemSecondaryAction>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <IconButton
                            edge="end"
                            onClick={() => handleViewTask(task)}
                            color="primary"
                          >
                            <Visibility />
                          </IconButton>
                          
                          {canReviewTask(task) && (
                            <IconButton
                              edge="end"
                              onClick={() => handleReviewTask(task)}
                              color="success"
                              sx={{
                                animation: 'pulse 2s infinite',
                                '@keyframes pulse': {
                                  '0%': { transform: 'scale(1)' },
                                  '50%': { transform: 'scale(1.1)' },
                                  '100%': { transform: 'scale(1)' }
                                }
                              }}
                            >
                              <RateReview />
                            </IconButton>
                          )}
                        </Box>
                      </ListItemSecondaryAction>
                    </ListItem>
                  ))}
                </List>
              )}
            </EnhancedPaper>
          </Grid>

          {/* Quick Actions */}
          <Grid item xs={12} md={4}>
            <EnhancedPaper sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Быстрые действия
              </Typography>
              
              <Box display="flex" flexDirection="column" gap={2}>
                <Button
                  variant="contained"
                  startIcon={<Add />}
                  fullWidth
                  onClick={() => setShowNewTaskDialog(true)}
                  sx={{ 
                    background: clientGradients.primary,
                    '&:hover': {
                      background: clientGradients.primary,
                      transform: 'translateY(-1px)',
                      boxShadow: '0 6px 20px rgba(102, 126, 234, 0.3)',
                    }
                  }}
                >
                  Создать новую задачу
                </Button>
                
                {completedTasks.length > 0 && (
                  <Button
                    variant="outlined"
                    startIcon={<RateReview />}
                    fullWidth
                    color="success"
                    onClick={() => {
                      const firstCompletedTask = completedTasks[0];
                      handleReviewTask(firstCompletedTask);
                    }}
                    sx={{
                      borderWidth: 2,
                      '&:hover': {
                        borderWidth: 2,
                        transform: 'translateY(-1px)',
                      }
                    }}
                  >
                    Принять работу ({completedTasks.length})
                  </Button>
                )}
                
                <Button
                  variant="outlined"
                  startIcon={<Task />}
                  fullWidth
                  sx={{
                    borderWidth: 2,
                    '&:hover': {
                      borderWidth: 2,
                      transform: 'translateY(-1px)',
                    }
                  }}
                >
                  Посмотреть все задачи
                </Button>
              </Box>
            </EnhancedPaper>
          </Grid>
        </Grid>
      </Container>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="добавить"
        sx={{ 
          position: 'fixed', 
          bottom: 16, 
          right: 16,
          background: clientGradients.primary,
          '&:hover': {
            background: clientGradients.primary,
            transform: 'scale(1.1)',
          }
        }}
        onClick={() => setShowNewTaskDialog(true)}
      >
        <Add />
      </Fab>

      {/* New Task Dialog */}
      <NewTaskModal
        open={showNewTaskDialog}
        onClose={() => setShowNewTaskDialog(false)}
        onSubmit={handleCreateTask}
        isLoading={isLoading}
        allowedTaskTypes={taskTypePermissions.allowed_types}
        planType={taskTypePermissions.plan_type}
        canChooseType={taskTypePermissions.can_choose_type}
      />

      {/* Task Review Modal */}
      <TaskReviewModal
        open={showTaskReviewModal}
        onClose={() => setShowTaskReviewModal(false)}
        task={selectedTask}
        onTaskUpdated={handleTaskUpdated}
      />

      {/* Task Detail Dialog */}
      <Dialog open={showTaskDetailDialog} onClose={() => setShowTaskDetailDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Детали задачи</DialogTitle>
        <DialogContent>
          {selectedTask && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {selectedTask.title}
              </Typography>
              <Typography variant="body1" paragraph>
                {selectedTask.description}
              </Typography>
              <Box display="flex" gap={2} mb={2}>
                <GradientChip
                  label={getStatusText(selectedTask.status)}
                  color={getStatusColor(selectedTask.status) as any}
                  icon={getStatusIcon(selectedTask.status)}
                />
                <GradientChip 
                  label={selectedTask.task_type === 'personal' ? 'Личная' : 'Бизнес'} 
                  color="secondary"
                  variant="outlined" 
                />
              </Box>

              {selectedTask.result && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                    Результат работы:
                  </Typography>
                  <Typography variant="body2" sx={{ 
                    bgcolor: 'grey.50', 
                    p: 2, 
                    borderRadius: 1, 
                    border: '1px solid',
                    borderColor: 'grey.300'
                  }}>
                    {selectedTask.result}
                  </Typography>
                </Box>
              )}

              {selectedTask.completion_notes && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                    Комментарии ассистента:
                  </Typography>
                  <Typography variant="body2" sx={{ 
                    bgcolor: 'grey.50', 
                    p: 2, 
                    borderRadius: 1, 
                    border: '1px solid',
                    borderColor: 'grey.300'
                  }}>
                    {selectedTask.completion_notes}
                  </Typography>
                </Box>
              )}

              {selectedTask.client_rating && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                    Ваша оценка:
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star 
                        key={star}
                        sx={{ 
                          fontSize: 20, 
                          color: star <= (selectedTask.client_rating || 0) ? 'warning.main' : 'grey.300' 
                        }} 
                      />
                    ))}
                    <Typography variant="body2" sx={{ ml: 1 }}>
                      ({selectedTask.client_rating}/5)
                    </Typography>
                  </Box>
                  {selectedTask.client_feedback && (
                    <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
                      "{selectedTask.client_feedback}"
                    </Typography>
                  )}
                </Box>
              )}

              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Создано: {new Date(selectedTask.created_at).toLocaleString('ru-RU')}
              </Typography>
              {selectedTask.updated_at && (
                <Typography variant="body2" color="text.secondary">
                  Обновлено: {new Date(selectedTask.updated_at).toLocaleString('ru-RU')}
                </Typography>
              )}
              {selectedTask.completed_at && (
                <Typography variant="body2" color="text.secondary">
                  Выполнено: {new Date(selectedTask.completed_at).toLocaleString('ru-RU')}
                </Typography>
              )}
              {selectedTask.approved_at && (
                <Typography variant="body2" color="text.secondary">
                  Принято: {new Date(selectedTask.approved_at).toLocaleString('ru-RU')}
                </Typography>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          {selectedTask && canReviewTask(selectedTask) && (
            <Button 
              onClick={() => {
                setShowTaskDetailDialog(false);
                handleReviewTask(selectedTask);
              }}
              variant="contained"
              color="success"
              startIcon={<RateReview />}
            >
              Принять или отправить на доработку
            </Button>
          )}
          <Button onClick={() => setShowTaskDetailDialog(false)}>Закрыть</Button>
        </DialogActions>
      </Dialog>

      {/* Profile Modal */}
      <ProfileModal
        open={showProfileModal}
        onClose={() => setShowProfileModal(false)}
      />
    </Box>
  );
};

export default DashboardScreen; 