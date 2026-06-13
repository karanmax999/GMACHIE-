import React, { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Sidebar from '../components/Sidebar';
import { INITIAL_CAMPAIGNS } from '../lib/mockData';
import { Campaign } from '../lib/types';
import { Zap, HelpCircle, Briefcase, Plus, Send, Target, Rocket, Sparkles, Building, Globe } from 'lucide-react';

export default function Home() {
  const router = useRouter();
  const [campaigns, setCampaigns] = useState<Campaign[]>(INITIAL_CAMPAIGNS);
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  // Form fields
  const [name, setName] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [description, setDescription] = useState('');
  const [website, setWebsite] = useState('');
  const [icp, setIcp] = useState('');
  const [goal, setGoal] = useState('');
  const [industry, setIndustry] = useState('');

  const handleSelectCampaign = (id: string) => {
    router.push(`/campaign/${id}`);
  };

  const handleCreateCampaign = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !businessName || !description || !goal) return;

    const newCampaignId = `camp-${Math.random().toString(36).substring(2, 9)}`;
    const newCampaign: Campaign = {
      id: newCampaignId,
      name,
      businessInfo: {
        name: businessName,
        description,
        website,
        industry
      },
      icp,
      goal,
      status: 'draft',
      currentCycle: 0,
      currentPhase: 'idle',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    // Update global state/local mock state
    const updated = [newCampaign, ...campaigns];
    setCampaigns(updated);
    
    // Save to localStorage for simple cross-page persistence in demo
    if (typeof window !== 'undefined') {
      localStorage.setItem('gmachie_campaigns', JSON.stringify(updated));
    }

    // Reset Form
    setName('');
    setBusinessName('');
    setDescription('');
    setWebsite('');
    setIcp('');
    setGoal('');
    setIndustry('');
    setShowCreateModal(false);

    // Navigate to the new campaign cockpit
    router.push(`/campaign/${newCampaignId}`);
  };

  // Fetch campaigns from localStorage if present
  React.useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('gmachie_campaigns');
      if (stored) {
        setCampaigns(JSON.parse(stored));
      }
    }
  }, []);

  return (
    <>
      <Head>
        <title>GMACHIE - Agentic GTM Machine</title>
      </Head>

      <div className="flex h-screen bg-space-950 overflow-hidden text-slate-100 font-sans">
        {/* Left Sidebar */}
        <Sidebar
          campaigns={campaigns}
          selectedCampaignId={null}
          onSelectCampaign={handleSelectCampaign}
          onCreateCampaign={() => setShowCreateModal(true)}
        />

        {/* Main Dashboard Panel */}
        <main className="flex-1 overflow-y-auto bg-space-900/40 p-8 relative flex flex-col justify-between">
          <div className="max-w-6xl mx-auto w-full space-y-8">
            
            {/* Top Row / Welcome banner */}
            <div className="flex items-center justify-between border-b border-slate-800/60 pb-6">
              <div>
                <h2 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-2">
                  <span>Welcome to GMACHIE</span>
                  <Sparkles className="w-6 h-6 text-accent-violet animate-pulse" />
                </h2>
                <p className="text-slate-400 text-sm mt-1">Autonomous Go-To-Market orchestration and multi-channel optimization.</p>
              </div>

              {/* Status Badge */}
              <div className="flex items-center gap-4 text-xs font-bold text-slate-400">
                <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-space-950 border border-slate-850">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent-emerald animate-pulse" />
                  Orchestrator Idle
                </span>
              </div>
            </div>

            {/* Quick Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 select-none">
              <div className="glass-card rounded-2xl p-6 border border-slate-800/80">
                <div className="text-slate-500 text-xs font-bold uppercase tracking-wider">Total Campaigns</div>
                <div className="text-4xl font-black text-white mt-2 tracking-tight">{campaigns.length}</div>
                <div className="text-[10px] text-slate-500 font-medium mt-1">Active distribution programs</div>
              </div>
              <div className="glass-card rounded-2xl p-6 border border-slate-800/80">
                <div className="text-slate-500 text-xs font-bold uppercase tracking-wider">Reach Generated</div>
                <div className="text-4xl font-black text-accent-indigo mt-2 tracking-tight">36.7K</div>
                <div className="text-[10px] text-slate-500 font-medium mt-1">Total social & email impressions</div>
              </div>
              <div className="glass-card rounded-2xl p-6 border border-slate-800/80">
                <div className="text-slate-500 text-xs font-bold uppercase tracking-wider">User Signups</div>
                <div className="text-4xl font-black text-accent-emerald mt-2 tracking-tight">272</div>
                <div className="text-[10px] text-slate-500 font-medium mt-1">Conversions driven by agents</div>
              </div>
            </div>

            {/* Main Content Split: Overview / CTA */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
              {/* Left Column: System guide */}
              <div className="lg:col-span-3 space-y-6">
                <div className="glass-card rounded-2xl p-6 border border-slate-800/80">
                  <h3 className="text-lg font-bold text-white mb-4 tracking-tight flex items-center gap-2">
                    <Rocket className="w-5 h-5 text-accent-cyan" />
                    <span>How GMACHIE Drives Growth</span>
                  </h3>
                  <div className="space-y-4 text-sm text-slate-400">
                    <div className="flex gap-3">
                      <div className="text-xs bg-slate-900 border border-slate-800 w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-slate-300 font-bold">1</div>
                      <p><strong>Input context:</strong> Provide your SaaS details, ICP definitions, and specific campaign targets (e.g. 500 signups).</p>
                    </div>
                    <div className="flex gap-3">
                      <div className="text-xs bg-slate-900 border border-slate-800 w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-slate-300 font-bold">2</div>
                      <p><strong>Strategy & Research:</strong> AI Strategist maps messaging pillars, while the Research Agent analyzes competitors and maps buyer personas.</p>
                    </div>
                    <div className="flex gap-3">
                      <div className="text-xs bg-slate-900 border border-slate-800 w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-slate-300 font-bold">3</div>
                      <p><strong>Copywriting & Execution:</strong> Content Agent drafts social posts and outreach email variants. Channel Agents simulate publishing instantly.</p>
                    </div>
                    <div className="flex gap-3">
                      <div className="text-xs bg-slate-900 border border-slate-800 w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-slate-300 font-bold">4</div>
                      <p><strong>Analytics Loop:</strong> Performance data is monitored by the Analytics Agent. Insights are fed back to automatically refine copy and targeting for the next cycle.</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Active programs */}
              <div className="lg:col-span-2 space-y-6">
                <div className="glass-card rounded-2xl p-6 border border-slate-800/80 flex flex-col justify-between h-full min-h-[300px]">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-3 tracking-tight">Setup a New Campaign</h3>
                    <p className="text-xs text-slate-400 leading-relaxed mb-6">
                      Launch an autonomous go-to-market loop. Let our specialized agents research your target audience, compose posts, and drive conversions.
                    </p>
                  </div>
                  <button
                    onClick={() => setShowCreateModal(true)}
                    className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-accent-indigo to-accent-violet hover:from-accent-indigo/90 hover:to-accent-violet/90 text-white font-bold text-sm shadow-lg shadow-accent-indigo/10 flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.99] transition-all"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Create Campaign Configuration</span>
                  </button>
                </div>
              </div>
            </div>

          </div>

          <footer className="text-center text-slate-600 text-xs py-8 mt-12 border-t border-slate-850 max-w-6xl mx-auto w-full">
            GMACHIE • Built for B2B SME Go-To-Market Automation. Powered by AI Agents.
          </footer>
        </main>

        {/* Campaign Creation Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-md animate-fade-in">
            <div 
              className="glass-card w-full max-w-2xl rounded-2xl border border-slate-800 shadow-2xl overflow-hidden animate-slide-up flex flex-col max-h-[90vh]"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="px-6 py-4 bg-space-950 border-b border-slate-850 flex items-center justify-between">
                <h3 className="text-xl font-extrabold text-white flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-accent-indigo" />
                  <span>Configure GTM Program</span>
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-slate-500 hover:text-slate-350 text-sm font-bold p-1 hover:bg-slate-900 rounded-lg"
                >
                  Cancel
                </button>
              </div>

              {/* Form Body */}
              <form onSubmit={handleCreateCampaign} className="p-6 overflow-y-auto space-y-5 flex-1 text-sm">
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Campaign Name</label>
                    <input
                      type="text"
                      placeholder="e.g. FinSmart GST Launch"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Company/Product Name</label>
                    <input
                      type="text"
                      placeholder="e.g. FinSmart"
                      value={businessName}
                      onChange={(e) => setBusinessName(e.target.value)}
                      className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Industry Sector</label>
                    <input
                      type="text"
                      placeholder="e.g. B2B FinTech SaaS"
                      value={industry}
                      onChange={(e) => setIndustry(e.target.value)}
                      className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Product Website</label>
                    <input
                      type="url"
                      placeholder="https://example.com"
                      value={website}
                      onChange={(e) => setWebsite(e.target.value)}
                      className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Product Description & Core Value Prop</label>
                  <textarea
                    placeholder="What does your product do, what pain does it solve, and how does it integrate?"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200 resize-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Ideal Customer Profile (ICP)</label>
                  <textarea
                    placeholder="Who is your target buyer? (e.g. Small retail merchants in tier-2 cities using Tally for book-keeping)"
                    value={icp}
                    onChange={(e) => setIcp(e.target.value)}
                    rows={2}
                    className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200 resize-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">GTM Campaign Goal</label>
                  <input
                    type="text"
                    placeholder="e.g. Achieve 500 platform registrations and 50k impressions on Twitter & LinkedIn in 2 weeks"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    className="w-full px-4 py-2.5 bg-space-950 border border-slate-800 rounded-xl focus:outline-none focus:border-accent-indigo text-slate-200"
                    required
                  />
                </div>

                {/* Submit button */}
                <div className="pt-4 border-t border-slate-850 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-5 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-900 text-slate-400 font-bold transition-all text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-accent-indigo to-accent-violet hover:from-accent-indigo/90 hover:to-accent-violet/90 text-white font-bold transition-all text-xs flex items-center gap-1.5 shadow-md shadow-accent-indigo/15"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>Launch Campaign Cockpit</span>
                  </button>
                </div>

              </form>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
