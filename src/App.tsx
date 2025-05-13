import React from 'react';
import { USSDMenu } from './components/USSDMenu';
export function App() {
  return <div className="flex items-center justify-center min-h-screen bg-gray-900 p-4">
      <div className="w-full max-w-sm bg-white text-green-500 p-4 font-mono rounded-lg shadow-lg border-2 border-green-500">
        <div className="text-center mb-4">
          <div className="text-xs">*483*1#</div>
          <div className="text-lg font-bold mb-2">M-SHAMBA AI</div>
          <div className="text-xs mb-4">USSD SERVICE</div>
        </div>
        <USSDMenu />
      </div>
    </div>;
}