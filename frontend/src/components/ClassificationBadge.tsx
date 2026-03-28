interface ClassificationBadgeProps {
  classification: string;
  score: number;
}

function getBadgeClasses(score: number): string {
  if (score < 30) return 'bg-green-100 text-green-800 border-green-300';
  if (score < 60) return 'bg-yellow-100 text-yellow-800 border-yellow-300';
  return 'bg-red-100 text-red-800 border-red-300';
}

export function ClassificationBadge({ classification, score }: ClassificationBadgeProps) {
  return (
    <span
      data-testid="classification-badge"
      className={`inline-block px-4 py-2 text-lg font-semibold rounded-full border ${getBadgeClasses(score)}`}
    >
      {classification}
    </span>
  );
}
