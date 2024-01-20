import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function Navbar() {
  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Parody Generator
        </Typography>
        <Button color="inherit" component={RouterLink} to="/">Home</Button>
        <Button color="inherit" component={RouterLink} to="/library">Library</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;