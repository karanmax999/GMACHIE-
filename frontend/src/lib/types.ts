export interface Campaign {
  id: string;
  name: string;
  businessInfo: {
    name: string;
    description: string;
    industry?: string;
    website?: string;
  };
  icp?: string;
  goal: string;
  status: 'running' | 'completed' | 'failed' | 'draft' | 'needs_review';
  currentCycle: number;
  currentPhase: 'idle' | 'strategy' | 'research' | 'content' | 'review' | 'executing' | 'analytics' | 'adapting' | 'completed';
  createdAt: string;
  updatedAt: string;
  gtmPlan?: {
    positioning: string;
    target_audience: string;
    channels: Array<{ name: string; primary: boolean; why: string; expected_reach: string }>;
    campaign_themes: string[];
    kpi_targets: Record<string, { impressions: number; clicks: number; signups: number }>;
    north_star_metric: string;
  };
  researchInsights?: {
    personas: Array<{
      name: string;
      description: string;
      pain_points: string[];
      triggers: string[];
      objections: string[];
      language: string[];
    }>;
    competitor_insights: Array<{
      competitor: string;
      strategy: string;
      strengths: string[];
      weaknesses: string[];
      opportunity: string;
    }>;
    trending_topics: Array<{ topic: string; relevance: string; hashtags: string[] }>;
    recommended_keywords: string[];
    content_gaps: string[];
  };
}

export interface ContentItem {
  id: string;
  campaignId: string;
  channel: 'x' | 'linkedin' | 'email';
  type: 'post' | 'thread' | 'email' | 'ad';
  title?: string;
  body: string;
  variant?: string;
  status: 'generated' | 'scheduled' | 'published' | 'failed';
  scheduledAt?: string;
  publishedAt?: string;
  metrics?: {
    impressions?: number;
    clicks?: number;
    likes?: number;
    replies?: number;
    signups?: number;
  };
  createdAt: string;
}

export interface AgentRun {
  id: string;
  campaignId: string;
  agentName: 'strategy' | 'research' | 'content' | 'channel_x' | 'channel_email' | 'analytics';
  phase: string;
  input: any;
  output: any;
  status: 'running' | 'success' | 'failed';
  startedAt: string;
  completedAt?: string;
  errors?: string[];
}

export interface Metric {
  id: string;
  campaignId: string;
  contentId?: string;
  channel: string;
  metricType: 'impressions' | 'clicks' | 'signups' | 'ctr';
  value: number;
  recordedAt: string;
}
