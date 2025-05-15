import React, { useEffect, useState } from 'react';
import { createSmartAccountClient } from '@base-org/onchainkit';
import { parseEther } from 'viem';

interface BaseWalletProps {
  onWalletReady: (address: string) => void;
  onPaymentComplete: (txHash: string) => void;
}

export const BaseWallet: React.FC<BaseWalletProps> = ({ onWalletReady, onPaymentComplete }) => {
  const [walletAddress, setWalletAddress] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeWallet();
  }, []);

  const initializeWallet = async () => {
    try {
      const smartAccount = await createSmartAccountClient({
        apiKey: process.env.VITE_BASE_API_KEY || '',
        chainId: 84531, // Base Goerli testnet
      });

      const address = await smartAccount.getAddress();
      setWalletAddress(address);
      setIsLoading(false);
      onWalletReady(address);
    } catch (err) {
      setError('Failed to initialize wallet');
      setIsLoading(false);
      console.error('Wallet initialization error:', err);
    }
  };

  const sendPayment = async (toAddress: string, amountInUsdc: number) => {
    try {
      setIsLoading(true);
      const smartAccount = await createSmartAccountClient({
        apiKey: process.env.VITE_BASE_API_KEY || '',
        chainId: 84531,
      });

      const tx = await smartAccount.sendTransaction({
        to: toAddress,
        value: parseEther(amountInUsdc.toString()),
      });

      onPaymentComplete(tx.hash);
      setIsLoading(false);
    } catch (err) {
      setError('Payment failed');
      setIsLoading(false);
      console.error('Payment error:', err);
    }
  };

  if (isLoading) {
    return <div className="p-4">Initializing wallet...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div>;
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4">Base Wallet</h2>
      <div className="mb-4">
        <p className="text-sm text-gray-600">Wallet Address:</p>
        <p className="font-mono text-sm">{walletAddress}</p>
      </div>
      {/* Additional wallet UI components can be added here */}
    </div>
  );
};

export default BaseWallet; 