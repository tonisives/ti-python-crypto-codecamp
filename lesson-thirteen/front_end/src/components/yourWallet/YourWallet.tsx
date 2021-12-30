import { Box, Tab } from "@material-ui/core"
import { TabContext, TabList, TabPanel } from "@material-ui/lab"
import { useState } from "react"
import { Token } from "../Main"
import { WalletBalance } from "./WalletBalance"

interface YourWalletProps {
    supportedTokens: Array<Token>
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    // setSelectedTokenIndex updates the selectedTokenIndex
    // useState saves state between renders(like jetpack compose)
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue))
    }

    return (
        <Box>
            <h1>Your wallet</h1>
            <TabContext value={selectedTokenIndex.toString()}>
                {/* list of tokens in the tab context */}
                <TabList onChange={handleChange} aria-label="stake form tabs">
                    {supportedTokens.map((token, index) => (
                        <Tab
                            label={token.name}
                            value={index.toString()}
                            key={index} />
                    ))}
                </TabList>
                {supportedTokens.map((token, index) => {
                    return (
                        <TabPanel value={index.toString()} key={index}>
                            <WalletBalance token={token} />
                        </TabPanel>
                    )
                })}
            </TabContext>

        </Box>
    )
}