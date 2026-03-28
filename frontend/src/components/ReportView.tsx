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
    <div className="w-full max-w-3xl mx-auto space-y-8" data-testid="report-view">
      {/* Header: Score + Classification */}
      <div className="flex flex-col items-center gap-4">
        <ScoreGauge score={report.score} />
        <ClassificationBadge
          classification={report.classification}
          score={report.score}
        />
      </div>

      {/* Warnings */}
      {report.warnings.length > 0 && (
        <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg">
          {report.warnings.map((w, i) => (
            <p key={i} className="text-sm text-amber-700">{w}</p>
          ))}
        </div>
      )}

      {/* Stats Bar */}
      <div
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
        data-testid="stats-bar"
      >
        <StatCard label="Words" value={report.stats.word_count} />
        <StatCard label="Characters" value={report.stats.char_count} />
        <StatCard label="Sentences" value={report.stats.sentence_count} />
        <StatCard label="Avg Word Length" value={report.stats.avg_word_length} />
      </div>

      {/* Linguistic Factors */}
      <LinguisticFactors factors={report.linguistic_factors} />

      {/* Pattern Detections */}
      <PatternBreakdown detections={report.pattern_detections} />

      {/* Timestamp + Reset */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <span className="text-xs text-gray-400">
          Analyzed at {new Date(report.timestamp).toLocaleString()}
        </span>
        <button
          data-testid="reset-button"
          onClick={onReset}
          className="px-5 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg
                     hover:bg-gray-200 transition-colors"
        >
          Analyze Another
        </button>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="p-3 bg-white border border-gray-200 rounded-lg text-center">
      <div className="text-2xl font-bold text-gray-800">
        {typeof value === 'number' && !Number.isInteger(value) ? value.toFixed(1) : value}
      </div>
      <div className="text-xs text-gray-500 mt-1">{label}</div>
    </div>
  );
}
