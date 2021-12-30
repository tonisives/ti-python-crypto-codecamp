import { Button, Input } from "@material-ui/core"
import { useEthers, useTokenBalance } from "@usedapp/core"
import { utils } from "ethers"
import { formatUnits } from "ethers/lib/utils"
import { useState } from "react"
import { useStakeTokens } from "../../hooks/useStakeTokens"
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

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value)
        setAmount(newAmount)
        console.log(newAmount)
    }

    const { approve, approveErc20State } = useStakeTokens(tokenAddress)

    const handleStakeClick = () => {
        /**
         * - approve the tokens 
         * - call TokenFarm.sol function stakeTokens(uint256 _amount, address _token)
         * call these automatically in order
         */
        const amountAsWei = utils.parseEther(amount.toString())
        return approve(amountAsWei.toString())
    }


    return (<div>
        <>
            <Input onChange={handleInputChange} />
            <Button onClick={handleStakeClick} color="primary" size="large" variant="contained">Stake</Button>
        </>
    </div>)
}