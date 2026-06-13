import { query } from "../_generated/server";
import { v } from "convex/values";

export default query({
  args: {
    campaignId: v.id("campaigns"),
  },
  handler: async (ctx, args) => {
    const { campaignId } = args;
    return await ctx.db
      .query("content")
      .withIndex("by_campaign", (q) => q.eq("campaignId", campaignId))
      .collect();
  },
});