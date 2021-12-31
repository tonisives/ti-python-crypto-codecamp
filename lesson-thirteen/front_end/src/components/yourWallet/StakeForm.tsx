import { Button, CircularProgress, Input } from "@material-ui/core"
import { useEthers, useNotifications, useTokenBalance } from "@usedapp/core"
import { utils } from "ethers"
import { formatUnits } from "ethers/lib/utils"
import { useEffect, useState } from "react"
import { approveTxName, stakeTxName, useStakeTokens } from "../../hooks/useStakeTokens"
import { Token } from "../Main"

interface StakeFormProps {
    token: Token
}

export const StakeForm = ({ token }: StakeFormProps) => {
    const { address: tokenAddress, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(tokenAddress, account)
    const formattedTokenBalance = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    const [amount, setAmount] = useState<number | string | Array<number | string>>(0)
    const { notifications } = useNotifications()


    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value)
        setAmount(newAmount)
        console.log(newAmount)
    }

    const { approveAndStake, state } = useStakeTokens(tokenAddress)
    const isMining = state.status === "Mining"

    const handleStakeClick = () => {
        /**
         * - approve the tokens 
         * - call TokenFarm.sol function stakeTokens(uint256 _amount, address _token)
         * call these automatically in order
         */
        const amountAsWei = utils.parseEther(amount.toString())
        return approveAndStake(amountAsWei.toString())
    }

    // useEffect when something changes with the contract notification
    useEffect(() => {
        // follow approve erc20 and tx succeded
        if (notifications.filter((notification) =>
            notification.type === "transactionSucceed" &&
            notification.transactionName === approveTxName).length > 0) {
            console.log("approved")
        }

        if (notifications.filter((notification) =>
            notification.type === "transactionSucceed" &&
            notification.transactionName === stakeTxName).length > 0) {
            console.log("tokens staked")
        }

    }, [notifications])

    return (<div>
        <>
            <Input onChange={handleInputChange} />
            <Button
                onClick={handleStakeClick}
                color="primary"
                size="large"
                variant="contained"
                disabled={isMining}>
                {isMining ? <CircularProgress size={26} /> : "Stake"}
            </Button>
        </>
    </div>)
}