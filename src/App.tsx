import { useState, useEffect } from 'react';
import USSDMenu from './components/USSDMenu';

const generateSessionId = () => Math.random().toString(36).substr(2, 9);

export default function App() {
  const [sessionId] = useState<string>(() => generateSessionId());
  const [inputHistory, setInputHistory] = useState<string>('');
  const [menuResponse, setMenuResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const SERVICE_CODE = import.meta.env.VITE_USSD_SERVICE_CODE;
  const PHONE_NUMBER = import.meta.env.VITE_USSD_PHONE_NUMBER;

  const sendUssdInput = async (text: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Get base URL with fallback to current origin
      const rawBase = import.meta.env.VITE_USSD_API_URL || window.location.origin;
      const sanitizedBase = rawBase.replace(/\\x3a/g, ':');
      
      // Ensure base URL has protocol
      const baseUrl = sanitizedBase.startsWith('http') ? sanitizedBase : `http://${sanitizedBase}`;
      
      // Construct full URL
      const endpoint = new URL('/ussd_callback/', baseUrl).href;
      console.log('✨ Fetching USSD at:', endpoint);

      const body = new URLSearchParams({
        sessionId,
        serviceCode: SERVICE_CODE,
        phoneNumber: PHONE_NUMBER,
        text,
      });

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const responseText = await res.text();
      setMenuResponse(responseText);

    } catch (err: any) {
      console.error('USSD fetch error:', err);
      setError('Network or server error.');
    } finally {
      setIsLoading(false);
    }
  };

  // Kick off session
  useEffect(() => {
    sendUssdInput('');
  }, []);

  const handleSubmit = (value: string) => {
    const newText = inputHistory ? `${inputHistory}*${value}` : value;
    setInputHistory(newText);
    sendUssdInput(newText);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-xs bg-white border-2 border-green-600 rounded-2xl shadow-lg p-6">
        <header className="text-center mb-6">
          <div className="text-sm text-gray-500">USSD: {SERVICE_CODE}</div>
          <h1 className="text-2xl font-bold text-green-700">M‑SHAMBA AI</h1>
        </header>

        <USSDMenu
          response={menuResponse}
          onSelect={handleSubmit}
          loading={isLoading}
          error={error}
        />
      </div>
    </div>
  );
}