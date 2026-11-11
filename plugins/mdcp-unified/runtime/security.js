const SECURITY_HEADERS = [
  ["content-security-policy", "Content Security Policy is missing; define a restrictive policy and test it before enforcement."],
  ["strict-transport-security", "HSTS is missing; enable it only after HTTPS is correctly deployed across the domain."],
  ["x-content-type-options", "Set X-Content-Type-Options: nosniff."],
  ["referrer-policy", "Set a privacy-conscious Referrer-Policy."],
  ["permissions-policy", "Define a Permissions-Policy for browser capabilities not required by the application."]
];

function normalizeHost(value) {
  return String(value ?? "").trim().toLowerCase().replace(/^\[|\]$/g, "");
}

export async function inspectWebsiteSecurity({ targetUrl, allowedHosts = [], fetchImpl = fetch, timeoutMs = 8000 } = {}) {
  if (!targetUrl) throw new Error("targetUrl is required.");
  const target = new URL(targetUrl);
  if (target.protocol !== "https:") throw new Error("Only HTTPS targets are accepted.");
  if (target.username || target.password) throw new Error("URLs containing credentials are not accepted.");
  const allow = new Set(allowedHosts.map(normalizeHost));
  if (!allow.has(normalizeHost(target.hostname))) throw new Error("Target hostname is not in allowedHosts. Add only a domain you own or are authorized to assess.");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetchImpl(target, { method: "GET", redirect: "manual", signal: controller.signal, headers: { "user-agent": "MDCP-Defensive-Audit/1.0" } });
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get("location");
      if (location) {
        const redirect = new URL(location, target);
        if (redirect.protocol !== "https:" || !allow.has(normalizeHost(redirect.hostname))) {
          return { target: target.origin, status: response.status, findings: [{ severity: "high", check: "redirect", detail: "Redirect points outside the HTTPS allowlist; it was not followed." }] };
        }
      }
    }
    const findings = [];
    for (const [header, detail] of SECURITY_HEADERS) {
      if (!response.headers.has(header)) findings.push({ severity: header === "content-security-policy" ? "medium" : "low", check: header, detail });
    }
    const csp = response.headers.get("content-security-policy") ?? "";
    if (/unsafe-inline|unsafe-eval/i.test(csp)) findings.push({ severity: "medium", check: "csp-directives", detail: "CSP contains unsafe-inline or unsafe-eval; assess whether nonces/hashes can replace them." });
    const server = response.headers.get("server");
    if (server) findings.push({ severity: "info", check: "server-disclosure", detail: "Server header is exposed; avoid unnecessary version/product disclosure." });
    const powered = response.headers.get("x-powered-by");
    if (powered) findings.push({ severity: "low", check: "technology-disclosure", detail: "X-Powered-By is exposed; remove it if not operationally required." });
    return { target: target.origin, status: response.status, mode: "passive-http-headers-only", findings, limitations: ["No port scan, payload injection, authentication bypass, crawling or exploitation was performed.", "Use network egress firewalling and DNS/IP controls in the deployment environment.", "A clean header check does not prove the application is secure."] };
  } finally {
    clearTimeout(timeout);
  }
}

export function reviewSqlSafety({ sourceCode = "", language = "javascript" } = {}) {
  if (typeof sourceCode !== "string" || !sourceCode.trim()) throw new Error("sourceCode is required.");
  const findings = [];
  const rules = [
    { id: "js-template-query", languages: ["javascript", "typescript"], pattern: /(?:query|execute|raw)\s*\(\s*\x60[^\x60]*\$\{/gi, detail: "Possible SQL built with template interpolation. Use parameterized queries and bind values separately." },
    { id: "js-concat-query", languages: ["javascript", "typescript"], pattern: /(?:query|execute|raw)\s*\([^)]*(?:\+\s*[A-Za-z_$]|\$\{)/gi, detail: "Possible SQL string concatenation. Replace with parameterized statements." },
    { id: "python-fstring-query", languages: ["python"], pattern: /(?:execute|executemany)\s*\(\s*f["']/gi, detail: "Possible f-string passed to a database execution method. Use DB-API placeholders." },
    { id: "php-concat-query", languages: ["php"], pattern: /(?:query|exec|prepare)\s*\([^)]*\.\s*\$/gi, detail: "Possible PHP variable concatenation in SQL. Prefer prepared statements with bound parameters." },
    { id: "unsafe-select-star", languages: ["sql"], pattern: /SELECT\s+\*\s+FROM/gi, detail: "SELECT * can expose more columns than needed. Select explicit columns and enforce authorization at the data layer." }
  ];
  for (const rule of rules) {
    if (rule.languages.includes(language) && rule.pattern.test(sourceCode)) findings.push({ severity: "warning", rule: rule.id, detail: rule.detail });
    rule.pattern.lastIndex = 0;
  }
  return { language, mode: "static-heuristic-review", findings, recommendations: ["Use parameterized queries/prepared statements for every user-controlled value.", "Validate input by business rules; validation does not replace parameterization.", "Use least-privilege database accounts and restrict sensitive columns/rows.", "Do not expose SQL errors or database details to end users.", "Add regression tests for authorization boundaries and injection-resistant query handling."], limitations: ["Heuristic checks can miss vulnerabilities and produce false positives.", "No code is executed and no live database is contacted.", "Review ORM raw-query escape hatches and stored procedures manually."] };
}

export function buildE2ePlan({ appType = "web application", flows = [] } = {}) {
  const baseline = ["Authentication: login, logout, session expiry, MFA and account recovery", "Authorization: role boundaries, tenant isolation and direct-object access", "Input handling: server-side validation, output encoding and safe error messages", "Core user journeys: create, read, update and delete with permission checks", "API contracts: schema validation, rate limits and consistent error responses", "Browser security: CSRF protections, cookie flags, CSP and HTTPS", "Resilience: timeout, retry, duplicate submission and network interruption", "Accessibility and responsive behavior on supported viewport sizes"];
  return { appType, userFlows: flows, testCases: [...baseline, ...flows.map(flow => `User flow: ${flow}`)], automationGuidance: ["Use Playwright or an equivalent browser E2E framework.", "Run against staging/test accounts and synthetic data.", "Keep destructive tests isolated; reset fixtures between runs.", "Store credentials in the CI secret manager, never in test files.", "Capture traces/screenshots on failure while redacting tokens and personal data."], safety: "Run tests only against environments you own or are explicitly authorized to test." };
}
