import { Link } from 'react-router-dom';
import { Button, Box } from '@mui/material';

const MenuBar = () => {
  return (
    <Box display="flex" justifyContent="space-around" alignItems="center" height="50px" bgcolor="white" border={4} borderColor="black">
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/">
        HOME
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/admin">
        ADMIN
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/flow">
        FLOW
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/draw">
        DRAW
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/draw-file">
        DRAWFILE
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/slides">
        SLIDES
      </Button>
      <Button variant="contained" size="small" sx={{ fontSize: '10px' }} component={Link} to="/propagator">
        PROPAGATOR
      </Button>
    </Box>
  );
};

export default MenuBar;