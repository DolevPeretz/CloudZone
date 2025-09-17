export type StatusKind = "info" | "success" | "error";

export interface ExistsResponse {
  exists: boolean;
  id?: string;
}

export interface ApiClient {
  getExists(id: string): Promise<ExistsResponse>;
  putId(id: string): Promise<unknown>;
  deleteId(id: string): Promise<unknown>;
}
