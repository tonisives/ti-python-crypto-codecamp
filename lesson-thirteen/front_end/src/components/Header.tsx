import { useEthers } from "@usedapp/core"
import { Button, makeStyles } from "@material-ui/core"

const useStyles = makeStyles(theme => ({
    container: {
        padding: theme.spacing(2),
        display: "flex",
        justifyContent: "flex-end",
        gap: theme.spacing(1)
    }
}))

export const Header = () => {
    const classes = useStyles()
    // variable
    const { account, activateBrowserWallet, deactivate } = useEthers();

    // if account is defined, user is connected
    const isConnected = account !== undefined

    // connect/disconnect button
    return (
        <div className={classes.container}>
            <div>
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