import type { PatternDetection } from '../types/report';

interface PatternBreakdownProps {
  detections: PatternDetection[];
}

export function PatternBreakdown({ detections }: PatternBreakdownProps) {
  if (detections.length === 0) return null;

  return (
    <div data-testid="pattern-breakdown">
      <div className="mb-5">
        <h2 className="font-[family-name:var(--font-display)] text-xl font-bold tracking-tight
                       text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
          Pattern Detections
        </h2>
        <div className="editorial-rule mt-2 w-12" />
      </div>

      <div className="space-y-4">
        {detections.map((detection, index) => (
          <div
            key={detection.category}
            className={`p-5 rounded-lg border transition-colors
                       bg-[var(--color-card-light)] dark:bg-[var(--color-card-dark)]
                       border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                       animate-fade-in-up stagger-${Math.min(index + 1, 8)}`}
          >
            <div className="flex items-baseline justify-between mb-3">
              <span className="font-[family-name:var(--font-body)] font-semibold text-sm
                             text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
                {detection.category}
              </span>
              <div className="flex items-center gap-3">
                <span className="font-[family-name:var(--font-mono)] text-xs
                               text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]">
                  {detection.occurrences} match{detection.occurrences !== 1 ? 'es' : ''}
                </span>
                <span className="font-[family-name:var(--font-mono)] text-xs font-semibold
                               text-[var(--color-vermillion)]">
                  +{detection.score_contribution}
                </span>
              </div>
            </div>

            {detection.details.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-3">
                {detection.details.map((detail, i) => (
                  <span
                    key={i}
                    className="inline-block px-2.5 py-1 text-xs rounded
                               font-[family-name:var(--font-mono)]
                               bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)]
                               text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)]
                               border border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]"
                  >
                    {detail}
                  </span>
                ))}
              </div>
            )}

            <p className="font-[family-name:var(--font-body)] text-sm leading-relaxed
                         text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)]">
              {detection.explanation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
