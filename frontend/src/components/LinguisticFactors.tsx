import type { LinguisticFactor } from '../types/report';

interface LinguisticFactorsProps {
  factors: LinguisticFactor[];
}

function getBarColor(contribution: number): string {
  if (contribution === 0) return 'bg-[var(--color-emerald)]';
  if (contribution <= 3) return 'bg-[var(--color-amber)]';
  return 'bg-[var(--color-vermillion)]';
}

export function LinguisticFactors({ factors }: LinguisticFactorsProps) {
  if (factors.length === 0) return null;

  return (
    <div data-testid="linguistic-factors">
      <div className="mb-5">
        <h2 className="font-[family-name:var(--font-display)] text-xl font-bold tracking-tight
                       text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
          Linguistic Factors
        </h2>
        <div className="editorial-rule mt-2 w-12" />
      </div>

      <div className="space-y-4">
        {factors.map((factor, index) => (
          <div
            key={factor.name}
            className={`p-5 rounded-lg border transition-colors
                       bg-[var(--color-card-light)] dark:bg-[var(--color-card-dark)]
                       border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                       animate-fade-in-up stagger-${Math.min(index + 1, 8)}`}
          >
            <div className="flex items-baseline justify-between mb-3">
              <span className="font-[family-name:var(--font-body)] font-semibold text-sm
                             text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]">
                {factor.name}
              </span>
              <span className="font-[family-name:var(--font-mono)] text-xs
                             text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)]">
                +{factor.score_contribution}
              </span>
            </div>

            <div className="w-full h-1 rounded-full mb-3
                           bg-[var(--color-border-light)] dark:bg-[var(--color-border-dark)]">
              <div
                className={`h-full rounded-full transition-all duration-700 ease-out ${getBarColor(factor.score_contribution)}`}
                style={{ width: `${Math.min(factor.value * 100, 100)}%` }}
              />
            </div>

            <p className="font-[family-name:var(--font-body)] text-sm leading-relaxed
                         text-[var(--color-ink-muted)] dark:text-[var(--color-ink-inverse-muted)]">
              {factor.explanation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
