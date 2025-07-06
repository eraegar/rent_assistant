import { createTheme } from '@mui/material/styles';

// Blue color palette for managers
const blue = {
  50: '#e3f2fd',
  100: '#bbdefb',
  200: '#90caf9',
  300: '#64b5f6',
  400: '#42a5f5',
  500: '#2196f3', // Main blue
  600: '#1e88e5',
  700: '#1976d2', // Primary blue
  800: '#1565c0',
  900: '#0d47a1',
};

const secondary = {
  50: '#fafafa',
  100: '#f5f5f5',
  200: '#eeeeee',
  300: '#e0e0e0',
  400: '#bdbdbd',
  500: '#9e9e9e', // Grey
  600: '#757575',
  700: '#616161',
  800: '#424242',
  900: '#212121',
};

const warning = {
  50: '#fff3e0',
  100: '#ffe0b2',
  200: '#ffcc80',
  300: '#ffb74d',
  400: '#ffa726',
  500: '#ff9800',
  600: '#fb8c00',
  700: '#f57c00', // Orange
  800: '#ef6c00',
  900: '#e65100',
};

// Define gradients for manager theme
export const managerGradients = {
  primary: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 50%, #64b5f6 100%)',
  secondary: 'linear-gradient(135deg, #757575 0%, #9e9e9e 50%, #bdbdbd 100%)',
  warning: 'linear-gradient(135deg, #f57c00 0%, #ff9800 50%, #ffa726 100%)',
  background: 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 30%, #90caf9 100%)',
  card: 'linear-gradient(145deg, #ffffff 0%, #f0f8ff 100%)',
  header: 'linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #1e88e5 100%)',
};

export const managerTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: blue[700], // #1976d2
      light: blue[400],
      dark: blue[900],
      contrastText: '#ffffff',
      50: blue[50],
      100: blue[100],
      200: blue[200],
      300: blue[300],
      400: blue[400],
      500: blue[500],
      600: blue[600],
      700: blue[700],
      800: blue[800],
      900: blue[900],
    },
    secondary: {
      main: secondary[600], // #757575
      light: secondary[300],
      dark: secondary[800],
      contrastText: '#ffffff',
      50: secondary[50],
      100: secondary[100],
      200: secondary[200],
      300: secondary[300],
      400: secondary[400],
      500: secondary[500],
      600: secondary[600],
      700: secondary[700],
      800: secondary[800],
      900: secondary[900],
    },
    warning: {
      main: warning[700], // #f57c00
      light: warning[300],
      dark: warning[900],
      contrastText: '#ffffff',
      50: warning[50],
      100: warning[100],
      200: warning[200],
      300: warning[300],
      400: warning[400],
      500: warning[500],
      600: warning[600],
      700: warning[700],
      800: warning[800],
      900: warning[900],
    },
    success: {
      main: '#388e3c',
      light: '#66bb6a',
      dark: '#2e7d32',
      contrastText: '#ffffff',
    },
    background: {
      default: '#fafafa',
      paper: '#ffffff',
    },
    text: {
      primary: '#1a1a1a',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: [
      'Inter',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  spacing: 8,
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
          padding: '10px 24px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)',
            transform: 'translateY(-1px)',
          },
          transition: 'all 0.2s ease-in-out',
        },
        contained: {
          background: managerGradients.primary,
          '&:hover': {
            background: 'linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #1e88e5 100%)',
          },
        },
        outlined: {
          borderColor: blue[300],
          color: blue[700],
          '&:hover': {
            borderColor: blue[500],
            backgroundColor: blue[50],
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
          border: '1px solid rgba(25, 118, 210, 0.08)',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            boxShadow: '0 8px 40px rgba(25, 118, 210, 0.12)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
        },
        elevation1: {
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        },
        elevation3: {
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.12)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: blue[400],
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: blue[600],
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          fontWeight: 500,
        },
        colorPrimary: {
          background: managerGradients.primary,
          color: 'white',
        },
        colorSecondary: {
          background: managerGradients.secondary,
          color: 'white',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: managerGradients.header,
          boxShadow: '0 4px 20px rgba(25, 118, 210, 0.3)',
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 16,
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        indicator: {
          background: managerGradients.primary,
          height: 3,
          borderRadius: 3,
        },
      },
    },
  },
});

export default managerTheme; 