import React, { useEffect, useRef } from 'react';
import { Terminal, Copy, Check } from 'lucide-react';

interface AgentLogProps {
  logs: string[];
}

export default function AgentLog({ logs }: AgentLogProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [copied, setCopied] = React.useState(false);

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTo({
        top: scrollContainerRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [logs]);

  const copyLogs = () => {
    navigator.clipboard.writeText(logs.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const parseLogLine = (line: string) => {
    const timestamp = new Date().toLocaleTimeString();
    let cleanLine = line;
    let type = 'system';
    let typeColor = 'text-slate-500 bg-slate-900 border-slate-800';

    if (line.startsWith('[INFO]')) {
      cleanLine = line.replace('[INFO] ', '');
      type = 'INFO';
      typeColor = 'text-slate-400 bg-slate-800/40 border-slate-700/40';
    } else if (line.startsWith('[REASONING]')) {
      cleanLine = line.replace('[REASONING] ', '');
      type = 'REASON';
      typeColor = 'text-accent-indigo bg-accent-indigo/10 border-accent-indigo/20';
    } else if (line.startsWith('[DECISION]')) {
      cleanLine = line.replace('[DECISION] ', '');
      type = 'DECIDE';
      typeColor = 'text-accent-violet bg-accent-violet/10 border-accent-violet/20';
    } else if (line.startsWith('[STRATEGY]')) {
      cleanLine = line.replace('[STRATEGY] ', '');
      type = 'STRAT';
      typeColor = 'text-accent-indigo bg-accent-indigo/10 border-accent-indigo/20';
    } else if (line.startsWith('[RESEARCH]')) {
      cleanLine = line.replace('[RESEARCH] ', '');
      type = 'RESEARCH';
      typeColor = 'text-accent-violet bg-accent-violet/10 border-accent-violet/20';
    } else if (line.startsWith('[COMPETITOR ANALYSES]')) {
      cleanLine = line.replace('[COMPETITOR ANALYSES] ', '');
      type = 'COMPETE';
      typeColor = 'text-pink-400 bg-pink-900/10 border-pink-800/20';
    } else if (line.startsWith('[PERSONA CREATED]')) {
      cleanLine = line.replace('[PERSONA CREATED] ', '');
      type = 'PERSONA';
      typeColor = 'text-accent-violet bg-accent-violet/10 border-accent-violet/20';
    } else if (line.startsWith('[TREND SEARCH]')) {
      cleanLine = line.replace('[TREND SEARCH] ', '');
      type = 'TREND';
      typeColor = 'text-yellow-400/80 bg-yellow-900/10 border-yellow-800/20';
    } else if (line.startsWith('[COPYWRITING]')) {
      cleanLine = line.replace('[COPYWRITING] ', '');
      type = 'COPY';
      typeColor = 'text-pink-400 bg-pink-550/10 border-pink-500/20';
    } else if (line.startsWith('[DRAFT]')) {
      cleanLine = line.replace('[DRAFT] ', '');
      type = 'DRAFT';
      typeColor = 'text-accent-violet bg-accent-violet/10 border-accent-violet/20';
    } else if (line.startsWith('[CHANNEL]')) {
      cleanLine = line.replace('[CHANNEL] ', '');
      type = 'CHANNEL';
      typeColor = 'text-accent-cyan bg-accent-cyan/10 border-accent-cyan/20';
    } else if (line.startsWith('[METRICS]')) {
      cleanLine = line.replace('[METRICS] ', '');
      type = 'METRIC';
      typeColor = 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/20';
    } else if (line.startsWith('[ANALYSIS]')) {
      cleanLine = line.replace('[ANALYSIS] ', '');
      type = 'ANALYZE';
      typeColor = 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/20';
    } else if (line.startsWith('[RECOMMENDATION]')) {
      cleanLine = line.replace('[RECOMMENDATION] ', '');
      type = 'RECOM';
      typeColor = 'text-amber-400 bg-amber-900/10 border-amber-800/20';
    } else if (line.startsWith('[SUCCESS]')) {
      cleanLine = line.replace('[SUCCESS] ', '');
      type = 'SUCCESS';
      typeColor = 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/20';
    }

    return { timestamp, type, cleanLine, typeColor };
  };

  return (
    <div className="glass-card rounded-2xl border border-slate-800 flex flex-col h-[480px] shadow-2xl relative overflow-hidden">
      {/* Console Header Bar */}
      <div className="bg-space-950 px-5 py-3 border-b border-slate-800 flex items-center justify-between select-none">
        <div className="flex items-center gap-3">
          {/* OS-style dots */}
          <div className="flex gap-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500/60" />
            <span className="w-3 h-3 rounded-full bg-yellow-500/60" />
            <span className="w-3 h-3 rounded-full bg-green-500/60" />
          </div>
          <span className="h-4 w-[1px] bg-slate-800 mx-1" />
          <div className="flex items-center gap-2 text-xs font-bold text-slate-400">
            <Terminal className="w-4 h-4 text-accent-cyan" />
            <span>GMACHIE Live Console</span>
          </div>
        </div>

        {/* Action: Copy logs */}
        <button
          onClick={copyLogs}
          disabled={logs.length === 0}
          className="text-slate-500 hover:text-slate-300 disabled:opacity-50 p-1.5 rounded-lg hover:bg-slate-900 border border-transparent hover:border-slate-800 transition-all"
          title="Copy console logs"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-accent-emerald" /> : <Copy className="w-3.5 h-3.5" />}
        </button>
      </div>

      {/* Console Log Area */}
      <div ref={scrollContainerRef} className="flex-1 overflow-y-auto p-5 space-y-3 font-mono text-[12px] leading-relaxed bg-[#05070B]/90">
        {logs.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-600 gap-2">
            <Terminal className="w-8 h-8 opacity-20" />
            <span className="italic select-none">Waiting for orchestration cycle to launch...</span>
          </div>
        ) : (
          logs.map((line, idx) => {
            const parsed = parseLogLine(line);
            return (
              <div key={idx} className="flex items-start gap-3.5 animate-slide-up">
                {/* Timestamp */}
                <span className="text-slate-600 select-none shrink-0">{parsed.timestamp}</span>
                {/* Agent Tag */}
                <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md border shrink-0 ${parsed.typeColor}`}>
                  {parsed.type}
                </span>
                {/* Message text */}
                <span className="text-slate-300 whitespace-pre-wrap select-text break-words">
                  {parsed.cleanLine}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
