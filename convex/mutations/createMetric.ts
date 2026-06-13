import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    campaignId: v.id("campaigns"),
    contentId: v.optional(v.id("content")),
    channel: v.string(),
    metricType: v.string(),
    value: v.number(),
    recordedAt: v.string(),  // ISO date string
  },
  handler: (ctx, args) => {
    const { campaignId, contentId, channel, metricType, value, recordedAt } = args;
    ctx.db.insert("metrics", {
      campaignId,
      contentId,
      channel,
      metricType,
      value,
      recordedAt,
    });
    return { success: true };
  },
});