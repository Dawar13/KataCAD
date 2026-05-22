import type { Layer } from "./domain";

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

export interface EchoRequest {
  message: string;
}

export interface EchoResponse {
  received: string;
  service: string;
}

/** A prompt sent to the router for classification. */
export interface RouteRequest {
  prompt: string;
}

/** The router's classification of a prompt. */
export interface RouteResponse {
  layer: Layer;
  /** Hero id when `layer` is 1, otherwise null. */
  hero: string | null;
  /** Archetype name when `layer` is 2, otherwise null. */
  archetype: string | null;
  /** Numeric parameters extracted from the prompt. */
  params: Record<string, number>;
  /** Where the classification came from. */
  source: "openai" | "cache" | "fallback";
}
