
import { configureChains, createConfig } from 'wagmi';
import { baseGoerli } from '@wagmi/core/chains';
import { publicProvider } from '@wagmi/core/providers/public';
import { createWeb3Modal } from '@web3modal/wagmi';

const projectId = import.meta.env.VITE_WALLETCONNECT_PROJECT_ID;

// Configure chains and providers using wagmi v2+ core packages
const { chains, publicClient } = configureChains(
  [baseGoerli],
  [publicProvider()]
);

export const config = createConfig({
  autoConnect: true,
  publicClient,
  chains,
});

export const web3modal = createWeb3Modal({
  wagmiConfig: config,
  projectId,
  chains,
  themeMode: 'light',
  themeVariables: {
    '--w3m-accent': '#22c55e', // Tailwind green-600
  },
});

