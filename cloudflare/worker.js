/**
 * 🔴💀 Cloudflare Worker — Edge API Gateway for Red Team Arsenal
 * Routes requests to the orchestrator, stores results in R2/KV
 */

const CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export default {
    async fetch(request, env) {
        // Handle CORS preflight
        if (request.method === "OPTIONS") {
            return new Response(null, { headers: CORS_HEADERS });
        }

        const url = new URL(request.url);
        const path = url.pathname;

        try {
            // ── Health Check ───────────────────────────────────────────
            if (path === "/health" || path === "/") {
                return json({ status: "🔴💀 Red Team Arsenal ONLINE", ts: Date.now() });
            }

            // ── Proxy to Orchestrator ──────────────────────────────────
            if (path.startsWith("/task") || path.startsWith("/research")) {
                return await proxyToOrchestrator(request, env);
            }

            // ── Report Storage (R2) ────────────────────────────────────
            if (path.startsWith("/report/")) {
                const sessionId = path.replace("/report/", "");
                return await handleReport(request, env, sessionId);
            }

            // ── Session State (KV) ─────────────────────────────────────
            if (path.startsWith("/session/")) {
                const sessionId = path.replace("/session/", "");
                return await handleSession(request, env, sessionId);
            }

            // ── Model Catalog ──────────────────────────────────────────
            if (path === "/models") {
                return json(MODEL_CATALOG);
            }

            return json({ error: "Not found" }, 404);
        } catch (e) {
            return json({ error: e.message }, 500);
        }
    },
};

// ── Proxy to Python Orchestrator ──────────────────────────────────────────────
async function proxyToOrchestrator(request, env) {
    const orchestratorUrl = env.ORCHESTRATOR_URL || "http://localhost:8888";
    const url = new URL(request.url);
    const targetUrl = `${orchestratorUrl}${url.pathname}${url.search}`;

    const proxied = new Request(targetUrl, {
        method: request.method,
        headers: { "Content-Type": "application/json" },
        body: request.method !== "GET" ? await request.text() : undefined,
    });

    try {
        const resp = await fetch(proxied);
        const data = await resp.json();
        return json(data, resp.status);
    } catch (e) {
        return json({ error: `Orchestrator unreachable: ${e.message}` }, 503);
    }
}

// ── R2 Report Storage ─────────────────────────────────────────────────────────
async function handleReport(request, env, sessionId) {
    if (!env.REPORTS_BUCKET) return json({ error: "R2 bucket not configured" }, 500);

    if (request.method === "PUT" || request.method === "POST") {
        const body = await request.text();
        await env.REPORTS_BUCKET.put(`reports/${sessionId}/report.md`, body, {
            httpMetadata: { contentType: "text/markdown" },
        });
        return json({ status: "stored", session_id: sessionId });
    }

    if (request.method === "GET") {
        const obj = await env.REPORTS_BUCKET.get(`reports/${sessionId}/report.md`);
        if (!obj) return json({ error: "Report not found" }, 404);
        const text = await obj.text();
        return new Response(text, {
            headers: { ...CORS_HEADERS, "Content-Type": "text/markdown" },
        });
    }

    return json({ error: "Method not allowed" }, 405);
}

// ── KV Session State ──────────────────────────────────────────────────────────
async function handleSession(request, env, sessionId) {
    if (!env.SESSIONS_KV) return json({ error: "KV namespace not configured" }, 500);

    if (request.method === "PUT" || request.method === "POST") {
        const body = await request.text();
        await env.SESSIONS_KV.put(`session:${sessionId}`, body, { expirationTtl: 86400 });
        return json({ status: "saved", session_id: sessionId });
    }

    if (request.method === "GET") {
        const value = await env.SESSIONS_KV.get(`session:${sessionId}`);
        if (!value) return json({ error: "Session not found" }, 404);
        return json(JSON.parse(value));
    }

    return json({ error: "Method not allowed" }, 405);
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function json(data, status = 200) {
    return new Response(JSON.stringify(data, null, 2), {
        status,
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
}

const MODEL_CATALOG = {
    infermatic: [
        "deepseek-r1", "deepseek-v3", "qwen3-235b-a22b",
        "llama-3.1-405b-instruct", "llama-3.3-70b-instruct",
        "qwen2.5-coder-32b-instruct", "deepseek-coder-v2-instruct",
        "gemma-3-27b-it", "phi-4", "mixtral-8x22b-instruct",
    ],
    huggingface: [
        "sentence-transformers/all-mpnet-base-v2",
        "BAAI/bge-large-en-v1.5",
        "jackaduma/SecBERT",
        "dslim/bert-base-NER",
        "bigcode/starcoder2-15b",
    ],
};
