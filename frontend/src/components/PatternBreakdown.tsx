import type { PatternDetection } from '../types/report';

interface PatternBreakdownProps {
  detections: PatternDetection[];
}

export function PatternBreakdown({ detections }: PatternBreakdownProps) {
  if (detections.length === 0) return null;

  return (
    <section data-testid="pattern-breakdown">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Pattern Detections</h2>
      <div className="space-y-3">
        {detections.map((detection) => (
          <div
            key={detection.category}
            className="p-4 bg-white border border-gray-200 rounded-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-gray-700">{detection.category}</span>
              <div className="flex items-center gap-3 text-sm">
                <span className="text-gray-500">
                  {detection.occurrences} match{detection.occurrences !== 1 ? 'es' : ''}
                </span>
                <span className="font-mono text-red-600 font-medium">
                  +{detection.score_contribution}
                </span>
              </div>
            </div>
            {detection.details.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-2">
                {detection.details.map((detail, i) => (
                  <span
                    key={i}
                    className="inline-block px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded"
                  >
                    {detail}
                  </span>
                ))}
              </div>
            )}
            <p className="text-sm text-gray-500">{detection.explanation}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
