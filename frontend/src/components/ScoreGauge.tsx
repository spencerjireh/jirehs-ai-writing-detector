interface ScoreGaugeProps {
  score: number;
}

function getScoreColor(score: number): string {
  if (score < 30) return '#22c55e';   // green
  if (score < 60) return '#eab308';   // yellow
  return '#ef4444';                    // red
}

function getScoreBg(score: number): string {
  if (score < 30) return 'bg-green-50 border-green-200';
  if (score < 60) return 'bg-yellow-50 border-yellow-200';
  return 'bg-red-50 border-red-200';
}

export function ScoreGauge({ score }: ScoreGaugeProps) {
  const color = getScoreColor(score);
  const bgClasses = getScoreBg(score);
  const rotation = (score / 100) * 180 - 90; // -90 to 90 degrees

  return (
    <div
      data-testid="score-gauge"
      className={`inline-flex flex-col items-center p-8 rounded-2xl border ${bgClasses}`}
    >
      <div className="relative w-48 h-24 overflow-hidden">
        {/* Background arc */}
        <div className="absolute inset-0 rounded-t-full border-8 border-gray-200 border-b-0" />
        {/* Colored fill arc */}
        <div
          className="absolute bottom-0 left-1/2 w-1 h-24 origin-bottom transition-transform duration-700"
          style={{
            transform: `rotate(${rotation}deg)`,
            backgroundColor: color,
          }}
        />
        {/* Center cover */}
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-32 h-16 bg-inherit rounded-t-full" />
      </div>
      <div
        className="text-6xl font-bold -mt-4"
        style={{ color }}
        data-testid="score-value"
      >
        {score}
      </div>
      <div className="text-sm text-gray-500 mt-1">out of 100</div>
    </div>
  );
}
