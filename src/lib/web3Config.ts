import { createConfig, configureChains } from 'wagmi';
import { baseGoerli } from 'wagmi/chains';
import { publicProvider } from 'wagmi/providers/public';
import { createWeb3Modal } from '@web3modal/wagmi';

const projectId = import.meta.env.VITE_WALLETCONNECT_PROJECT_ID;

const { chains, publicClient } = configureChains(
  [baseGoerli],
  [publicProvider()]
);

export const config = createConfig({
  autoConnect: true,
  publicClient,
  chains
});

export const web3modal = createWeb3Modal({
  wagmiConfig: config,
  projectId,
  chains,
  themeMode: 'light',
  themeVariables: {
    '--w3m-accent': '#22c55e', // Green-600 from Tailwind
  }
});