import type { EchoRequest, EchoResponse, HealthResponse } from "@katacad/shared";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

export async function echo(request: EchoRequest): Promise<EchoResponse> {
  const res = await fetch(`${API_URL}/api/echo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error(`Echo failed: ${res.status}`);
  return res.json();
}
