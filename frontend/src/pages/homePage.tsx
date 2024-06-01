import { Link } from 'react-router-dom';
import { Button, Container, Typography } from '@mui/material';

export default function Home() {
  return (
    <Container style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
      <Typography variant="h2" component="div" gutterBottom>
        Classroom Copilot
      </Typography>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <Button variant="contained" component={Link} to="/admin" style={{ margin: '10px' }}>
          Admin
        </Button>
        <Button variant="contained" component={Link} to="/flow" style={{ margin: '10px' }}>
          Flow
        </Button>
        <Button variant="contained" component={Link} to="/draw" style={{ margin: '10px' }}>
          Draw
        </Button>
      </div>
    </Container>
  );
}