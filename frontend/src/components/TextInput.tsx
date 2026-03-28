import { useState } from 'react';

interface TextInputProps {
  onAnalyze: (text: string) => void;
  loading: boolean;
}

export function TextInput({ onAnalyze, loading }: TextInputProps) {
  const [text, setText] = useState('');

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  return (
    <div className="w-full max-w-3xl mx-auto">
      <textarea
        data-testid="text-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste or type text to analyze..."
        className="w-full h-64 p-4 border border-gray-300 rounded-lg resize-y
                   text-base leading-relaxed focus:outline-none focus:ring-2
                   focus:ring-blue-500 focus:border-transparent
                   bg-white text-gray-900"
      />
      <div className="flex items-center justify-between mt-3">
        <div className="text-sm text-gray-500" data-testid="text-counter">
          {charCount} characters / {wordCount} words
        </div>
        <button
          data-testid="analyze-button"
          onClick={() => onAnalyze(text)}
          disabled={text.trim().length === 0 || loading}
          className="px-6 py-2.5 bg-blue-600 text-white font-medium rounded-lg
                     hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                     transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </div>
  );
}
