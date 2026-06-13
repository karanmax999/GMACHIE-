import { query } from "../_generated/server";
import { v } from "convex/values";

export default query({
  args: {
    campaignId: v.id("campaigns"),
  },
  handler: (ctx, args) => {
    const { campaignId } = args;
    const campaign = ctx.db.get(campaignId);
    if (!campaign) {
      throw new Error("Campaign not found");
    }
    return campaign;
  },
});