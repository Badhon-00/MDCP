/**
 * Configurable OpenAI-compatible provider fallback for a separate Node.js app/agent.
 * This does not intercept Claude.ai limits or run inside a Claude.ai Artifact.
 */
"use strict";

const fs = require("node:fs/promises");
const path = require("node:path");

const DEFAULT_PROVIDERS = [
  { name: "groq", baseURL: "https://api.groq.com/openai/v1/chat/completions", model: process.env.GROQ_MODEL || "llama-3.3-70b-versatile", apiKey: () => process.env.GROQ_API_KEY },
  { name: "openrouter", baseURL: "https://openrouter.ai/api/v1/chat/completions", model: process.env.OPENROUTER_MODEL || "meta-llama/llama-3.3-70b-instruct:free", apiKey: () => process.env.OPENROUTER_API_KEY },
  { name: "together", baseURL: "https://api.together.xyz/v1/chat/completions", model: process.env.TOGETHER_MODEL || "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", apiKey: () => process.env.TOGETHER_API_KEY }
];

const RETRYABLE_STATUS = new Set([401, 403, 408, 409, 425, 429, 500, 502, 503, 504]);

function makeError(message, status) {
  const error = new Error(message);
  if (status) error.status = status;
  return error;
}

async function writeCheckpoint(filePath, checkpoint) {
  if (!filePath) return;
  const target = path.resolve(filePath);
  await fs.mkdir(path.dirname(target), { recursive: true });
  const temp = target + "." + process.pid + ".tmp";
  await fs.writeFile(temp, JSON.stringify(checkpoint, null, 2) + "\n", { encoding: "utf8", mode: 0o600 });
  await fs.rename(temp, target);
}

async function callProvider(provider, messages, options) {
  const apiKey = typeof provider.apiKey === "function" ? provider.apiKey() : provider.apiKey;
  if (!apiKey) throw makeError("Missing API key for " + provider.name);

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), options.timeoutMs);
  try {
    const headers = { Authorization: "Bearer " + apiKey, "Content-Type": "application/json" };
    if (provider.name === "openrouter") {
      headers["HTTP-Referer"] = options.referer || "https://github.com/Badhon-00/MDCP";
      headers["X-Title"] = options.appTitle || "MDCP fallback client";
    }
    const response = await fetch(provider.baseURL, {
      method: "POST",
      headers,
      body: JSON.stringify({ model: provider.model, messages, temperature: options.temperature, max_tokens: options.maxTokens }),
      signal: controller.signal
    });
    const raw = await response.text();
    let data;
    try { data = raw ? JSON.parse(raw) : {}; }
    catch { throw makeError("Provider returned invalid JSON (" + response.status + ")", response.status); }

    if (!response.ok) {
      const detail = data?.error?.message || data?.error?.code;
      throw makeError(provider.name + " HTTP " + response.status + (detail ? ": " + String(detail).slice(0, 250) : ""), response.status);
    }
    const content = data?.choices?.[0]?.message?.content;
    if (typeof content !== "string" || !content.trim()) throw makeError(provider.name + " returned no assistant text");
    return content;
  } finally {
    clearTimeout(timer);
  }
}

async function continueWithFallback(input = {}) {
  if (typeof input.task !== "string" || !input.task.trim()) throw new TypeError("input.task must be a non-empty string");
  const providers = input.providers || DEFAULT_PROVIDERS;
  const messages = input.messages || [{ role: "user", content: input.task }];
  const options = {
    timeoutMs: input.timeoutMs || 45000,
    maxTokens: input.maxTokens || 4096,
    temperature: input.temperature ?? 0.2,
    referer: input.referer,
    appTitle: input.appTitle
  };
  const failures = [];

  for (const provider of providers) {
    if (!provider?.name || !provider?.baseURL || !provider?.model) continue;
    try {
      const content = await callProvider(provider, messages, options);
      const result = {
        taskId: input.taskId || null, task: input.task, provider: provider.name,
        model: provider.model, content, completedAt: new Date().toISOString(), failures
      };
      await writeCheckpoint(input.progressPath, {
        taskId: result.taskId, task: result.task, status: "response_received",
        provider: result.provider, model: result.model, lastOutput: result.content,
        completedAt: result.completedAt, failures
      });
      return result;
    } catch (error) {
      const status = error?.status;
      failures.push({ provider: provider.name, status: status || null, error: String(error?.message || error).slice(0, 350) });
      if (status && !RETRYABLE_STATUS.has(status)) throw error;
    }
  }

  await writeCheckpoint(input.progressPath, {
    taskId: input.taskId || null, task: input.task, status: "providers_exhausted",
    nextStep: "Retry later or configure another eligible provider.", failures,
    updatedAt: new Date().toISOString()
  });
  const error = makeError("All configured providers failed or have no API key.");
  error.failures = failures;
  throw error;
}

module.exports = { continueWithFallback, DEFAULT_PROVIDERS, writeCheckpoint };
