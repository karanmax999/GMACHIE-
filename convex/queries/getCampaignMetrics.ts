import { query } from "../_generated/server";
import { v } from "convex/validation";

export default query({
  args: {
    campaignId: v.id("campaigns"),
  },
  handler: (ctx, args) => {
    const { campaignId } = args;
    return ctx.db
      .query("by_campaign", (q) => q.eq("campaignId", campaignId))
      .collect();
  },
});