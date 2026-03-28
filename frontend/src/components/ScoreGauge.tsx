interface ScoreGaugeProps {
  score: number;
}

const RADIUS = 80;
const STROKE = 10;
const CIRCUMFERENCE = Math.PI * RADIUS;

function getScoreLabel(score: number): string {
  if (score < 30) return 'Low';
  if (score < 60) return 'Moderate';
  return 'High';
}

function getScoreColor(score: number): string {
  if (score < 30) return 'var(--color-emerald)';
  if (score < 60) return 'var(--color-amber)';
  return 'var(--color-vermillion)';
}

export function ScoreGauge({ score }: ScoreGaugeProps) {
  const clampedScore = Math.max(0, Math.min(100, score));
  const dashoffset = CIRCUMFERENCE - (clampedScore / 100) * CIRCUMFERENCE;

  return (
    <div
      data-testid="score-gauge"
      className="flex flex-col items-center"
    >
      <div className="relative" style={{ width: 200, height: 120 }}>
        <svg
          viewBox="0 0 200 120"
          width="200"
          height="120"
          className="overflow-visible"
        >
          <defs>
            <linearGradient id="arc-gradient" gradientUnits="userSpaceOnUse" x1="20" y1="100" x2="180" y2="100">
              <stop offset="0%" stopColor="var(--color-emerald)" />
              <stop offset="50%" stopColor="var(--color-amber)" />
              <stop offset="100%" stopColor="var(--color-vermillion)" />
            </linearGradient>
          </defs>

          {/* Background track */}
          <path
            d={`M ${100 - RADIUS} 100 A ${RADIUS} ${RADIUS} 0 0 1 ${100 + RADIUS} 100`}
            fill="none"
            stroke="var(--color-border-light)"
            strokeWidth={STROKE}
            strokeLinecap="round"
            className="dark:stroke-[var(--color-border-dark)]"
          />

          {/* Animated fill arc */}
          <path
            d={`M ${100 - RADIUS} 100 A ${RADIUS} ${RADIUS} 0 0 1 ${100 + RADIUS} 100`}
            fill="none"
            stroke="url(#arc-gradient)"
            strokeWidth={STROKE}
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={dashoffset}
            className="arc-animated"
            style={{
              '--arc-circumference': CIRCUMFERENCE,
              '--arc-target': dashoffset,
            } as React.CSSProperties}
          />
        </svg>

        {/* Score number */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-1">
          <span
            className="font-[family-name:var(--font-display)] text-6xl font-bold leading-none
                       animate-fade-in stagger-4"
            style={{ color: getScoreColor(clampedScore) }}
            data-testid="score-value"
          >
            {clampedScore}
          </span>
        </div>
      </div>

      <div className="mt-1 flex flex-col items-center gap-1">
        <span
          className="font-[family-name:var(--font-mono)] text-xs tracking-wider uppercase
                     text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]"
        >
          {getScoreLabel(clampedScore)} probability &middot; {clampedScore}/100
        </span>
      </div>
    </div>
  );
}
