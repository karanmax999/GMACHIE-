import { mutation } from "../_generated/server";
import { v } from "convex/values";

export default mutation({
  args: {
    contentId: v.id("content"),
    updates: v.any(),
  },
  handler: async (ctx, args) => {
    const { contentId, updates } = args;
    await ctx.db.patch(contentId, updates);
  },
});
