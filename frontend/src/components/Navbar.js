import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { usePageContext } from '../context';
import { useCallback } from 'react';

function Navbar() {
  const { setUrl, setIsUrlSubmitted } = usePageContext();

  const handleHomeClick = useCallback(() => {
    setUrl("");
    setIsUrlSubmitted(false);
  }, [setUrl, setIsUrlSubmitted]);
  
  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Parody Generator
        </Typography>
        <Button color="inherit" component={RouterLink} to="/" onClick={handleHomeClick}>Home</Button>
        <Button color="inherit" component={RouterLink} to="/library">Library</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;