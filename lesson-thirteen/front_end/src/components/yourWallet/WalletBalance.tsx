import { useEthers, useTokenBalance } from "@usedapp/core"
import { formatUnits } from "ethers/lib/utils"
import { Token } from "../Main"
import { BalanceMsg } from "../BalanceMsg"

export interface WalletBalanceProps {
    token: Token,
}


export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    console.log(tokenBalance)
    const formattedBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    return (<BalanceMsg
        label={`Your unstaked ${name} balance`}
        tokenImage={image}
        tokenBalance={formattedBalance}
    />)
}