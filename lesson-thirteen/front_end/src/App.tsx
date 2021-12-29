import { ChainId, DAppProvider } from '@usedapp/core';
import { Header } from './components/Header';
import { Container, makeStyles } from '@material-ui/core';
import { Main } from './components/Main';
import './App.css';

function App() {
  return (
    <div className="App">
      <DAppProvider config={{
        supportedChains: [ChainId.Kovan, ChainId.Rinkeby],
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
