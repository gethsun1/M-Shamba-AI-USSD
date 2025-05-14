import React, { useState, useEffect } from 'react';
import { USSDMenu } from './components/USSDMenu';

// Generate a simple session ID per user session
const generateSessionId = () => Math.random().toString(36).substr(2, 9);

export function App() {
  const [sessionId] = useState<string>(() => generateSessionId());
  const [inputText, setInputText] = useState<string>('');
  const [menuResponse, setMenuResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Environment variables for flexibility
  const API_URL = import.meta.env.VITE_USSD_API_URL;
  const SERVICE_CODE = import.meta.env.VITE_USSD_SERVICE_CODE;
  const PHONE_NUMBER = import.meta.env.VITE_USSD_PHONE_NUMBER;

  // Send USSD request to backend
  const sendUssdInput = async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/api/ussd/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ sessionId, serviceCode: SERVICE_CODE, phoneNumber: PHONE_NUMBER, text }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const textResponse = await response.text();
      setMenuResponse(textResponse);
    } catch (err: any) {
      console.error('USSD fetch error:', err);
      setError('Network error, please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Initialize the USSD session on mount
  useEffect(() => {
    sendUssdInput('');
  }, []);

  // Send subsequent inputs
  useEffect(() => {
    if (inputText !== '') sendUssdInput(inputText);
  }, [inputText]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 p-4">
      <div className="w-full max-w-sm bg-white text-green-500 p-4 font-mono rounded-lg shadow-lg border-2 border-green-500">
        <div className="text-center mb-4">
          <div className="text-xs">{SERVICE_CODE}</div>
          <div className="text-lg font-bold mb-2">M-SHAMBA AI</div>
          <div className="text-xs mb-4">USSD SERVICE</div>
        </div>
        <USSDMenu
          response={menuResponse}
          onSubmit={(value) => setInputText(prev => prev ? `${prev}*${value}` : value)}
          loading={isLoading}
          error={error}
        />
      </div>
    </div>
  );
}
