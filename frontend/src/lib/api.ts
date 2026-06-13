const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8082';

export interface Campaign {
  _id: string;
  name: string;
  businessInfo: any;
  icp?: string;
  goal: string;
  status?: string;
  currentCycle?: number;
  createdAt?: string;
  updatedAt?: string;
  // Optional derived fields
  totalImpressions?: number;
  totalClicks?: number;
  totalSignups?: number;
  ctr?: number;
  recommendations?: string[];
  finalReport?: any;
}

export async function startCampaign(data: {
  business_info: any;
  goal: string;
  icp?: string;
}): Promise<{ campaign_id: string; status: string }> {
  const res = await fetch(`${API_BASE}/api/campaigns`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to start campaign');
  return res.json();
}

export async function getCampaigns(): Promise<Campaign[]> {
  const res = await fetch(`${API_BASE}/api/campaigns`);
  if (!res.ok) throw new Error('Failed to fetch campaigns');
  return res.json();
}

export async function getCampaign(id: string): Promise<Campaign> {
  const res = await fetch(`${API_BASE}/api/campaigns/${id}`);
  if (!res.ok) throw new Error('Failed to fetch campaign');
  return res.json();
}

export async function getCampaignContent(id: string): Promise<any[]> {
  const res = await fetch(`${API_BASE}/api/campaigns/${id}/content`);
  if (!res.ok) throw new Error('Failed to fetch content');
  return res.json();
}

export async function getCampaignMetrics(id: string): Promise<any[]> {
  const res = await fetch(`${API_BASE}/api/campaigns/${id}/metrics`);
  if (!res.ok) throw new Error('Failed to fetch metrics');
  return res.json();
}

export async function getCampaignAgentRuns(id: string): Promise<any[]> {
  const res = await fetch(`${API_BASE}/api/campaigns/${id}/agent-runs`);
  if (!res.ok) throw new Error('Failed to fetch agent runs');
  return res.json();
}

export async function triggerCampaignRun(id: string): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/api/campaigns/${id}/run`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to trigger campaign run');
  return res.json();
}