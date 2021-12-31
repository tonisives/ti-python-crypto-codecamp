import { useContractFunction, useEthers } from "@usedapp/core"
import { constants, Contract, utils } from "ethers"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/RandomERC20.json"
import networkMapping from "../chain-info/deployments/map.json"
import { useEffect, useState } from "react"

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
    // state is status of the transaction, send is the function we can call. send can have any number of arguments that are passed to the contract.
    const { send: approveErc20Send, state: approveErc20State } = useContractFunction(
        erc20Contract, "approve", { transactionName: "Approve ERC20 transfer" }
    )

    // listen for the approved amount
    const [amountToStake, setAmountToStake] = useState("0")

    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        return approveErc20Send(tokenFarmAddress, amount)
    }

    const { send: stakeSend, state: stakeState } = useContractFunction(
        tokenFarmContract,
        "stakeTokens",
        { transactionName: "Stake tokens" }
    )

    // useEffect - do something after variable has changed.
    // TODO: there should be a loading spinner between approve and stake
    useEffect(() => {
        if (approveErc20State.status === "Success") {
            // stake
            console.log("Approved ERC20 transfer")

            // function stakeTokens(uint256 _amount, address _token) public {
            stakeSend(amountToStake, tokenAddress)
        }

        // if anything in this array changes, it will kick off the useEffect
    }, [approveErc20State])

    // return the approve function, so it can be called with the amount from the StakeForm
    return { approveAndStake, approveErc20State }
} 