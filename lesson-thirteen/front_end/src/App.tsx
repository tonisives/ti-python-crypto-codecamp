import { ChainId, DAppProvider, Rinkeby, Kovan } from '@usedapp/core';
import { Header } from './components/Header';
import { Container, makeStyles } from '@material-ui/core';
import { Main } from './components/Main';
import './App.css';

function App() {
  return (
    // App css might not be necessary
    <div className="App">
      <DAppProvider config={{
        networks: [Kovan],
      }}>
        <Header />
        <Container maxWidth="md">
          <Main />
        </Container>
      </DAppProvider>
    </div>
  );
}

export default App;
