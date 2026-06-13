import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    businessInfo: v.any(),
    goal: v.string(),
  },
  handler: async (ctx, args) => {
    const { businessInfo, goal } = args;
    const { icp, ...cleanBusinessInfo } = businessInfo;
    const id = await ctx.db.insert("campaigns", {
      name: businessInfo.name || "Unnamed Campaign",
      businessInfo: cleanBusinessInfo,
      icp: icp || "",
      goal,
      status: "running",
      currentCycle: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });
    return { campaignId: id };
  },
});