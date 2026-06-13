import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    campaignId: v.id("campaigns"),
    channel: v.string(),
    type: v.string(),
    title: v.optional(v.string()),
    body: v.string(),
    variant: v.optional(v.string()),
    status: v.string(),
    publishedAt: v.optional(v.string()),
    scheduledAt: v.optional(v.string()),
    metrics: v.optional(v.any()),
  },
  handler: async (ctx, args) => {
    const {
      campaignId,
      channel,
      type,
      title,
      body,
      variant,
      status,
      publishedAt,
      scheduledAt,
      metrics,
    } = args;
    const id = await ctx.db.insert("content", {
      campaignId,
      channel,
      type,
      title,
      body,
      variant,
      status,
      publishedAt,
      scheduledAt,
      metrics,
      createdAt: new Date().toISOString(),
    });
    return { contentId: id };
  },
});