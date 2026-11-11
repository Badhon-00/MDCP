import { inspectWebsiteSecurity, reviewSqlSafety, buildE2ePlan } from "./security.js";
import { executeYouTubeOperation } from "../../youtube-studio/runtime/agent-tool.js";

export const MDCP_TOOL_SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    operation: { type: "string", enum: ["website_security_audit", "sql_code_review", "e2e_test_plan", "youtube"] },
    targetUrl: { type: "string", description: "Website URL; hostname must be present in the configured allowlist." },
    allowedHosts: { type: "array", items: { type: "string" }, maxItems: 50 },
    sourceCode: { type: "string", description: "Source text to review; do not include secrets." },
    language: { type: "string", enum: ["javascript", "typescript", "python", "php", "sql"] },
    appType: { type: "string" },
    flows: { type: "array", items: { type: "string" }, maxItems: 30 },
    youtubeOperation: { type: "object" }
  },
  required: ["operation"]
};

export async function executeMdcpOperation(dependencies, args = {}) {
  switch (args.operation) {
    case "website_security_audit":
      return inspectWebsiteSecurity({ targetUrl: args.targetUrl, allowedHosts: args.allowedHosts, fetchImpl: dependencies.fetchImpl ?? fetch });
    case "sql_code_review":
      return reviewSqlSafety({ sourceCode: args.sourceCode, language: args.language });
    case "e2e_test_plan":
      return buildE2ePlan({ appType: args.appType, flows: args.flows ?? [] });
    case "youtube":
      if (!dependencies.youtubeClient) throw new Error("A configured YouTube API client is required for YouTube operations.");
      return executeYouTubeOperation({ client: dependencies.youtubeClient, fetchImpl: dependencies.fetchImpl ?? fetch }, args.youtubeOperation ?? {});
    default:
      throw new Error("Unsupported MDCP operation.");
  }
}

export function createMdcpTool(dependencies = {}) {
  return {
    name: "mdcp",
    description: "Unified MDCP tool. Choose one operation: passive authorized website security audit, SQL safety review, E2E test plan, or YouTube operation. Security checks do not exploit targets.",
    inputSchema: MDCP_TOOL_SCHEMA,
    async handler(args) {
      const result = await executeMdcpOperation(dependencies, args);
      return { content: [{ type: "text", text: JSON.stringify(result) }], structuredContent: { result } };
    }
  };
}

export function registerMdcpTool(server, dependencies = {}) {
  const tool = createMdcpTool(dependencies);
  if (typeof server?.registerTool !== "function") throw new Error("MCP server must expose registerTool(name, config, handler).");
  server.registerTool(tool.name, { description: tool.description, inputSchema: tool.inputSchema }, tool.handler);
  return tool.name;
}
