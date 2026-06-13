import React from 'react';
import { Eye, ArrowUpRight, UserCheck, Percent, HelpCircle } from 'lucide-react';

interface MetricsPanelProps {
  metrics: {
    impressions: number;
    clicks: number;
    signups: number;
    ctr: number;
  };
}

export default function MetricsPanel({ metrics }: MetricsPanelProps) {
  // Sparkline data points to render smooth mini SVG trend charts
  const sparklineData = {
    impressions: "M0,25 Q15,10 30,22 T60,8 T90,28 T120,4",
    clicks: "M0,28 Q15,22 30,12 T60,25 T90,10 T120,6",
    signups: "M0,28 Q15,24 30,26 T60,18 T90,8 T120,4",
    ctr: "M0,20 Q15,28 30,14 T60,22 T90,8 T120,5",
  };

  return (
    <div className="space-y-4 select-none">
      <h3 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
        <span>Performance Analytics</span>
      </h3>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric Card: Impressions */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex flex-col justify-between h-40 relative group overflow-hidden">
          <div className="absolute -right-3 -top-3 w-16 h-16 bg-slate-850 rounded-full blur-[10px] opacity-10 group-hover:scale-125 transition-transform duration-300 pointer-events-none" />
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Impressions</span>
            <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400">
              <Eye className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-white tracking-tight">
              {metrics.impressions.toLocaleString()}
            </div>
            <div className="flex items-center gap-1 text-[10px] text-accent-emerald font-extrabold mt-1">
              <span>+18.2%</span>
              <span className="text-slate-500 font-medium">vs target</span>
            </div>
          </div>
          {/* Sparkline chart */}
          <div className="h-8 mt-2 w-full">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none">
              <path
                d={sparklineData.impressions}
                fill="none"
                stroke="#6366F1"
                strokeWidth="2"
                strokeLinecap="round"
                className="opacity-70"
              />
            </svg>
          </div>
        </div>

        {/* Metric Card: Clicks */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex flex-col justify-between h-40 relative group overflow-hidden">
          <div className="absolute -right-3 -top-3 w-16 h-16 bg-slate-850 rounded-full blur-[10px] opacity-10 group-hover:scale-125 transition-transform duration-300 pointer-events-none" />
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Link Clicks</span>
            <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-accent-cyan">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-white tracking-tight">
              {metrics.clicks.toLocaleString()}
            </div>
            <div className="flex items-center gap-1 text-[10px] text-accent-emerald font-extrabold mt-1">
              <span>+14.5%</span>
              <span className="text-slate-500 font-medium">vs target</span>
            </div>
          </div>
          {/* Sparkline chart */}
          <div className="h-8 mt-2 w-full">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none">
              <path
                d={sparklineData.clicks}
                fill="none"
                stroke="#06B6D4"
                strokeWidth="2"
                strokeLinecap="round"
                className="opacity-70"
              />
            </svg>
          </div>
        </div>

        {/* Metric Card: Signups */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex flex-col justify-between h-40 relative group overflow-hidden">
          <div className="absolute -right-3 -top-3 w-16 h-16 bg-slate-850 rounded-full blur-[10px] opacity-10 group-hover:scale-125 transition-transform duration-300 pointer-events-none" />
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Signups</span>
            <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-accent-emerald">
              <UserCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-white tracking-tight">
              {metrics.signups.toLocaleString()}
            </div>
            <div className="flex items-center gap-1 text-[10px] text-accent-emerald font-extrabold mt-1">
              <span>+22.7%</span>
              <span className="text-slate-500 font-medium">vs target</span>
            </div>
          </div>
          {/* Sparkline chart */}
          <div className="h-8 mt-2 w-full">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none">
              <path
                d={sparklineData.signups}
                fill="none"
                stroke="#10B981"
                strokeWidth="2"
                strokeLinecap="round"
                className="opacity-70"
              />
            </svg>
          </div>
        </div>

        {/* Metric Card: CTR */}
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex flex-col justify-between h-40 relative group overflow-hidden">
          <div className="absolute -right-3 -top-3 w-16 h-16 bg-slate-850 rounded-full blur-[10px] opacity-10 group-hover:scale-125 transition-transform duration-300 pointer-events-none" />
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Click Rate</span>
            <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-accent-violet">
              <Percent className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <div className="text-2xl font-black text-white tracking-tight">
              {metrics.ctr.toFixed(2)}%
            </div>
            <div className="flex items-center gap-1 text-[10px] text-accent-emerald font-extrabold mt-1">
              <span>+9.3%</span>
              <span className="text-slate-500 font-medium">vs target</span>
            </div>
          </div>
          {/* Sparkline chart */}
          <div className="h-8 mt-2 w-full">
            <svg className="w-full h-full overflow-visible" preserveAspectRatio="none">
              <path
                d={sparklineData.ctr}
                fill="none"
                stroke="#8B5CF6"
                strokeWidth="2"
                strokeLinecap="round"
                className="opacity-70"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
