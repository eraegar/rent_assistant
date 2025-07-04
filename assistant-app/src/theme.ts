import { createTheme } from '@mui/material/styles';

// Green color palette for assistants
const green = {
  50: '#e8f5e8',
  100: '#c8e6c8',
  200: '#a5d6a5',
  300: '#81c784',
  400: '#66bb6a',
  500: '#4caf50', // Main green
  600: '#43a047',
  700: '#388e3c',
  800: '#2e7d32', // Primary green
  900: '#1b5e20',
};

const secondary = {
  50: '#fff3e0',
  100: '#ffe0b2',
  200: '#ffcc80',
  300: '#ffb74d',
  400: '#ffa726',
  500: '#ff9800', // Orange
  600: '#fb8c00',
  700: '#f57c00',
  800: '#ef6c00',
  900: '#e65100',
};

const success = {
  50: '#e0f2f1',
  100: '#b2dfdb',
  200: '#80cbc4',
  300: '#4db6ac',
  400: '#26a69a',
  500: '#009688',
  600: '#00897b',
  700: '#00796b',
  800: '#00695c',
  900: '#004d40',
};

// Define gradients for assistant theme
export const assistantGradients = {
  primary: 'linear-gradient(135deg, #2e7d32 0%, #4caf50 50%, #66bb6a 100%)',
  secondary: 'linear-gradient(135deg, #ff9800 0%, #ffa726 50%, #ffb74d 100%)',
  success: 'linear-gradient(135deg, #009688 0%, #26a69a 50%, #4db6ac 100%)',
  background: 'linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 30%, #a5d6a5 100%)',
  card: 'linear-gradient(145deg, #ffffff 0%, #f8fff8 100%)',
  header: 'linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%)',
};

export const assistantTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: green[800], // #2e7d32
      light: green[400],
      dark: green[900],
      contrastText: '#ffffff',
      50: green[50],
      100: green[100],
      200: green[200],
      300: green[300],
      400: green[400],
      500: green[500],
      600: green[600],
      700: green[700],
      800: green[800],
      900: green[900],
    },
    secondary: {
      main: secondary[500], // #ff9800
      light: secondary[300],
      dark: secondary[700],
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
    success: {
      main: success[500], // #009688
      light: success[300],
      dark: success[700],
      contrastText: '#ffffff',
      50: success[50],
      100: success[100],
      200: success[200],
      300: success[300],
      400: success[400],
      500: success[500],
      600: success[600],
      700: success[700],
      800: success[800],
      900: success[900],
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
            boxShadow: '0 4px 12px rgba(46, 125, 50, 0.3)',
            transform: 'translateY(-1px)',
          },
          transition: 'all 0.2s ease-in-out',
        },
        contained: {
          background: assistantGradients.primary,
          '&:hover': {
            background: 'linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%)',
          },
        },
        outlined: {
          borderColor: green[300],
          color: green[800],
          '&:hover': {
            borderColor: green[500],
            backgroundColor: green[50],
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
          border: '1px solid rgba(46, 125, 50, 0.08)',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            boxShadow: '0 8px 40px rgba(46, 125, 50, 0.12)',
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
              borderColor: green[400],
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: green[600],
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
          background: assistantGradients.primary,
          color: 'white',
        },
        colorSecondary: {
          background: assistantGradients.secondary,
          color: 'white',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: assistantGradients.header,
          boxShadow: '0 4px 20px rgba(46, 125, 50, 0.3)',
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
          background: assistantGradients.primary,
          height: 3,
          borderRadius: 3,
        },
      },
    },
  },
});

export default assistantTheme; 