import { makeStyles } from "@material-ui/core"

interface BalanceMsgProps {
    label: string,
    tokenImage: string,
    tokenBalance: number,
}
const useStyles = makeStyles((theme) => ({
    container: {
        display: "inline-grid",
        gridTemplateColumns: "auto auto auto",
        gap: theme.spacing(1),
        alignItems: "center",
    },
    tokenImg: {
        width: "32px",
    },
    amount: {
        fontWeight: 700,
    }
}))

export const BalanceMsg = ({ label, tokenImage, tokenBalance }: BalanceMsgProps) => {
    const classes = useStyles()

    return (<div>
        <div className={classes.container}>
            <div>{label}</div>
            <div className={classes.amount}>{tokenBalance}</div>
            <img className={classes.tokenImg} src={tokenImage} />
        </div>
    </div>)
}