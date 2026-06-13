import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    campaignId: v.id("campaigns"),
    updates: v.any(),
  },
  handler: async (ctx, args) => {
    const { campaignId, updates } = args;
    await ctx.db.patch(campaignId, {
      ...updates,
      updatedAt: new Date().toISOString(),
    });
    return { success: true };
  },
});