import type { AnalyzeResponse } from '../types/report';
import { ScoreGauge } from './ScoreGauge';
import { ClassificationBadge } from './ClassificationBadge';
import { LinguisticFactors } from './LinguisticFactors';
import { PatternBreakdown } from './PatternBreakdown';

interface ReportViewProps {
  report: AnalyzeResponse;
  onReset: () => void;
}

export function ReportView({ report, onReset }: ReportViewProps) {
  return (
    <div className="w-full space-y-14" data-testid="report-view">
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
