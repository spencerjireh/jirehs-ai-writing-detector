import { useState } from 'react';
import { analyzeText } from './api/client';
import type { AnalyzeResponse } from './types/report';
import { TextInput } from './components/TextInput';
import { ReportView } from './components/ReportView';
import { ThemeToggle } from './components/ThemeToggle';

type View = 'input' | 'loading' | 'report';

export default function App() {
  const [view, setView] = useState<View>('input');
  const [report, setReport] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze(text: string) {
    setError(null);
    setView('loading');
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
    <div className="min-h-screen py-10 px-4 sm:px-6 transition-colors duration-400">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <header className="flex items-start justify-between mb-12 animate-fade-in-up">
          <div>
            <h1
              className="font-[family-name:var(--font-display)] text-4xl sm:text-5xl font-bold tracking-tight
                         text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]
                         leading-[1.1]"
            >
              AI Writing<br />Detector
            </h1>
            <p
              className="mt-3 font-[family-name:var(--font-body)] text-base sm:text-lg
                         text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)]
                         max-w-sm leading-relaxed animate-fade-in-up stagger-2"
            >
              Analyze text to estimate the probability it was written by AI.
            </p>
          </div>
          <ThemeToggle />
        </header>

        {/* Error */}
        {error && (
          <div
            className="mb-8 p-4 rounded-lg border animate-slide-down
                       bg-[var(--color-vermillion-soft)] border-[var(--color-vermillion)]
                       dark:bg-[var(--color-vermillion)]/10 dark:border-[var(--color-vermillion)]/40
                       text-[var(--color-vermillion)] text-sm font-[family-name:var(--font-body)]"
            data-testid="error-message"
          >
            {error}
          </div>
        )}

        {/* Input View */}
        {view === 'input' && (
          <div className="animate-fade-in-up stagger-3">
            <TextInput onAnalyze={handleAnalyze} loading={false} />
          </div>
        )}

        {/* Loading View */}
        {view === 'loading' && (
          <div
            className="flex flex-col items-center gap-6 py-24 animate-fade-in"
            data-testid="loading-indicator"
          >
            <div className="flex gap-2">
              <div className="loading-dot w-2.5 h-2.5 rounded-full bg-[var(--color-ink-muted)] dark:bg-[var(--color-ink-inverse-muted)]" />
              <div className="loading-dot w-2.5 h-2.5 rounded-full bg-[var(--color-ink-muted)] dark:bg-[var(--color-ink-inverse-muted)]" />
              <div className="loading-dot w-2.5 h-2.5 rounded-full bg-[var(--color-ink-muted)] dark:bg-[var(--color-ink-inverse-muted)]" />
            </div>
            <p className="font-[family-name:var(--font-body)] text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)] text-sm tracking-wide uppercase">
              Analyzing text
            </p>
          </div>
        )}

        {/* Report View */}
        {view === 'report' && report && (
          <div className="animate-fade-in-up">
            <ReportView report={report} onReset={handleReset} />
          </div>
        )}
      </div>
    </div>
  );
}
