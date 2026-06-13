import { mutation } from "../_generated/server";
import { v } from "convex/validation";

export default mutation({
  args: {
    businessInfo: v.any(),
    goal: v.string(),
  },
  handler: (ctx, args) => {
    const { businessInfo, goal } = args;
    const id = ctx.db.insert("campaigns", {
      name: businessInfo.name || "Unnamed Campaign",
      businessInfo,
      icp: businessInfo.icp || "",
      goal,
      status: "running",
      currentCycle: 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    });
    return { campaignId: id };
  },
});