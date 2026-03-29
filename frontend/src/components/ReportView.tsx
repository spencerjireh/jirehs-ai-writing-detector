import type { AnalyzeResponse } from '../types/report';
import { ScoreGauge } from './ScoreGauge';
import { ClassificationBadge } from './ClassificationBadge';
import { LinguisticFactors } from './LinguisticFactors';
import { PatternBreakdown } from './PatternBreakdown';

interface ReportViewProps {
  report: AnalyzeResponse;
  text: string;
  onTextChange: (text: string) => void;
  onReAnalyze: () => void;
  reanalyzing: boolean;
  onReset: () => void;
}

export function ReportView({ report, text, onTextChange, onReAnalyze, reanalyzing, onReset }: ReportViewProps) {
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  return (
    <div className="w-full" data-testid="report-view">
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr] gap-10 lg:gap-14">
        {/* Left Column: Text */}
        <div className="animate-fade-in-up">
          <SectionHeader title="Your Text" />
          <div className="mt-5 lg:sticky lg:top-10">
            <textarea
              data-testid="text-input"
              value={text}
              onChange={(e) => onTextChange(e.target.value)}
              className="w-full h-80 lg:h-[calc(100vh-16rem)] p-6 rounded-lg border transition-all duration-300
                         font-[family-name:var(--font-body)] text-base leading-relaxed
                         resize-y
                         bg-[var(--color-card-light)] dark:bg-[var(--color-card-dark)]
                         border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                         text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]
                         placeholder:text-[var(--color-ink-faint)] dark:placeholder:text-[var(--color-ink-inverse-muted)]
                         focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]/30 focus:border-[var(--color-accent)]"
            />
            <div className="flex items-center justify-between mt-4">
              <div
                className="font-[family-name:var(--font-mono)] text-xs tracking-wide
                           text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]"
                data-testid="text-counter"
              >
                {charCount} chars &middot; {wordCount} words
              </div>
              <button
                data-testid="analyze-button"
                onClick={onReAnalyze}
                disabled={text.trim().length === 0 || reanalyzing}
                className="px-6 py-2.5 font-[family-name:var(--font-display)] font-semibold text-sm tracking-wide uppercase
                           rounded-lg transition-all duration-300
                           bg-[var(--color-ink)] text-[var(--color-surface-light)]
                           dark:bg-[var(--color-ink-inverse)] dark:text-[var(--color-surface-dark)]
                           hover:opacity-80 hover:translate-y-[-1px] hover:shadow-lg
                           disabled:opacity-30 disabled:cursor-not-allowed disabled:translate-y-0 disabled:shadow-none"
              >
                {reanalyzing ? 'Analyzing...' : 'Re-Analyze'}
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Report */}
        <div className={`space-y-14 transition-opacity duration-300 ${reanalyzing ? 'opacity-50' : 'opacity-100'}`}>
          {/* Hero: Score + Classification */}
          <section className="flex flex-col items-center gap-5 pt-4 animate-fade-in-up">
            <ScoreGauge score={report.score} />
            <ClassificationBadge
              classification={report.classification}
              score={report.score}
            />
          </section>

          {/* Warnings */}
          {report.warnings.length > 0 && (
            <div className="p-4 rounded-lg border animate-fade-in-up stagger-3
                            bg-[var(--color-amber-soft)] border-[var(--color-amber)]/30
                            dark:bg-[var(--color-amber)]/10 dark:border-[var(--color-amber)]/20">
              {report.warnings.map((w, i) => (
                <p key={i} className="text-sm text-[var(--color-amber)] font-[family-name:var(--font-body)]">{w}</p>
              ))}
            </div>
          )}

          {/* Stats */}
          <section className="animate-fade-in-up stagger-4">
            <SectionHeader title="Text Statistics" />
            <div
              className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5"
              data-testid="stats-bar"
            >
              <StatCard label="Words" value={report.stats.word_count} delay={1} />
              <StatCard label="Characters" value={report.stats.char_count} delay={2} />
              <StatCard label="Sentences" value={report.stats.sentence_count} delay={3} />
              <StatCard label="Avg Length" value={report.stats.avg_word_length} delay={4} />
            </div>
          </section>

          {/* Linguistic Factors */}
          <section className="animate-fade-in-up stagger-5">
            <LinguisticFactors factors={report.linguistic_factors} />
          </section>

          {/* Pattern Detections */}
          <section className="animate-fade-in-up stagger-6">
            <PatternBreakdown detections={report.pattern_detections} />
          </section>

          {/* Footer */}
          <footer className="flex items-center justify-between pt-8 animate-fade-in-up stagger-7">
            <span className="font-[family-name:var(--font-mono)] text-xs
                             text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]">
              {new Date(report.timestamp).toLocaleString()}
            </span>
            <button
              data-testid="reset-button"
              onClick={onReset}
              className="px-6 py-2.5 font-[family-name:var(--font-display)] font-semibold text-sm tracking-wide uppercase
                         rounded-lg border transition-all duration-300
                         border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                         text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]
                         hover:border-[var(--color-ink)] dark:hover:border-[var(--color-ink-inverse)]
                         hover:translate-y-[-1px] hover:shadow-md
                         bg-transparent"
            >
              Analyze Another
            </button>
          </footer>
        </div>
      </div>
    </div>
  );
}

function SectionHeader({ title }: { title: string }) {
  return (
    <div>
      <h2 className="font-[family-name:var(--font-display)] text-xl font-bold tracking-tight
                     text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
        {title}
      </h2>
      <div className="editorial-rule mt-2 w-12" />
    </div>
  );
}

function StatCard({ label, value, delay }: { label: string; value: number; delay: number }) {
  const formatted = typeof value === 'number' && !Number.isInteger(value) ? value.toFixed(1) : value;
  return (
    <div className={`p-4 rounded-lg border transition-colors
                     bg-[var(--color-card-light)] dark:bg-[var(--color-card-dark)]
                     border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                     animate-fade-in-up stagger-${delay}`}>
      <div className="font-[family-name:var(--font-mono)] text-2xl font-semibold
                      text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
        {formatted}
      </div>
      <div className="font-[family-name:var(--font-body)] text-xs mt-1 tracking-wide uppercase
                      text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]">
        {label}
      </div>
    </div>
  );
}
