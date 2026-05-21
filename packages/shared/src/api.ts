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
