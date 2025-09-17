import type { ApiClient, ExistsResponse } from "./types";

async function request<T = unknown>({
  baseUrl,
  apiKey,
  method,
  path = "/customer",
  query,
  body,
}: {
  baseUrl: string;
  apiKey?: string;
  method: "GET" | "PUT" | "DELETE";
  path?: string;
  query?: Record<string, string | undefined>;
  body?: unknown;
}): Promise<T> {
  if (!baseUrl) throw new Error("חסר API Base URL (אפשר להגדיר במסך Settings)");

  const base = baseUrl.endsWith("/") ? baseUrl : baseUrl + "/";
  const url = new URL(path.startsWith("/") ? path.slice(1) : path, base);
  if (query)
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined) url.searchParams.set(k, String(v));
    });

  const res = await fetch(url.toString(), {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(apiKey ? { "x-api-key": apiKey } : {}),
    },
    body: method === "PUT" ? JSON.stringify(body ?? {}) : undefined,
  });

  const text = await res.text();
  let json: any = undefined;
  try {
    json = text ? JSON.parse(text) : undefined;
  } catch {}

  if (!res.ok) {
    const msg = json?.message || json?.error || text || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return (json as T) ?? ({} as T);
}

export function createApiClient(baseUrl: string, apiKey?: string): ApiClient {
  return {
    async getExists(id: string) {
      return request<ExistsResponse>({
        baseUrl,
        apiKey,
        method: "GET",
        path: `/customers/${id}`,
      });
    },
    async putId(id: string) {
      return request({
        baseUrl,
        apiKey,
        method: "PUT",
        path: `/customers/${id}`,
      });
    },
    async deleteId(id: string) {
      return request({
        baseUrl,
        apiKey,
        method: "DELETE",
        path: `/customers/${id}`,
      });
    },
  };
}
