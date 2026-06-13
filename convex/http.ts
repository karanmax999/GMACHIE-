import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

const jsonResponse = (data: any, status = 200) => {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
    },
  });
};

// Route mutations
http.route({
  path: "/api/mutations/createCampaign",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.createCampaign.default, args);
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/mutations/updateCampaign",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.updateCampaign.default, args);
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/mutations/logAgentRun",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.logAgentRun.default, args);
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/mutations/createContent",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.createContent.default, args);
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/mutations/createMetric",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.createMetric.default, args);
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/mutations/updateContent",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const { args } = await request.json();
    const result = await ctx.runMutation(api.mutations.updateContent.default, args);
    return jsonResponse(result);
  }),
});

// Route queries
http.route({
  path: "/api/queries/getCampaign",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const campaignId = url.searchParams.get("campaignId");
    if (!campaignId) return jsonResponse({ error: "Missing campaignId" }, 400);
    const result = await ctx.runQuery(api.queries.getCampaign.default, { campaignId: campaignId as any });
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/queries/listCampaigns",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const result = await ctx.runQuery(api.queries.listCampaigns.default, {});
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/queries/getCampaignContent",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const campaignId = url.searchParams.get("campaignId");
    if (!campaignId) return jsonResponse({ error: "Missing campaignId" }, 450);
    const result = await ctx.runQuery(api.queries.getCampaignContent.default, { campaignId: campaignId as any });
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/queries/getCampaignMetrics",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const campaignId = url.searchParams.get("campaignId");
    if (!campaignId) return jsonResponse({ error: "Missing campaignId" }, 400);
    const result = await ctx.runQuery(api.queries.getCampaignMetrics.default, { campaignId: campaignId as any });
    return jsonResponse(result);
  }),
});

http.route({
  path: "/api/queries/getCampaignAgentRuns",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const url = new URL(request.url);
    const campaignId = url.searchParams.get("campaignId");
    if (!campaignId) return jsonResponse({ error: "Missing campaignId" }, 400);
    const result = await ctx.runQuery(api.queries.getCampaignAgentRuns.default, { campaignId: campaignId as any });
    return jsonResponse(result);
  }),
});

// OPTIONS preflight handler
http.route({
  path: "/api/mutations/:name",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }),
});

http.route({
  path: "/api/queries/:name",
  method: "OPTIONS",
  handler: httpAction(async () => {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }),
});

export default http;
