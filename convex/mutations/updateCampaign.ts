import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    campaignId: v.id("campaigns"),
    updates: v.any(),
  },
  handler: (ctx, args) => {
    const { campaignId, updates } = args;
    ctx.db.patch(campaignId, {
      ...updates,
      updatedAt: new Date(),
    });
    return { success: true };
  },
});