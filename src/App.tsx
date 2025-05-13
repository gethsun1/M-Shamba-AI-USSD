import React, { useState, useEffect } from 'react';
import { USSDMenu } from './components/USSDMenu';

// Utility to generate a simple session ID
const generateSessionId = () => Math.random().toString(36).substr(2, 9);

export function App() {
  // Track session and message state
  const [sessionId] = useState<string>(generateSessionId());
  const [inputText, setInputText] = useState<string>('');
  const [menuResponse, setMenuResponse] = useState<string>('CON Karibu M-Shamba AI\n1. Uza Mazao\n2. Angalia Bei\n3. Akaunti\n4. Msaada');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Function to call the Django backend USSD endpoint
  const sendUssdInput = async (text: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(import.meta.env.VITE_USSD_API_URL + '/api/ussd/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          sessionId,
          serviceCode: '*483*1#',
          phoneNumber: '+254700123456',
          text,
        }),
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

  // Whenever user enters new input, send it
  useEffect(() => {
    if (inputText !== '') sendUssdInput(inputText);
  }, [inputText]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 p-4">
      <div className="w-full max-w-sm bg-white text-green-500 p-4 font-mono rounded-lg shadow-lg border-2 border-green-500">
        <div className="text-center mb-4">
          <div className="text-xs">*483*1#</div>
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
