import React from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import PriceCalculator from './components/PriceCalculator';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <PriceCalculator />
      </Container>
    </ThemeProvider>
  );
}

export default App; 