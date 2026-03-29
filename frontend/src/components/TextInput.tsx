interface TextInputProps {
  text: string;
  onTextChange: (text: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export function TextInput({ text, onTextChange, onAnalyze, loading }: TextInputProps) {
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  return (
    <div className="w-full">
      <textarea
        data-testid="text-input"
        value={text}
        onChange={(e) => onTextChange(e.target.value)}
        placeholder="Paste or type text to analyze..."
        className="w-full h-72 p-6 rounded-lg border transition-all duration-300
                   font-[family-name:var(--font-body)] text-base leading-relaxed
                   resize-y
                   bg-[var(--color-card-light)] dark:bg-[var(--color-card-dark)]
                   border-[var(--color-border-light)] dark:border-[var(--color-border-dark)]
                   text-[var(--color-ink)] dark:text-[var(--color-ink-inverse)]
                   placeholder:text-[var(--color-ink-faint)] dark:placeholder:text-[var(--color-ink-inverse-muted)]
                   focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]/30 focus:border-[var(--color-accent)]"
      />
      <div className="flex items-center justify-between mt-4">
        <div
          className="font-[family-name:var(--font-mono)] text-xs tracking-wide
                     text-[var(--color-ink-faint)] dark:text-[var(--color-ink-inverse-muted)]"
          data-testid="text-counter"
        >
          {charCount} chars &middot; {wordCount} words
        </div>
        <button
          data-testid="analyze-button"
          onClick={onAnalyze}
          disabled={text.trim().length === 0 || loading}
          className="px-8 py-3 font-[family-name:var(--font-display)] font-semibold text-sm tracking-wide uppercase
                     rounded-lg transition-all duration-300
                     bg-[var(--color-ink)] text-[var(--color-surface-light)]
                     dark:bg-[var(--color-ink-inverse)] dark:text-[var(--color-surface-dark)]
                     hover:opacity-80 hover:translate-y-[-1px] hover:shadow-lg
                     disabled:opacity-30 disabled:cursor-not-allowed disabled:translate-y-0 disabled:shadow-none"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </div>
  );
}
