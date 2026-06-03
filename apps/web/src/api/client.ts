import axios from "axios";
import type {
  CalculateRequest,
  CalculateResponse,
  AnalyzeResponse,
  ReportResponse,
} from "../types/bazi";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  timeout: 30000,
});

export async function calculateBazi(
  req: CalculateRequest
): Promise<CalculateResponse> {
  const { data } = await api.post<CalculateResponse>("/bazi/calculate", req);
  return data;
}

export async function analyzeBazi(
  req: CalculateRequest
): Promise<AnalyzeResponse> {
  const { data } = await api.post<AnalyzeResponse>("/bazi/analyze", req);
  return data;
}

export async function reportBazi(
  req: CalculateRequest
): Promise<ReportResponse> {
  const { data } = await api.post<ReportResponse>("/bazi/report", req);
  return data;
}
