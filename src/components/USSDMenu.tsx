import React from 'react';
import { Text, Button, Loader, Center } from '@mantine/core';

interface USSDMenuProps {
  /** Raw USSD response text, including leading 'CON ' or 'END ' */
  response: string;
  /** Called with the digit ('1', '2', ..., '*', '#') user selects */
  onSubmit: (input: string) => void;
  /** True if awaiting backend reply */
  loading: boolean;
  /** Network or session error message */
  error: string | null;
}

export function USSDMenu({ response, onSubmit, loading, error }: USSDMenuProps) {
  // Determine if session ended
  const isEnded = response.trim().startsWith('END');

  return (
    <div className="space-y-4">
      {/* Display loading, error, or USSD response */}
      {loading ? (
        <Center style={{ height: 100 }}><Loader /></Center>
      ) : error ? (
        <Text className="text-xs text-red-600 text-center p-4">{error}</Text>
      ) : (
        <pre className="whitespace-pre-wrap text-xs p-2 border border-green-500 rounded">{response}</pre>
      )}

      {/* Keypad disabled if session ended or loading */}
      <div className="text-xs text-center mt-2">
        {isEnded ? 'Session ended. Dial *483*1# to restart.' : 'Enter number and press Send'}
      </div>

      <div className="grid grid-cols-3 gap-2 text-black">
        {['1','2','3','4','5','6','7','8','9','*','0','#'].map(key => (
          <Button
            key={key}
            variant="outline"
            color="green"
            size="xs"
            disabled={loading || isEnded}
            onClick={() => onSubmit(key)}
            className="aspect-square"
          >
            {key}
          </Button>
        ))}
      </div>
    </div>
  );
}
