import { useEthers } from "@usedapp/core"
import { Button, FormControlLabel, makeStyles, Switch } from "@material-ui/core"
import { AppProps } from ".."

const useStyles = makeStyles(theme => ({
    container: {
        padding: theme.spacing(2),
        display: "flex",
        justifyContent: "flex-end",
        gap: theme.spacing(1)
    }
}))

export const Header: React.FC<AppProps<boolean>> = ({ theme }) => {
    const classes = useStyles()
    // variable
    const { account, activateBrowserWallet, deactivate } = useEthers();

    // if account is defined, user is connected
    const isConnected = account !== undefined

    // connect/disconnect button
    return (
        <div className={classes.container}>
            <div>
                <FormControlLabel control={
                    <Switch checked={theme[0]} onChange={() => theme[1](!theme[0])} />
                } label="Dark theme" />

                {isConnected ? (
                    <Button color="primary" variant="contained"
                        onClick={deactivate}>
                        Disconnect
                    </Button>
                ) : (
                    <Button color="primary" variant="contained"
                        onClick={() => activateBrowserWallet()}>
                        Connect
                    </Button>
                )
                }
            </div>
        </div>
    )
} 