import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  campaigns: defineTable({
    name: v.string(),
    businessInfo: v.object({
      name: v.string(),
      description: v.string(),
      industry: v.optional(v.string()),
      website: v.optional(v.string()),
    }),
    icp: v.optional(v.string()),
    goal: v.string(),
    status: v.optional(v.string()), // "running", "completed", "failed"
    currentCycle: v.optional(v.number()),
    phases: v.optional(v.array(v.string())),
    // Results
    gtmPlan: v.optional(v.any()),
    personas: v.optional(v.array(v.any())),
    researchInsights: v.optional(v.array(v.any())),
    recommendations: v.optional(v.array(v.string())),
    totalImpressions: v.optional(v.number()),
    totalClicks: v.optional(v.number()),
    totalSignups: v.optional(v.number()),
    ctr: v.optional(v.number()),
    createdAt: v.optional(v.any()),
    updatedAt: v.optional(v.any()),
  }).index("by_status", ["status"]),

  content: defineTable({
    campaignId: v.id("campaigns"),
    channel: v.string(), // "x", "linkedin", "email"
    type: v.string(), // "post", "thread", "email", "ad"
    title: v.optional(v.string()),
    body: v.string(),
    variant: v.optional(v.string()),
    status: v.string(), // "generated", "scheduled", "published", "failed"
    publishedAt: v.optional(v.any()),
    scheduledAt: v.optional(v.any()),
    metrics: v.optional(v.object({
      impressions: v.optional(v.number()),
      clicks: v.optional(v.number()),
      likes: v.optional(v.number()),
      replies: v.optional(v.number()),
      signups: v.optional(v.number()),
    })),
    createdAt: v.optional(v.any()),
  }).index("by_campaign", ["campaignId"]),

  metrics: defineTable({
    campaignId: v.id("campaigns"),
    contentId: v.optional(v.id("content")),
    channel: v.string(),
    metricType: v.string(), // "impressions", "clicks", "signups", "ctr"
    value: v.number(),
    recordedAt: v.any(),
  }).index("by_campaign", ["campaignId"]).index("by_channel", ["channel"]),

  agentRuns: defineTable({
    campaignId: v.id("campaigns"),
    agentName: v.string(),
    phase: v.string(),
    input: v.any(),
    output: v.any(),
    status: v.string(), // "running", "success", "failed"
    startedAt: v.any(),
    completedAt: v.optional(v.any()),
    errors: v.optional(v.array(v.string())),
  }).index("by_campaign", ["campaignId"]).index("by_agent", ["agentName"]),
});