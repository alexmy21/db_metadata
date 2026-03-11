import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, Container, Grid, CssBaseline } from '@mui/material';
import Header from './components/Header';
import DatabaseOverview from './components/DatabaseOverview';
import TableList from './components/TableList';
import TableDetails from './components/TableDetails';
import { useMetadata } from './hooks/useMetadata';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const { tables, loading, error } = useMetadata();
  const [selectedTable, setSelectedTable] = useState(null);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header />
        
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <DatabaseOverview />
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <TableList
                tables={tables}
                selectedTable={selectedTable}
                onSelectTable={setSelectedTable}
              />
            </Grid>
            
            <Grid item xs={12} md={8}>
              {selectedTable ? (
                <TableDetails tableName={selectedTable} />
              ) : (
                <Box
                  sx={{
                    height: '400px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: 'background.paper',
                    borderRadius: 1,
                  }}
                >
                  Select a table to view details
                </Box>
              )}
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
