import './App.css'
import Container from '@material-ui/core/Container'
import AppBar from '@material-ui/core/AppBar'
import Typography from '@material-ui/core/Typography'
import Toolbar from '@material-ui/core/Toolbar'
import GoalsForAgainst from './components/GoalsForAgainst'

function App() {
  return (
    <Container fixed>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Hockey Nerds</Typography>
        </Toolbar>
      </AppBar>
      <GoalsForAgainst />
    </Container>
  )
}

export default App
