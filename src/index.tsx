import './index.css';
import { MantineProvider } from "@mantine/core";
import "@mantine/core/styles.css";
import React from "react";
import { render } from "react-dom";
import { App } from "./App";
render(<MantineProvider>
    <App />
  </MantineProvider>, document.getElementById("root"));