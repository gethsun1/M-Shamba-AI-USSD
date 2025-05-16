import { useState } from 'react';

type USSDMenuProps = {
  response: string;
  loading: boolean;
  error: string | null;
  onSelect: (value: string) => void;
  onRestart: () => void; // New prop for restart functionality
};

export default function USSDMenu({ response, loading, error, onSelect, onRestart }: USSDMenuProps) {
  const [choice, setChoice] = useState<string>('');

  const lines = response.split('\n');
  const isEnd = lines[lines.length - 1].startsWith('END');

  return (
    <div>
      <div className="font-mono bg-gray-50 p-4 rounded-md h-48 overflow-y-auto mb-4">
        {loading
          ? <p className="italic text-gray-400">Simulating USSD...</p>
          : lines.map((line, idx) => <div key={idx}>{line}</div>)
        }
        {error && <div className="text-red-500 mt-2">{error}</div>}
      </div>

      {!loading && !isEnd && (
        <form
          onSubmit={e => {
            e.preventDefault();
            if (choice.trim()) {
              onSelect(choice.trim());
              setChoice('');
            }
          }}
        >
          <input
            type="text"
            value={choice}
            onChange={e => setChoice(e.target.value)}
            placeholder="Select Option..."
            className="w-full p-2 border border-gray-300 rounded-md mb-2 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button
            type="submit"
            className="w-full bg-green-600 text-white p-2 rounded-md hover:bg-green-700"
          >
            Send
          </button>
        </form>
      )}
      
      {/* Add restart button when the flow ends */}
      {!loading && isEnd && (
        <button
          onClick={onRestart}
          className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 mt-4"
        >
          Start New Session
        </button>
      )}
    </div>
  );
}