
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
  const API_BASE_RAW = import.meta.env.VITE_USSD_API_URL;

  const sendUssdInput = async (text: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Sanitize raw base URL in case of escaped characters
      const raw = API_BASE_RAW || 'http://localhost:8000';
      const sanitizedBase = raw.replace(/\\x3a/g, ':').replace(/\/+$/g, '');
      // Build endpoint using URL constructor
      const endpoint = new URL('/ussd_callback/', sanitizedBase).href;
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
      setError(`Network error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Kick off session
  useEffect(() => {
    sendUssdInput('');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSubmit = (value: string) => {
    const newText = inputHistory ? `${inputHistory}*${value}` : value;
    setInputHistory(newText);
    sendUssdInput(newText);
  };

  // Handler to restart the USSD session
  const handleRestart = () => {
    setInputHistory('');
    sendUssdInput('');
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
          onRestart={handleRestart}
        />
      </div>
    </div>
  );
}
