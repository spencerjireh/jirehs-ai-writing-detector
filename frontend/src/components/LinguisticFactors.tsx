import type { LinguisticFactor } from '../types/report';

interface LinguisticFactorsProps {
  factors: LinguisticFactor[];
}

function getBarColor(contribution: number): string {
  if (contribution === 0) return 'bg-green-400';
  if (contribution <= 3) return 'bg-yellow-400';
  return 'bg-red-400';
}

export function LinguisticFactors({ factors }: LinguisticFactorsProps) {
  if (factors.length === 0) return null;

  return (
    <section data-testid="linguistic-factors">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Linguistic Factors</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {factors.map((factor) => (
          <div
            key={factor.name}
            className="p-4 bg-white border border-gray-200 rounded-lg"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium text-gray-700">{factor.name}</span>
              <span className="text-sm font-mono text-gray-500">
                +{factor.score_contribution}
              </span>
            </div>
            <div className="w-full h-2 bg-gray-100 rounded-full mb-2">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getBarColor(factor.score_contribution)}`}
                style={{ width: `${Math.min(factor.value * 100, 100)}%` }}
              />
            </div>
            <p className="text-sm text-gray-500">{factor.explanation}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
