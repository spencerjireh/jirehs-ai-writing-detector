interface ClassificationBadgeProps {
  classification: string;
  score: number;
}

function getBadgeStyle(score: number) {
  if (score < 30) return {
    bg: 'bg-[var(--color-emerald-soft)] dark:bg-[var(--color-emerald)]/15',
    text: 'text-[var(--color-emerald)]',
    border: 'border-[var(--color-emerald)]/30',
  };
  if (score < 60) return {
    bg: 'bg-[var(--color-amber-soft)] dark:bg-[var(--color-amber)]/15',
    text: 'text-[var(--color-amber)]',
    border: 'border-[var(--color-amber)]/30',
  };
  return {
    bg: 'bg-[var(--color-vermillion-soft)] dark:bg-[var(--color-vermillion)]/15',
    text: 'text-[var(--color-vermillion)]',
    border: 'border-[var(--color-vermillion)]/30',
  };
}

export function ClassificationBadge({ classification, score }: ClassificationBadgeProps) {
  const style = getBadgeStyle(score);

  return (
    <span
      data-testid="classification-badge"
      className={`inline-block px-5 py-2 text-sm font-[family-name:var(--font-display)] font-semibold
                  tracking-wide uppercase rounded-full border
                  animate-fade-in stagger-5
                  ${style.bg} ${style.text} ${style.border}`}
    >
      {classification}
    </span>
  );
}
