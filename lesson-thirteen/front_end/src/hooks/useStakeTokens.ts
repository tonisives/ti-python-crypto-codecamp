import { useContractFunction, useEthers } from "@usedapp/core"
import { constants, Contract, utils } from "ethers"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/RandomERC20.json"
import networkMapping from "../chain-info/deployments/map.json"
import { useState } from "react"

export const useStakeTokens = (tokenAddress: string) => {
    // approve
    // address, abi, chainId
    const { chainId } = useEthers()
    const { abi } = TokenFarm
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero
    const tokenFarmInterface = new utils.Interface(abi)
    // https://youtu.be/M576WGiDBdQ?t=56124
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)

    // any erc20 child is fine for the abi
    const erc20Abi = ERC20.abi
    const erc20Interface = new utils.Interface(erc20Abi)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)

    /**
     * useContractFunction
    Hook returns an object with three variables: state , send and events.
     */
    // state is status of the transaction, send is the function we can call
    const { send: approveErc20Send, state: approveErc20State } = useContractFunction(
        erc20Contract, "approve", { transactionName: "Approve ERC20 transfer" }
    )

    const approve = (amount: string) => {
        return approveErc20Send(tokenFarmAddress, amount)
    }

    return { approve, approveErc20State }
} 