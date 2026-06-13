import React from 'react';
import { Campaign } from '../lib/types';
import { Plus, Briefcase, Zap, Database, Cpu, Network } from 'lucide-react';

interface SidebarProps {
  campaigns: Campaign[];
  selectedCampaignId: string | null;
  onSelectCampaign: (id: string) => void;
  onCreateCampaign: () => void;
}

export default function Sidebar({
  campaigns,
  selectedCampaignId,
  onSelectCampaign,
  onCreateCampaign,
}: SidebarProps) {
  return (
    <aside className="w-72 bg-space-950 border-r border-slate-800 flex flex-col h-screen select-none">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <div className="bg-gradient-to-tr from-accent-indigo to-accent-cyan p-2.5 rounded-xl shadow-lg shadow-accent-indigo/20">
          <Network className="w-6 h-6 text-space-950 stroke-[2.5]" />
        </div>
        <div>
          <h1 className="font-extrabold text-xl tracking-tight text-neon-gradient">GMACHIE</h1>
          <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">Agentic GTM Machine</p>
        </div>
      </div>

      {/* Action: Create Campaign */}
      <div className="p-4">
        <button
          onClick={onCreateCampaign}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-gradient-to-r from-accent-indigo to-accent-violet hover:from-accent-indigo/90 hover:to-accent-violet/90 text-white font-semibold shadow-lg shadow-accent-indigo/15 hover:shadow-accent-indigo/25 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 text-sm"
        >
          <Plus className="w-4 h-4" />
          <span>New Campaign</span>
        </button>
      </div>

      {/* Navigation list */}
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-1.5">
        <div className="text-[10px] uppercase font-bold text-slate-500 tracking-wider px-2 mb-2">Active Campaigns</div>
        {campaigns.length === 0 ? (
          <div className="text-xs text-slate-500 italic p-3 text-center border border-dashed border-slate-800 rounded-lg">
            No campaigns created yet.
          </div>
        ) : (
          campaigns.map((c) => {
            const isActive = c.id === selectedCampaignId;
            return (
              <button
                key={c.id}
                onClick={() => onSelectCampaign(c.id)}
                className={`w-full text-left p-3 rounded-xl flex items-start gap-3 transition-all duration-200 group ${
                  isActive
                    ? 'bg-space-800 border border-slate-700/60 shadow-inner'
                    : 'hover:bg-space-900/40 border border-transparent'
                }`}
              >
                <div
                  className={`p-2 rounded-lg mt-0.5 transition-colors ${
                    isActive ? 'bg-accent-indigo/25 text-accent-indigo' : 'bg-slate-800 text-slate-500 group-hover:text-slate-400'
                  }`}
                >
                  <Briefcase className="w-4 h-4" />
                </div>
                <div className="min-w-0">
                  <div className={`text-sm font-semibold truncate ${isActive ? 'text-white' : 'text-slate-300 group-hover:text-white'}`}>
                    {c.name}
                  </div>
                  <div className="text-[11px] text-slate-500 truncate mt-0.5">
                    {(c.businessInfo?.name || 'Unknown')} • Cycle {c.currentCycle}
                  </div>
                </div>
                {c.status === 'running' && (
                  <span className="ml-auto w-2 h-2 rounded-full bg-accent-cyan animate-pulse mt-2 shadow-[0_0_8px_#06B6D4]" />
                )}
              </button>
            );
          })
        )}
      </div>

      {/* System Health Badges Footer */}
      <div className="p-4 border-t border-slate-800 bg-space-900/30 space-y-2">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5 font-medium">
            <Cpu className="w-3.5 h-3.5 text-accent-cyan" />
            <span>Orchestrator</span>
          </span>
          <span className="font-semibold text-accent-cyan flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-cyan animate-ping" />
            ONLINE
          </span>
        </div>
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5 font-medium">
            <Database className="w-3.5 h-3.5 text-accent-indigo" />
            <span>Convex Sync</span>
          </span>
          <span className="font-semibold text-slate-400">SYNCED</span>
        </div>
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5 font-medium">
            <Zap className="w-3.5 h-3.5 text-accent-violet" />
            <span>Demo Engine</span>
          </span>
          <span className="font-semibold text-slate-400">READY</span>
        </div>
      </div>
    </aside>
  );
}
