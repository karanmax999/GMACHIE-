import { Campaign, ContentItem, AgentRun } from './types';

export const INITIAL_CAMPAIGNS: Campaign[] = [
  {
    id: "finsmart-gtm",
    name: "FinSmart India Launch",
    businessInfo: {
      name: "FinSmart",
      description: "Automated tax preparation and GST compliance software for Indian small business owners using Tally ERP.",
      industry: "Fintech / SaaS",
      website: "https://finsmart.in"
    },
    icp: "Indian small business owners, traders, and CA firms who manually reconcile GST and use Tally.",
    goal: "Acquire 500 signups and reach 50k impressions on socials in 2 weeks.",
    status: "completed",
    currentCycle: 1,
    currentPhase: "idle",
    createdAt: new Date(Date.now() - 3600000 * 24 * 7).toISOString(), // 7 days ago
    updatedAt: new Date().toISOString(),
    gtmPlan: {
      positioning: "Unlocking seamless compliance: Reconcile Tally sales with GST portal in 1 click, saving 15 hours every month.",
      target_audience: "Tech-wary Indian merchants, Kirana chains, and independent Chartered Accountants.",
      channels: [
        { name: "Twitter/X", primary: true, why: "Active community of startup founders, tech-savvy CAs, and business influencers.", expected_reach: "15,000 impressions" },
        { name: "LinkedIn", primary: true, why: "B2B reach targeting financial advisors, mid-sized business directors, and enterprise finance heads.", expected_reach: "25,000 impressions" },
        { name: "Email", primary: true, why: "High conversion channel for cold outreach targeting CA lists and registered merchants.", expected_reach: "10,000 send list" }
      ],
      campaign_themes: ["GST Freedom", "Error-Free Filings", "Tally Integration"],
      kpi_targets: {
        "week1": { impressions: 20000, clicks: 800, signups: 150 },
        "week2": { impressions: 30000, clicks: 1200, signups: 350 }
      },
      north_star_metric: "Tally GST signups"
    },
    researchInsights: {
      personas: [
        {
          name: "Ramesh Sharma (Kirana Owner)",
          description: "Owner of a retail provisions network in Noida. Spends weekends sorting bills for his accountant.",
          pain_points: ["Double taxation errors", "Manual data entry mismatch", "Fear of GST department notices"],
          triggers: ["Simple WhatsApp-like mobile updates", "Auto-reconciliation", "Clear vernacular support"],
          objections: ["Tally is too complex to connect", "Fear of cloud data privacy"],
          language: ["#GSTMadeEasy", "#TallyReconciliation", "Dhanda", "Simple Tax", "#KiranaBusiness"]
        },
        {
          name: "CA Neha Gupta (Independent Accountant)",
          description: "Handles accounting for 30+ SME clients. Bottlenecked during tax season due to clients delayed uploads.",
          pain_points: ["Client cooperation delay", "Format errors in raw spreadsheets", "TDS/GST cross check time"],
          triggers: ["Multi-client dashboard", "Automated email reminders to clients", "Tally direct export sync"],
          objections: ["Software cost absorption", "Learning curve for her staff"],
          language: ["#CharteredAccountant", "#TaxSeason", "#CAOffice", "InputTaxCredit", "ITC Reconcile"]
        }
      ],
      competitor_insights: [
        {
          competitor: "Clear (formerly ClearTax)",
          strategy: "Large enterprise focus, high subscription pricing, broad feature list.",
          strengths: ["Strong brand awareness", "Robust desktop client"],
          weaknesses: ["Too complex for tiny merchants", "Poor native integration with old Tally versions"],
          opportunity: "Offer lightweight, 1-click mobile-friendly integration tailored for Tally desktop clients."
        },
        {
          competitor: "Vyapar",
          strategy: "Billing app focused on mobile-first accounting.",
          strengths: ["Easy invoicing", "Offline support"],
          weaknesses: ["Lack of advanced automated compliance analytics", "Doesn't support deep Tally sync"],
          opportunity: "Target businesses who already use Tally but need heavy GST automation."
        }
      ],
      trending_topics: [
        { topic: "GST Council Decisions on Rate Revisions", relevance: "High urgency, businesses need immediate updates", hashtags: ["#GSTCouncil", "#TaxUpdate"] },
        { topic: "Tally Prime Upgrades", relevance: "Direct alignment, users looking for tutorials", hashtags: ["#TallyPrime", "#AccountingTutorial"] }
      ],
      recommended_keywords: ["GST Reconciliation", "Tally Integration", "Input Tax Credit Calculator", "GST Refund", "GSTR-2B Automation"],
      content_gaps: ["No competitor simplifies GSTR-2B vs Tally mismatches under 2 minutes.", "Lack of video tutorials explaining GST adjustments in Hindi."]
    }
  }
];

export const MOCK_CONTENT: ContentItem[] = [
  {
    id: "c-1",
    campaignId: "finsmart-gtm",
    channel: "x",
    type: "post",
    body: "Still copying and pasting sales from Tally to check your GST compliance? 🤯\n\nIndian businesses lose thousands in unclaimed Input Tax Credit (ITC) every year due to manual matching errors.\n\nReconcile GSTR-2B with Tally in just 1 click with FinSmart. 🚀\n\n👉 finsmart.in/demo\n\n#GST #TallyPrime #SMEIndia #Accounting",
    status: "published",
    publishedAt: new Date(Date.now() - 3600000 * 24 * 3).toISOString(),
    metrics: { impressions: 12500, clicks: 420, likes: 184, replies: 28, signups: 74 },
    createdAt: new Date(Date.now() - 3600000 * 24 * 3).toISOString(),
  },
  {
    id: "c-2",
    campaignId: "finsmart-gtm",
    channel: "linkedin",
    type: "post",
    body: "Tired of tax filing delays bottlenecking your accounting firm? \n\nChartered Accountants spend up to 40% of tax season chasing clients for missing GST documents. \n\nWith FinSmart's unified multi-tenant dashboard, you can track all client Tally ledgers, auto-trigger WhatsApp reminders for GSTR mismatches, and claim 100% accurate Input Tax Credit.\n\nSign up today for a free CA audit trial.\n\n👉 finsmart.in/ca-partner\n\n#CharteredAccountant #B2BIndia #GSTCompliance #Fintech",
    status: "published",
    publishedAt: new Date(Date.now() - 3600000 * 24 * 2).toISOString(),
    metrics: { impressions: 24200, clicks: 880, likes: 312, replies: 42, signups: 198 },
    createdAt: new Date(Date.now() - 3600000 * 24 * 2).toISOString(),
  },
  {
    id: "c-3",
    campaignId: "finsmart-gtm",
    channel: "email",
    type: "email",
    title: "Claim your unclaimed Input Tax Credit (ITC) from Tally",
    body: "Dear Finance Partner,\n\nDid you know that over 78% of small and medium businesses in India file incorrect GST returns, missing out on crucial Input Tax Credit (ITC)?\n\nIf your team manually matches purchase invoices with your GSTR-2B portal report, mistakes are inevitable. FinSmart links directly with your desktop Tally application to run real-time checks.\n\nGet a free report on your business's compliance leaks in 5 minutes.\n\nTry FinSmart Free today: finsmart.in/itc-scan\n\nWarm regards,\nTeam FinSmart",
    status: "scheduled",
    scheduledAt: new Date(Date.now() + 3600000 * 12).toISOString(), // 12 hours from now
    createdAt: new Date(Date.now() - 3600000).toISOString(),
  }
];

export const MOCK_AGENT_LOGS: Record<string, string[]> = {
  strategy: [
    "[INFO] Initializing Strategy Agent...",
    "[INFO] Reading business details for product 'FinSmart'...",
    "[INFO] Goal: 500 signups, 50k impressions on Twitter/X, LinkedIn, and Email...",
    "[REASONING] Product targets GST compliance in India. Primary integration is Tally. Target demographic is SME owners and CAs.",
    "[DECISION] Channel Selection: Twitter/X (reach & tech focus), LinkedIn (professional CAs & founders), Email (cold list conversion).",
    "[STRATEGY] Defined main positioning: '1-click Tally GST reconciliation, saving 15 hours/month.'",
    "[KPI TARGETS] Setup milestone: Week 1 (150 signups), Week 2 (350 signups).",
    "[SUCCESS] GTM Strategy Plan generated successfully in JSON."
  ],
  research: [
    "[INFO] Initializing Research Agent...",
    "[INFO] Analysing ICP: SME owners using Tally and CAs...",
    "[RESEARCH] Scraping accounting forums and scanning competitor strategies...",
    "[COMPETITOR ANALYSES] Cleaned data on ClearTax (SME pricing barrier) and Vyapar (lack of Tally integration).",
    "[PERSONA CREATED] 'Ramesh Sharma': Tech-wary merchant. Pain points: compliance penalties, data reconciliation mismatches.",
    "[PERSONA CREATED] 'CA Neha Gupta': Independent advisor. Pain points: client collaboration delays, manual GSTR check bottlenecks.",
    "[TREND SEARCH] Trending hashtags identified: #GSTPrime, #TaxUpdate, #TallyAccounting.",
    "[SUCCESS] Competitor profiles and target personas saved to state."
  ],
  content: [
    "[INFO] Initializing Content Agent...",
    "[INFO] Fetching GTM plan and persona guidelines...",
    "[COPYWRITING] Theme 1: GST Freedom. Target: Ramesh Sharma.",
    "[DRAFT] Creating Twitter post: 'Still copying and pasting sales from Tally...'" ,
    "[COPYWRITING] Theme 2: Automated Compliance. Target: CA Neha Gupta.",
    "[DRAFT] Creating LinkedIn post: 'Tired of tax filing delays...'",
    "[COPYWRITING] Theme 3: Input Tax Credit scan. Target: SME finance teams.",
    "[DRAFT] Creating Email draft: 'Claim your unclaimed Input Tax Credit (ITC)...'",
    "[SUCCESS] Generated 3 assets, mapped tone to target personas, variants saved."
  ],
  executing: [
    "[INFO] Initializing Channel Agents...",
    "[CHANNEL] Connecting to mock Twitter/X API...",
    "[SUCCESS] Published post ID 'c-1' to Twitter/X. Status: Active.",
    "[CHANNEL] Connecting to mock LinkedIn API...",
    "[SUCCESS] Published post ID 'c-2' to LinkedIn. Status: Active.",
    "[CHANNEL] Queueing B2B outreach email...",
    "[SUCCESS] Scheduled email campaign ID 'c-3' for delivery.",
    "[INFO] Social reach listeners active. Live telemetry stream initialized."
  ],
  analytics: [
    "[INFO] Initializing Analytics Agent...",
    "[DATA] Scraping impressions, link clicks, and CTA signups...",
    "[METRICS] Twitter/X: 12.5k impressions, 420 clicks, 74 signups.",
    "[METRICS] LinkedIn: 24.2k impressions, 880 clicks, 198 signups.",
    "[ANALYSIS] LinkedIn performs 53% better on CTR due to professional CA targeting. Twitter/X is cost-efficient for top-of-funnel reach.",
    "[SUCCESS] Aggregate results: 36.7k impressions, 1300 clicks, 272 signups.",
    "[RECOMMENDATION] Shift 20% budget focus from general SME posts to specialized CA partner posts."
  ]
};
