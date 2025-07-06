import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  TextField,
  Box,
  Rating,
  Alert,
  Tab,
  Tabs,
  Chip,
  Paper,
  Divider,
  CircularProgress,
} from '@mui/material';
import {
  CheckCircle,
  Edit,
  Star,
  Warning,
  Info,
} from '@mui/icons-material';
import { Task, TaskApproval, TaskRevision } from '../types';
import { apiService } from '../services/api';

interface TaskReviewModalProps {
  open: boolean;
  onClose: () => void;
  task: Task | null;
  onTaskUpdated: () => void;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
};

const TaskReviewModal: React.FC<TaskReviewModalProps> = ({
  open,
  onClose,
  task,
  onTaskUpdated,
}) => {
  const [tabValue, setTabValue] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Approval state
  const [rating, setRating] = useState<number>(5);
  const [feedback, setFeedback] = useState('');

  // Revision state
  const [revisionFeedback, setRevisionFeedback] = useState('');
  const [additionalRequirements, setAdditionalRequirements] = useState('');

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setError(null);
    setSuccess(null);
  };

  const handleApproveTask = async () => {
    if (!task) return;
    
    if (!feedback.trim()) {
      setError('Пожалуйста, оставьте отзыв о работе');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const approval: TaskApproval = {
        rating,
        feedback: feedback.trim(),
      };

      const response = await apiService.approveTask(task.id, approval);
      
      if (response.success) {
        setSuccess('Работа принята! Спасибо за оценку.');
        onTaskUpdated();
        setTimeout(() => {
          onClose();
          resetForm();
        }, 2000);
      } else {
        setError(response.message || 'Ошибка при принятии работы');
      }
    } catch (error) {
      setError('Произошла ошибка при принятии работы');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRequestRevision = async () => {
    if (!task) return;
    
    if (!revisionFeedback.trim()) {
      setError('Пожалуйста, укажите что нужно исправить');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const revision: TaskRevision = {
        feedback: revisionFeedback.trim(),
        additional_requirements: additionalRequirements.trim() || undefined,
      };

      const response = await apiService.requestRevision(task.id, revision);
      
      if (response.success) {
        setSuccess('Задача отправлена на доработку. Ассистент получил ваши комментарии.');
        onTaskUpdated();
        setTimeout(() => {
          onClose();
          resetForm();
        }, 2000);
      } else {
        setError(response.message || 'Ошибка при отправке на доработку');
      }
    } catch (error) {
      setError('Произошла ошибка при отправке на доработку');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setTabValue(0);
    setRating(5);
    setFeedback('');
    setRevisionFeedback('');
    setAdditionalRequirements('');
    setError(null);
    setSuccess(null);
  };

  const handleClose = () => {
    onClose();
    resetForm();
  };

  if (!task) return null;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CheckCircle color="primary" />
          <Typography variant="h6" fontWeight="bold">
            Принять работу или отправить на доработку
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent>
        {/* Task Info */}
        <Paper sx={{ p: 2, mb: 3, bgcolor: 'grey.50' }}>
          <Typography variant="h6" gutterBottom fontWeight="bold">
            {task.title}
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {task.description}
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
            <Chip 
              label={task.task_type === 'personal' ? 'Личная' : 'Бизнес'} 
              color="primary" 
              size="small" 
            />
            <Chip 
              label="Выполнена" 
              color="success" 
              size="small" 
              icon={<CheckCircle />}
            />
          </Box>

          {task.result && (
            <Box>
              <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                Результат работы:
              </Typography>
              <Typography variant="body2" sx={{ 
                bgcolor: 'white', 
                p: 2, 
                borderRadius: 1, 
                border: '1px solid',
                borderColor: 'grey.300'
              }}>
                {task.result}
              </Typography>
            </Box>
          )}

          {task.completion_notes && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                Комментарии ассистента:
              </Typography>
              <Typography variant="body2" sx={{ 
                bgcolor: 'white', 
                p: 2, 
                borderRadius: 1, 
                border: '1px solid',
                borderColor: 'grey.300'
              }}>
                {task.completion_notes}
              </Typography>
            </Box>
          )}
        </Paper>

        {/* Error/Success Messages */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        {/* Action Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab 
              icon={<CheckCircle />} 
              label="Принять работу" 
              sx={{ textTransform: 'none', fontWeight: 500 }}
            />
            <Tab 
              icon={<Edit />} 
              label="Отправить на доработку" 
              sx={{ textTransform: 'none', fontWeight: 500 }}
            />
          </Tabs>
        </Box>

        {/* Approve Tab */}
        <TabPanel value={tabValue} index={0}>
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Star color="warning" />
              Оценить работу
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography component="legend" gutterBottom>
                Оценка качества работы (1-5 звезд)
              </Typography>
              <Rating
                value={rating}
                onChange={(_, newValue) => setRating(newValue || 1)}
                size="large"
                sx={{ mb: 1 }}
              />
              <Typography variant="body2" color="text.secondary">
                {rating === 1 && 'Очень плохо'}
                {rating === 2 && 'Плохо'}
                {rating === 3 && 'Удовлетворительно'}
                {rating === 4 && 'Хорошо'}
                {rating === 5 && 'Отлично'}
              </Typography>
            </Box>

            <TextField
              label="Отзыв о работе"
              placeholder="Поделитесь впечатлениями о качестве выполненной работы..."
              multiline
              rows={4}
              fullWidth
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              required
              sx={{ mb: 2 }}
            />

            <Alert severity="info" icon={<Info />}>
              После принятия работы ассистент получит вашу оценку, что поможет ему улучшить качество услуг.
              {rating === 0 && ' Если ассистент не выполнил задачу, его оценка автоматически будет 0.'}
            </Alert>
          </Box>
        </TabPanel>

        {/* Revision Tab */}
        <TabPanel value={tabValue} index={1}>
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Edit color="warning" />
              Отправить на доработку
            </Typography>

            <Alert severity="warning" sx={{ mb: 2 }} icon={<Warning />}>
              Работа будет возвращена ассистенту для исправления. Укажите конкретно, что нужно изменить.
            </Alert>

            <TextField
              label="Что нужно исправить"
              placeholder="Опишите конкретно, что не устраивает в выполненной работе..."
              multiline
              rows={4}
              fullWidth
              value={revisionFeedback}
              onChange={(e) => setRevisionFeedback(e.target.value)}
              required
              sx={{ mb: 2 }}
            />

            <TextField
              label="Дополнительные требования (опционально)"
              placeholder="Укажите дополнительные требования, если они появились..."
              multiline
              rows={3}
              fullWidth
              value={additionalRequirements}
              onChange={(e) => setAdditionalRequirements(e.target.value)}
              sx={{ mb: 2 }}
            />

            <Alert severity="info" icon={<Info />}>
              Ассистент получит ваши комментарии и сможет доработать задачу. После доработки вы снова сможете принять или отправить работу на доработку.
            </Alert>
          </Box>
        </TabPanel>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={handleClose} disabled={isLoading}>
          Отмена
        </Button>
        
        {tabValue === 0 ? (
          <Button
            variant="contained"
            color="success"
            onClick={handleApproveTask}
            disabled={isLoading || !feedback.trim()}
            startIcon={isLoading ? <CircularProgress size={20} /> : <CheckCircle />}
            sx={{ ml: 1 }}
          >
            {isLoading ? 'Принимаем...' : 'Принять работу'}
          </Button>
        ) : (
          <Button
            variant="contained"
            color="warning"
            onClick={handleRequestRevision}
            disabled={isLoading || !revisionFeedback.trim()}
            startIcon={isLoading ? <CircularProgress size={20} /> : <Edit />}
            sx={{ ml: 1 }}
          >
            {isLoading ? 'Отправляем...' : 'Отправить на доработку'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default TaskReviewModal; 