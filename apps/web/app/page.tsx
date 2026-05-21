"use client";

import { useState } from "react";

export default function HomePage() {
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const pingApi = async () => {
    setLoading(true);
    setResponse("");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/echo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "hello from web" }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      setResponse(`Error: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h1>KatACAD — Phase 0 Placeholder</h1>
      <p>
        This page exists only to prove the web app can talk to the API. Real functionality begins in
        Phase 1.
      </p>
      <button onClick={pingApi} disabled={loading}>
        {loading ? "Pinging..." : "Ping API"}
      </button>
      {response && <pre>{response}</pre>}
    </main>
  );
}
