import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Sidebar from '../../components/Sidebar';
import AgentPipeline from '../../components/AgentPipeline';
import AgentLog from '../../components/AgentLog';
import ContentMatrix from '../../components/ContentMatrix';
import MetricsPanel from '../../components/MetricsPanel';
import { INITIAL_CAMPAIGNS, MOCK_CONTENT, MOCK_AGENT_LOGS } from '../../lib/mockData';
import { Campaign, ContentItem } from '../../lib/types';
import { Play, RotateCcw, AlertTriangle, ArrowLeft, CheckCircle, HelpCircle } from 'lucide-react';

export default function CampaignCockpit() {
  const router = useRouter();
  const { id } = router.query;

  const [campaigns, setCampaigns] = useState<Campaign[]>(INITIAL_CAMPAIGNS);
  const [currentCampaign, setCurrentCampaign] = useState<Campaign | null>(null);
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [runningLogs, setRunningLogs] = useState<string[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);

  // Load campaigns & content from localStorage or fallback to defaults
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedCamp = localStorage.getItem('gmachie_campaigns');
      const storedContent = localStorage.getItem('gmachie_content');
      
      const loadedCamp = storedCamp ? JSON.parse(storedCamp) : INITIAL_CAMPAIGNS;
      setCampaigns(loadedCamp);

      if (id) {
        const found = loadedCamp.find((c: Campaign) => c.id === id);
        if (found) {
          setCurrentCampaign(found);
          // Only load mock content if the campaign has run before (cycle > 0)
          if (found.currentCycle > 0) {
            const defaultContent = MOCK_CONTENT.filter(c => c.campaignId === id);
            const loadedContent = storedContent ? JSON.parse(storedContent) : defaultContent;
            setContentItems(loadedContent);
          } else {
            setContentItems([]);
          }
        }
      }
    }
  }, [id]);

  const handleSelectCampaign = (campId: string) => {
    router.push(`/campaign/${campId}`);
  };

  const handleCreateNew = () => {
    router.push('/');
  };

  const updateCampaignState = (updatedCamp: Campaign) => {
    setCurrentCampaign(updatedCamp);
    const updatedList = campaigns.map((c) => (c.id === updatedCamp.id ? updatedCamp : c));
    setCampaigns(updatedList);
    if (typeof window !== 'undefined') {
      localStorage.setItem('gmachie_campaigns', JSON.stringify(updatedList));
    }
  };

  // Helper to wait
  const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  // Run the multi-agent GTM simulation loop
  const handleLaunchSimulation = async () => {
    if (!currentCampaign || isSimulating) return;

    setIsSimulating(true);
    setRunningLogs([]);
    setContentItems([]);

    const camp = { ...currentCampaign };
    camp.status = 'running';
    updateCampaignState(camp);

    // --- PHASE 1: STRATEGY ---
    camp.currentPhase = 'strategy';
    updateCampaignState(camp);
    for (const logLine of MOCK_AGENT_LOGS.strategy) {
      setRunningLogs((prev) => [...prev, `[STRATEGY] ${logLine}`]);
      await delay(600);
    }
    
    // Set mock GTM plan strategy in state
    camp.gtmPlan = {
      positioning: `Claiming top value proposition for ${camp.name}: Automating and accelerating operations by 10x.`,
      target_audience: camp.icp || "General B2B SaaS SME Audience",
      channels: [
        { name: "Twitter/X", primary: true, why: "Tech community reach.", expected_reach: "15,000" },
        { name: "LinkedIn", primary: true, why: "B2B professional engagement.", expected_reach: "25,000" },
        { name: "Email", primary: true, why: "Direct outreach lists.", expected_reach: "10,000" }
      ],
      campaign_themes: ["Automation", "Direct Sync", "Compliance Freedom"],
      kpi_targets: {
        "week1": { impressions: 20000, clicks: 800, signups: 150 },
        "week2": { impressions: 30000, clicks: 1200, signups: 350 }
      },
      north_star_metric: "Conversions"
    };
    updateCampaignState(camp);
    await delay(500);

    // --- PHASE 2: RESEARCH ---
    camp.currentPhase = 'research';
    updateCampaignState(camp);
    for (const logLine of MOCK_AGENT_LOGS.research) {
      setRunningLogs((prev) => [...prev, `[RESEARCH] ${logLine}`]);
      await delay(700);
    }
    
    // Set mock Research Insights
    camp.researchInsights = {
      personas: [
        {
          name: "SME Manager (Tech Conservative)",
          description: `Demographics matching ${camp.name}'s target audience. Needs simple user interfaces.`,
          pain_points: ["Manual errors", "Compliance risk", "Time drain"],
          triggers: ["Automated dashboards", "WhatsApp reports"],
          objections: ["High setup cost", "Cloud security"],
          language: ["#SMEIndia", "#BusinessAutomation"]
        }
      ],
      competitor_insights: [
        { competitor: "Legacy Manual Flow", strategy: "Rule-based macros", strengths: ["Familiarity"], weaknesses: ["Fragility", "Manual sync needed"], opportunity: "Fully autonomous agents" }
      ],
      trending_topics: [{ topic: "SaaS growth strategies 2026", relevance: "High", hashtags: ["#SaaSGrowth", "#Automation"] }],
      recommended_keywords: ["Automated workflow", "SME scaling", "Cloud Sync"],
      content_gaps: ["No competitor offers 1-click execution reports."]
    };
    updateCampaignState(camp);
    await delay(500);

    // --- PHASE 3: CONTENT ---
    camp.currentPhase = 'content';
    updateCampaignState(camp);
    for (const logLine of MOCK_AGENT_LOGS.content) {
      setRunningLogs((prev) => [...prev, `[CONTENT] ${logLine}`]);
      await delay(600);
    }
    
    // Generate the content items
    const generatedContent: ContentItem[] = [
      {
        id: `content-x-${camp.id}`,
        campaignId: camp.id,
        channel: 'x',
        type: 'post',
        body: `Still running manual GTM campaigns for ${camp.businessInfo.name}? 🤯\n\nTraditional systems are rule-based and fragment your messaging.\n\nMeet GMACHIE, our agentic campaign copilot that plans, creates, and optimizes distribution in 1 click.\n\n👉 gmachie.ai/demo\n\n#GTM #Automation #SaaS #Growth`,
        status: 'generated',
        createdAt: new Date().toISOString()
      },
      {
        id: `content-li-${camp.id}`,
        campaignId: camp.id,
        channel: 'linkedin',
        type: 'post',
        body: `How is your team scaling its B2B distribution? \n\nModern marketers spend 60% of their time copying, scheduling, and editing templates. \n\nWith GMACHIE's multi-agent loop, Strategy, Research, and Content agents run goal-driven campaigns and adapt strategy based on live performance metrics.\n\nClaim your free GTM audit:\n\n👉 gmachie.ai/audit\n\n#GoToMarket #AgenticAI #B2BMarketing #SaaSGrowth`,
        status: 'generated',
        createdAt: new Date().toISOString()
      },
      {
        id: `content-em-${camp.id}`,
        campaignId: camp.id,
        channel: 'email',
        type: 'email',
        title: `Automate your B2B Go-To-Market distribution with AI Agents`,
        body: `Dear Growth Leader,\n\nAre you still manually managing B2B campaign execution across social media, email, and landing pages?\n\nRule-based marketing automation fails to adapt. FinSmart integrates GMACHIE's agentic loop to continuously test copy, monitor conversions, and shift reach strategies.\n\nSchedule a 10-minute demo to see it in action.\n\nBest regards,\nTeam GMACHIE`,
        status: 'generated',
        createdAt: new Date().toISOString()
      }
    ];
    setContentItems(generatedContent);
    await delay(500);

    // --- PHASE 4: EXECUTING ---
    camp.currentPhase = 'executing';
    updateCampaignState(camp);
    for (const logLine of MOCK_AGENT_LOGS.executing) {
      setRunningLogs((prev) => [...prev, `[EXECUTION] ${logLine}`]);
      await delay(700);
    }
    
    // Mark content items as published
    const publishedContent = generatedContent.map((item) => ({
      ...item,
      status: (item.channel === 'email' ? 'scheduled' : 'published') as any,
      publishedAt: item.channel !== 'email' ? new Date().toISOString() : undefined,
      scheduledAt: item.channel === 'email' ? new Date(Date.now() + 3600000 * 24).toISOString() : undefined,
      metrics: item.channel !== 'email' ? {
        impressions: item.channel === 'x' ? 14200 : 25800,
        clicks: item.channel === 'x' ? 490 : 920,
        likes: item.channel === 'x' ? 192 : 340,
        replies: item.channel === 'x' ? 12 : 28,
        signups: item.channel === 'x' ? 82 : 204
      } : undefined
    }));
    setContentItems(publishedContent);
    if (typeof window !== 'undefined') {
      localStorage.setItem('gmachie_content', JSON.stringify(publishedContent));
    }
    await delay(500);

    // --- PHASE 5: ANALYTICS ---
    camp.currentPhase = 'analytics';
    updateCampaignState(camp);
    for (const logLine of MOCK_AGENT_LOGS.analytics) {
      setRunningLogs((prev) => [...prev, `[ANALYTICS] ${logLine}`]);
      await delay(800);
    }
    await delay(500);

    // --- PHASE 6: ADAPTING ---
    camp.currentPhase = 'adapting';
    updateCampaignState(camp);
    await delay(2500);

    // --- FINALIZE CYCLE ---
    camp.status = 'completed';
    camp.currentPhase = 'idle';
    camp.currentCycle += 1;
    camp.updatedAt = new Date().toISOString();
    updateCampaignState(camp);

    setIsSimulating(false);
  };

  const handleUpdateContentBody = (contentId: string, newBody: string) => {
    const updated = contentItems.map((item) => (item.id === contentId ? { ...item, body: newBody } : item));
    setContentItems(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('gmachie_content', JSON.stringify(updated));
    }
  };

  // Safe defaults for metrics
  const getAggregatedMetrics = () => {
    let impressions = 0;
    let clicks = 0;
    let signups = 0;

    contentItems.forEach((item) => {
      if (item.metrics) {
        impressions += item.metrics.impressions || 0;
        clicks += item.metrics.clicks || 0;
        signups += item.metrics.signups || 0;
      }
    });

    // Fallback if no content runs have metrics yet
    if (impressions === 0 && currentCampaign && currentCampaign.currentCycle > 0) {
      return { impressions: 36700, clicks: 1300, signups: 272, ctr: 3.54 };
    }

    const ctr = impressions > 0 ? (clicks / impressions) * 100 : 0;
    return { impressions, clicks, signups, ctr };
  };

  const metricsSummary = getAggregatedMetrics();

  if (!currentCampaign) {
    return (
      <div className="h-screen bg-space-950 flex flex-col items-center justify-center text-slate-400 gap-4">
        <AlertTriangle className="w-12 h-12 text-accent-violet animate-bounce" />
        <span className="font-bold tracking-wide">Loading Campaign Workspace...</span>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{currentCampaign.name} | GMACHIE Cockpit</title>
      </Head>

      <div className="flex h-screen bg-space-950 overflow-hidden text-slate-100 font-sans">
        {/* Left Sidebar */}
        <Sidebar
          campaigns={campaigns}
          selectedCampaignId={currentCampaign.id}
          onSelectCampaign={handleSelectCampaign}
          onCreateCampaign={handleCreateNew}
        />

        {/* Campaign Workspace */}
        <main className="flex-1 overflow-y-auto bg-space-900/40 p-8 flex flex-col justify-between">
          <div className="max-w-6xl mx-auto w-full space-y-6">
            
            {/* Header section */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800/60 pb-6">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => router.push('/')}
                  className="p-2.5 rounded-xl border border-slate-800 bg-space-950 hover:bg-slate-900 text-slate-500 hover:text-slate-350 transition-colors"
                >
                  <ArrowLeft className="w-4 h-4" />
                </button>
                <div>
                  <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
                    <span>{currentCampaign.name}</span>
                    <span className="text-xs bg-accent-indigo/10 border border-accent-indigo/25 text-accent-indigo px-3 py-0.5 rounded-full font-bold select-none">
                      Cycle {currentCampaign.currentCycle}
                    </span>
                  </h2>
                  <p className="text-xs text-slate-400 mt-1">
                    ICP: <span className="font-semibold text-slate-300">{currentCampaign.icp || "Not defined"}</span>
                  </p>
                </div>
              </div>

              {/* Trigger orchestration button */}
              <button
                onClick={handleLaunchSimulation}
                disabled={isSimulating}
                className="flex items-center gap-2 py-3 px-5 rounded-xl bg-gradient-to-r from-accent-cyan via-accent-indigo to-accent-violet hover:brightness-110 disabled:opacity-50 text-white font-bold text-sm shadow-xl shadow-accent-indigo/15 hover:scale-[1.02] active:scale-[0.98] transition-all self-stretch sm:self-auto justify-center"
              >
                {isSimulating ? (
                  <>
                    <span className="w-2 h-2 rounded-full bg-white animate-ping" />
                    <span>Running Agents...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 text-white fill-white" />
                    <span>Launch Orchestration Cycle</span>
                  </>
                )}
              </button>
            </div>

            {/* Stage Pipeline Banner */}
            <AgentPipeline currentPhase={currentCampaign.currentPhase} />

            {/* Split Screen Dashboard Area */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              
              {/* Left Column: Log Telemetry terminal */}
              <div className="lg:col-span-5 h-full">
                <AgentLog logs={runningLogs} />
              </div>

              {/* Right Column: Content Cards & Metrics */}
              <div className="lg:col-span-7 space-y-6">
                
                {/* Visual statistics */}
                <MetricsPanel metrics={metricsSummary} />

                {/* Social generated text matrix */}
                <ContentMatrix
                  contentItems={contentItems}
                  onUpdateContentBody={handleUpdateContentBody}
                />
              </div>

            </div>

          </div>

          <footer className="text-center text-slate-600 text-xs py-8 mt-12 border-t border-slate-850 max-w-6xl mx-auto w-full">
            GMACHIE • Built for B2B SME Go-To-Market Automation. Powered by AI Agents.
          </footer>
        </main>
      </div>
    </>
  );
}
