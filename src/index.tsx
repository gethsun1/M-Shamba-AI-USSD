import React from 'react';
import ReactDOM from 'react-dom/client';      
import { MantineProvider } from '@mantine/core';
import { WagmiConfig } from 'wagmi';
import { config } from './lib/web3Config';
import App from './App';
import './index.css';

const container = document.getElementById('root');
if (!container) {
  throw new Error('Root container missing in index.html');
}

const root = ReactDOM.createRoot(container);
root.render(
  <React.StrictMode>
    <WagmiConfig config={config}>
      <MantineProvider>
        <App />
      </MantineProvider>
    </WagmiConfig>
  </React.StrictMode>
);