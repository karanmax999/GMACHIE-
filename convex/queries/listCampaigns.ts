import { query } from "../_generated/server";

export default query({
  args: {},
  handler: (ctx) => {
    return ctx.db
      .query("by_status")
      .collect()
      .sort((a, b) => (b.createdAt?.getTime() || 0) - (a.createdAt?.getTime() || 0));
  },
});