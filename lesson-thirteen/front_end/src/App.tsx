import { ChainId, DAppProvider, Rinkeby, Kovan } from '@usedapp/core';
import { Header } from './components/Header';
import { Container, FormControlLabel, makeStyles, Switch } from '@material-ui/core';
import { Main } from './components/Main';
import { Dispatch, SetStateAction } from 'react';
import { AppProps } from '.';

// function App({ changeTheme }: AppProps) {
const App: React.FC<AppProps<boolean>> = ({ theme }) => {
  return (
    // App css might not be necessary
    <div>
      <DAppProvider config={{
        networks: [Kovan],
      }}>
        <Header theme={theme} />
        <Container maxWidth="md">
          <Main />
        </Container>
      </DAppProvider>
    </div>
  );
}

export default App;
