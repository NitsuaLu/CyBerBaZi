/** TypeScript types matching the BaZi API response schemas. */

export interface HiddenStemInfo {
  stem: string;
  qi_level: string;
  shishen: string | null;
}

export interface PillarData {
  heavenly_stem: string;
  earthly_branch: string;
  hidden_stems: HiddenStemInfo[];
  nayin: string;
  stem_shishen: string | null;
}

export interface FortuneCycle {
  stem: string;
  branch: string;
  start_age: number;
  start_year: number;
  end_year: number;
  nayin: string;
}

export interface CalculateResponse {
  sex: string;
  birth_datetime: string;
  true_solar_datetime: string | null;
  year_pillar: PillarData;
  month_pillar: PillarData;
  day_pillar: PillarData;
  hour_pillar: PillarData;
  day_master: string;
  day_master_wuxing: string;
  fortune_cycles: FortuneCycle[];
  qi_yun_age: number;
}

export interface ShiShenCount {
  shishen: string;
  stem_count: number;
  hidden_count: number;
  total: number;
}

export interface ShenShaResult {
  name: string;
  category: string;
  location: string;
  description: string;
}

export interface AnalyzeResponse {
  sex: string;
  birth_datetime: string;
  day_master: string;
  shishen: ShiShenCount[];
  shensha: ShenShaResult[];
  wang_shuai_level: string;
  wang_shuai_score: number;
  wang_shuai_details: string[];
  geju: string;
  geju_category: string;
  yong_shen: string[];
  ji_shen: string[];
  method: string;
  suggestions: string[];
}

export interface ReportSection {
  heading: string;
  content: string;
}

export interface ReportResponse {
  title: string;
  sections: ReportSection[];
  plain_text: string;
  markdown: string;
}

export interface CalculateRequest {
  birth_date: string;
  birth_time: string;
  sex: "male" | "female";
  longitude: number;
}
