import React, { Dispatch, SetStateAction, useState } from "react";
import ReactDOM from "react-dom";
import { Button, createTheme, CssBaseline, FormControlLabel, FormGroup, Switch, ThemeProvider } from "@material-ui/core";
import App from "./App";

const themeLight = createTheme({
  palette: {
    background: {
      default: "#e4f0e2"
    }
  }
});

const themeDark = createTheme({
  palette: {
    background: {
      default: "#222222"
    },
    text: {
      primary: "#ffffff"
    }
  }
});

export interface AppProps<S> {
  theme: [S, Dispatch<SetStateAction<S>>];
}

const ThemedApp = () => {
  const themee = useState(true);

  return (
    <ThemeProvider theme={themee[0] ? themeDark : themeLight}>
      <CssBaseline />
      <App theme={themee} />
    </ThemeProvider>
  );
};

const rootElement = document.getElementById("root");
ReactDOM.render(<ThemedApp />, rootElement);
