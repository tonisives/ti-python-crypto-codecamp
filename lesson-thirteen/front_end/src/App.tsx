import { ChainId, DAppProvider, Rinkeby, Kovan } from '@usedapp/core';
import { Header } from './components/Header';
import { Container, FormControlLabel, makeStyles, Switch } from '@material-ui/core';
import { Main } from './components/Main';
import { Dispatch, SetStateAction } from 'react';
import { AppProps } from '.';

const App: React.FC<AppProps<boolean>> = ({ theme }) => {
  return (
    // App css might not be necessary
    <div>
      <DAppProvider config={{
        networks: [Kovan],
        notifications: {
          // check the blockchain every 1s for our tx-s
          expirationPeriod: 1000,
          checkInterval: 1000
        }
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
