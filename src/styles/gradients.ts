import { styled } from '@mui/material/styles';
import { Card, Paper, Chip } from '@mui/material';

// Client app gradients to match manager app
export const clientGradients = {
  primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  secondary: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  warning: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
  card: 'linear-gradient(135deg, #ffffff 0%, #f8faff 100%)',
  header: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  success: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  info: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
};

// Styled components for enhanced design
export const StatsCard = styled(Card)(({ theme }) => ({
  background: clientGradients.card,
  borderRadius: 16,
  transition: 'all 0.3s ease-in-out',
  border: '1px solid rgba(102, 126, 234, 0.1)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 40px rgba(102, 126, 234, 0.15)',
  },
}));

export const EnhancedPaper = styled(Paper)(({ theme }) => ({
  borderRadius: 16,
  background: clientGradients.card,
  border: '1px solid rgba(102, 126, 234, 0.08)',
}));

export const GradientChip = styled(Chip)(({ theme }) => ({
  borderRadius: 8,
  fontWeight: 500,
  '&.MuiChip-colorPrimary': {
    background: clientGradients.primary,
  },
  '&.MuiChip-colorSecondary': {
    background: clientGradients.secondary,
  },
  '&.MuiChip-colorWarning': {
    background: clientGradients.warning,
  },
  '&.MuiChip-colorSuccess': {
    background: clientGradients.success,
  },
  '&.MuiChip-colorInfo': {
    background: clientGradients.info,
  },
})); 