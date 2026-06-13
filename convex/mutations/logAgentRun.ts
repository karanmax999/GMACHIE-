import { mutation } from "../_generated/server";
import { v } from "convex/validation";

export default mutation({
  args: {
    campaignId: v.id("campaigns"),
    agentName: v.string(),
    phase: v.string(),
    input: v.any(),
    output: v.any(),
    status: v.string(),
    startedAt: v.string(),  // ISO date string
    completedAt: v.optional(v.string()),
    errors: v.optional(v.array(v.string())),
  },
  handler: (ctx, args) => {
    const {
      campaignId,
      agentName,
      phase,
      input,
      output,
      status,
      startedAt,
      completedAt,
      errors,
    } = args;
    ctx.db.insert("agentRuns", {
      campaignId,
      agentName,
      phase,
      input,
      output,
      status,
      startedAt,
      completedAt,
      errors,
    });
    return { success: true };
  },
});