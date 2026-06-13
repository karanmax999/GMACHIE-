import React from 'react';
import { Shield, Settings, Users, PenTool, Radio, BarChart3, RefreshCw, Check } from 'lucide-react';

interface AgentPipelineProps {
  currentPhase: 'idle' | 'strategy' | 'research' | 'content' | 'executing' | 'analytics' | 'adapting';
}

const PHASES = [
  { id: 'strategy', label: 'Strategy', desc: 'Campaign Plan & Targets', icon: Settings },
  { id: 'research', label: 'Research', desc: 'Audience & Competitors', icon: Users },
  { id: 'content', label: 'Content', desc: 'Copywriting & Variations', icon: PenTool },
  { id: 'executing', label: 'Channels', desc: 'Publishing & Reaching', icon: Radio },
  { id: 'analytics', label: 'Analytics', desc: 'Metrics & Performance', icon: BarChart3 },
];

export default function AgentPipeline({ currentPhase }: AgentPipelineProps) {
  const getPhaseIndex = (phase: string) => {
    return PHASES.findIndex((p) => p.id === phase);
  };

  const currentIndex = getPhaseIndex(currentPhase);

  return (
    <div className="glass-card rounded-2xl p-6 shadow-xl relative overflow-hidden">
      {/* Background Decorative Blur */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-20 bg-accent-indigo/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="flex flex-col md:flex-row items-center justify-between gap-6 md:gap-4 relative z-10">
        {PHASES.map((p, idx) => {
          const Icon = p.icon;
          const isCompleted = idx < currentIndex || currentPhase === 'adapting';
          const isActive = currentPhase === p.id;
          const isPending = idx > currentIndex && currentPhase !== 'adapting';

          return (
            <React.Fragment key={p.id}>
              {/* Node Card */}
              <div className="flex flex-col items-center flex-1 text-center group relative w-full md:w-auto">
                <div
                  className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                    isActive
                      ? 'bg-space-950 border-2 border-accent-cyan text-accent-cyan shadow-[0_0_20px_rgba(6,182,212,0.3)] scale-110 animate-pulse-glow'
                      : isCompleted
                      ? 'bg-accent-emerald/10 border-2 border-accent-emerald text-accent-emerald'
                      : 'bg-space-900 border border-slate-800 text-slate-500'
                  }`}
                >
                  {isCompleted ? (
                    <Check className="w-6 h-6 stroke-[3]" />
                  ) : isActive && currentPhase === 'executing' ? (
                    <Radio className="w-6 h-6 animate-pulse" />
                  ) : (
                    <Icon className={`w-6 h-6 ${isActive ? 'animate-bounce' : ''}`} />
                  )}
                </div>

                <div className="mt-3">
                  <div
                    className={`text-sm font-bold tracking-wide transition-colors ${
                      isActive ? 'text-accent-cyan' : isCompleted ? 'text-accent-emerald' : 'text-slate-400'
                    }`}
                  >
                    {p.label}
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5 max-w-[120px] mx-auto leading-relaxed font-medium">
                    {p.desc}
                  </div>
                </div>

                {/* Status indicator underneath */}
                {isActive && (
                  <span className="absolute -bottom-4 text-[9px] font-extrabold uppercase tracking-widest text-accent-cyan bg-accent-cyan/10 py-0.5 px-2 rounded-full border border-accent-cyan/20">
                    Active
                  </span>
                )}
              </div>

              {/* Connecting Line (Only draw if not the last item) */}
              {idx < PHASES.length - 1 && (
                <div className="hidden md:block h-[2px] flex-1 bg-slate-800 relative mx-2">
                  <div
                    className={`absolute inset-0 transition-all duration-700 ${
                      isCompleted 
                        ? 'bg-accent-emerald' 
                        : isActive 
                        ? 'bg-gradient-to-r from-accent-cyan to-slate-800 w-1/2 animate-pulse'
                        : 'w-0'
                    }`}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}

        {/* Adapting Phase Overlay Banner (Shows up when phase is 'adapting') */}
        {currentPhase === 'adapting' && (
          <div className="absolute inset-0 bg-space-950/80 backdrop-blur-sm flex items-center justify-center gap-3 animate-fade-in">
            <RefreshCw className="w-6 h-6 text-accent-violet animate-spin" />
            <span className="font-extrabold text-accent-violet tracking-wide uppercase text-sm">
              Analytics Agent Re-Calibrating & Adapting Campaign Strategy...
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
