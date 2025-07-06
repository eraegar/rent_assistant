import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  Alert,
  CircularProgress,
  styled,
  SelectChangeEvent,
} from '@mui/material';
import {
  Add,
  Business,
  Person,
  Description,
  Schedule,
} from '@mui/icons-material';
import { EnhancedPaper, GradientChip, clientGradients } from '../styles/gradients';

interface NewTaskModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (taskData: {
    title: string;
    description: string;
    task_type: 'personal' | 'business';
    deadline_hours: number;
  }) => void;
  isLoading?: boolean;
  allowedTaskTypes?: string[];
  planType?: string;
  canChooseType?: boolean;
}

interface TaskTypeCardProps {
  selected?: boolean;
  children: React.ReactNode;
  onClick: () => void;
  sx?: any;
}

const TaskTypeCard = styled(Box)<TaskTypeCardProps>(({ theme, selected }) => ({
  padding: theme.spacing(2),
  borderRadius: 12,
  border: `2px solid ${selected ? theme.palette.primary.main : 'rgba(102, 126, 234, 0.2)'}`,
  background: selected ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
  cursor: 'pointer',
  transition: 'all 0.2s ease-in-out',
  textAlign: 'center',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    background: 'rgba(102, 126, 234, 0.05)',
    transform: 'translateY(-1px)',
  },
}));

const NewTaskModal: React.FC<NewTaskModalProps> = ({ 
  open, 
  onClose, 
  onSubmit, 
  isLoading,
  allowedTaskTypes = ['personal', 'business'],
  planType = 'full',
  canChooseType = true
}) => {
  // Determine default task type based on allowed types
  const getDefaultTaskType = (): 'personal' | 'business' => {
    if (allowedTaskTypes.includes('personal')) return 'personal';
    if (allowedTaskTypes.includes('business')) return 'business';
    return 'personal';
  };

  const [taskData, setTaskData] = useState({
    title: '',
    description: '',
    task_type: getDefaultTaskType(),
    deadline_hours: 24,
  });
  const [error, setError] = useState<string | null>(null);

  // Reset task type when allowed types change
  React.useEffect(() => {
    setTaskData(prev => ({
      ...prev,
      task_type: getDefaultTaskType()
    }));
  }, [allowedTaskTypes]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!taskData.title.trim()) {
      setError('Введите название задачи');
      return;
    }

    if (!taskData.description.trim()) {
      setError('Введите описание задачи');
      return;
    }

    // Check if task type is allowed
    if (!allowedTaskTypes.includes(taskData.task_type)) {
      setError(`Ваш тариф не поддерживает ${taskData.task_type === 'business' ? 'бизнес' : 'личные'} задачи`);
      return;
    }

    onSubmit(taskData);
  };

  const handleClose = () => {
    setTaskData({
      title: '',
      description: '',
      task_type: getDefaultTaskType(),
      deadline_hours: 24,
    });
    setError(null);
    onClose();
  };

  const handleTaskTypeChange = (type: 'personal' | 'business') => {
    // Only allow change if type is in allowed types and user can choose
    if (allowedTaskTypes.includes(type) && canChooseType) {
      setTaskData({ ...taskData, task_type: type });
    }
  };

  const handleDeadlineChange = (event: SelectChangeEvent<number>) => {
    setTaskData({ ...taskData, deadline_hours: event.target.value as number });
  };

  // Get plan restriction message
  const getPlanMessage = () => {
    if (planType === 'personal') {
      return '📋 Ваш персональный тариф позволяет создавать только личные задачи';
    } else if (planType === 'business') {
      return '💼 Ваш бизнес тариф позволяет создавать только бизнес задачи';
    }
    return '';
  };

  const planMessage = getPlanMessage();

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Add sx={{ color: 'primary.main' }} />
          <Typography variant="h6" fontWeight="bold">
            Создать новую задачу
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent>
        <EnhancedPaper sx={{ p: 3, mt: 2 }}>
          <form onSubmit={handleSubmit}>
            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            {/* Task Title */}
            <TextField
              fullWidth
              label="Название задачи"
              variant="outlined"
              value={taskData.title}
              onChange={(e) => setTaskData({ ...taskData, title: e.target.value })}
              placeholder="Например: Найти и забронировать ресторан"
              sx={{ mb: 3 }}
              InputProps={{
                startAdornment: (
                  <Description sx={{ mr: 1, color: 'primary.main' }} />
                ),
              }}
            />

            {/* Task Description */}
            <TextField
              fullWidth
              label="Описание задачи"
              variant="outlined"
              multiline
              rows={4}
              value={taskData.description}
              onChange={(e) => setTaskData({ ...taskData, description: e.target.value })}
              placeholder="Опишите подробно, что нужно сделать..."
              sx={{ mb: 3 }}
            />

            {/* Task Type Selection */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight={600}>
                Тип задачи
              </Typography>
              
              {/* Plan restriction message */}
              {planMessage && (
                <Alert severity="info" sx={{ mb: 2 }}>
                  {planMessage}
                </Alert>
              )}
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TaskTypeCard
                  selected={taskData.task_type === 'personal'}
                  onClick={() => handleTaskTypeChange('personal')}
                  sx={{ 
                    flex: 1,
                    opacity: allowedTaskTypes.includes('personal') ? 1 : 0.5,
                    cursor: allowedTaskTypes.includes('personal') && canChooseType ? 'pointer' : 'not-allowed',
                    '&:hover': allowedTaskTypes.includes('personal') && canChooseType ? {
                      borderColor: 'primary.main',
                      background: 'rgba(102, 126, 234, 0.05)',
                      transform: 'translateY(-1px)',
                    } : {}
                  }}
                >
                  <Person sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                  <Typography variant="h6" fontWeight="bold" gutterBottom>
                    Личная
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Домашние дела, покупки, личные поручения
                  </Typography>
                  {taskData.task_type === 'personal' && (
                    <GradientChip
                      label="Выбрано"
                      size="small"
                      color="primary"
                      sx={{ mt: 1 }}
                    />
                  )}
                  {!allowedTaskTypes.includes('personal') && (
                    <GradientChip
                      label="Недоступно"
                      size="small"
                      color="default"
                      sx={{ mt: 1, opacity: 0.7 }}
                    />
                  )}
                </TaskTypeCard>

                <TaskTypeCard
                  selected={taskData.task_type === 'business'}
                  onClick={() => handleTaskTypeChange('business')}
                  sx={{ 
                    flex: 1,
                    opacity: allowedTaskTypes.includes('business') ? 1 : 0.5,
                    cursor: allowedTaskTypes.includes('business') && canChooseType ? 'pointer' : 'not-allowed',
                    '&:hover': allowedTaskTypes.includes('business') && canChooseType ? {
                      borderColor: 'primary.main',
                      background: 'rgba(102, 126, 234, 0.05)',
                      transform: 'translateY(-1px)',
                    } : {}
                  }}
                >
                  <Business sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                  <Typography variant="h6" fontWeight="bold" gutterBottom>
                    Бизнес
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Рабочие задачи, деловые встречи, документы
                  </Typography>
                  {taskData.task_type === 'business' && (
                    <GradientChip
                      label="Выбрано"
                      size="small"
                      color="primary"
                      sx={{ mt: 1 }}
                    />
                  )}
                  {!allowedTaskTypes.includes('business') && (
                    <GradientChip
                      label="Недоступно"
                      size="small"
                      color="default"
                      sx={{ mt: 1, opacity: 0.7 }}
                    />
                  )}
                </TaskTypeCard>
              </Box>
            </Box>

            {/* Deadline */}
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Желаемый срок выполнения</InputLabel>
              <Select
                value={taskData.deadline_hours}
                onChange={handleDeadlineChange}
                label="Желаемый срок выполнения"
                startAdornment={<Schedule sx={{ mr: 1, color: 'primary.main' }} />}
              >
                <MenuItem value={2}>2 часа</MenuItem>
                <MenuItem value={4}>4 часа</MenuItem>
                <MenuItem value={8}>8 часов</MenuItem>
                <MenuItem value={24}>24 часа</MenuItem>
                <MenuItem value={48}>2 дня</MenuItem>
                <MenuItem value={72}>3 дня</MenuItem>
              </Select>
            </FormControl>

            {/* Task Type Info */}
            <Box sx={{ 
              p: 2, 
              background: taskData.task_type === 'business' 
                ? 'rgba(102, 126, 234, 0.1)' 
                : 'rgba(76, 175, 80, 0.1)',
              borderRadius: 2,
              mb: 2
            }}>
              <Typography variant="body2" color="text.secondary">
                {taskData.task_type === 'business' 
                  ? '💼 Бизнес-задачи выполняются специализированными ассистентами с опытом работы в деловой сфере'
                  : '🏠 Личные задачи выполняются ассистентами, специализирующимися на домашних и персональных поручениях'
                }
              </Typography>
            </Box>
          </form>
        </EnhancedPaper>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button 
          onClick={handleClose}
          variant="outlined"
          disabled={isLoading}
        >
          Отмена
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={isLoading || !taskData.title.trim() || !taskData.description.trim()}
          startIcon={isLoading ? <CircularProgress size={20} /> : <Add />}
          sx={{
            background: clientGradients.primary,
            '&:hover': {
              background: clientGradients.primary,
              transform: 'translateY(-1px)',
              boxShadow: '0 6px 20px rgba(102, 126, 234, 0.3)',
            }
          }}
        >
          {isLoading ? 'Создание...' : 'Создать задачу'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewTaskModal; 