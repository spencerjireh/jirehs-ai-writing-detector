import { useState } from 'react';
import type { AnalyzeResponse } from './types/report';
import { analyzeText } from './api/client';
import { TextInput } from './components/TextInput';
import { ReportView } from './components/ReportView';

type View = 'input' | 'loading' | 'report';

function App() {
  const [view, setView] = useState<View>('input');
  const [report, setReport] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze(text: string) {
    setView('loading');
    setError(null);
    try {
      const result = await analyzeText(text);
      setReport(result);
      setView('report');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
      setView('input');
    }
  }

  function handleReset() {
    setReport(null);
    setView('input');
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            AI Writing Detector
          </h1>
          <p className="text-gray-500 mt-2">
            Analyze text to estimate the probability it was written by AI
          </p>
        </header>

        {error && (
          <div
            className="max-w-3xl mx-auto mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700"
            data-testid="error-message"
          >
            {error}
          </div>
        )}

        {view === 'input' && (
          <TextInput onAnalyze={handleAnalyze} loading={false} />
        )}

        {view === 'loading' && (
          <div className="flex flex-col items-center gap-4 py-16" data-testid="loading-indicator">
            <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
            <p className="text-gray-500">Analyzing text...</p>
          </div>
        )}

        {view === 'report' && report && (
          <ReportView report={report} onReset={handleReset} />
        )}
      </div>
    </div>
  );
}

export default App;
