import { useLocation, Link } from "react-router-dom";
import { useState } from "react";
import type { CalculateResponse, CalculateRequest } from "../types/bazi";
import { analyzeBazi } from "../api/client";
import type { AnalyzeResponse } from "../types/bazi";

const WUXING_COLORS: Record<string, string> = {
  木: "#4CAF50",
  火: "#F44336",
  土: "#FF9800",
  金: "#FFC107",
  水: "#2196F3",
};

export default function ChartPage() {
  const location = useLocation();
  const chart = location.state?.chart as CalculateResponse;
  const request = location.state?.request as CalculateRequest;

  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [showAnalysis, setShowAnalysis] = useState(false);

  if (!chart) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">未找到命盘数据</p>
        <Link to="/" className="text-red-600 underline mt-4 inline-block">
          返回首页
        </Link>
      </div>
    );
  }

  const pillars = [
    { name: "年柱", key: "year_pillar" as const, data: chart.year_pillar },
    { name: "月柱", key: "month_pillar" as const, data: chart.month_pillar },
    { name: "日柱", key: "day_pillar" as const, data: chart.day_pillar },
    { name: "时柱", key: "hour_pillar" as const, data: chart.hour_pillar },
  ];

  const loadAnalysis = async () => {
    if (analysis) {
      setShowAnalysis(!showAnalysis);
      return;
    }
    setAnalyzing(true);
    try {
      const data = await analyzeBazi(request);
      setAnalysis(data);
      setShowAnalysis(true);
    } catch {
      alert("分析失败");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link to="/" className="text-red-600 hover:text-red-800">
          ← 重新排盘
        </Link>
        <div className="text-sm text-gray-500">
          {chart.sex === "男" ? "乾造" : "坤造"} · {chart.birth_datetime}
        </div>
      </div>

      {/* Four Pillars Table */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="grid grid-cols-4 text-center bg-red-800 text-white">
          {pillars.map((p) => (
            <div key={p.name} className="py-2 font-bold border-r border-red-700 last:border-0">
              {p.name}
            </div>
          ))}
        </div>

        {/* Heavenly Stems */}
        <div className="grid grid-cols-4 text-center border-b">
          {pillars.map((p, i) => (
            <div
              key={`stem-${i}`}
              className={`py-3 border-r last:border-0 ${
                p.key === "day_pillar" ? "bg-red-50" : ""
              }`}
            >
              <span className="text-3xl font-bold text-red-900">
                {p.data.heavenly_stem}
              </span>
              {p.data.stem_shishen && (
                <div className="text-xs text-gray-500 mt-1">
                  {p.data.stem_shishen}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Earthly Branches */}
        <div className="grid grid-cols-4 text-center border-b bg-gray-50">
          {pillars.map((p, i) => (
            <div key={`branch-${i}`} className="py-2 border-r last:border-0">
              <span className="text-2xl text-red-700">
                {p.data.earthly_branch}
              </span>
            </div>
          ))}
        </div>

        {/* Hidden Stems */}
        <div className="grid grid-cols-4 text-center border-b">
          {pillars.map((p, i) => (
            <div key={`hs-${i}`} className="py-2 border-r last:border-0 text-sm text-gray-600">
              {p.data.hidden_stems.map((h) => (
                <span key={h.stem} className="mx-1">
                  {h.stem}
                  <span className="text-xs text-gray-400">({h.qi_level})</span>
                </span>
              ))}
            </div>
          ))}
        </div>

        {/* Nayin */}
        <div className="grid grid-cols-4 text-center">
          {pillars.map((p, i) => (
            <div key={`nayin-${i}`} className="py-2 border-r last:border-0 text-sm text-gray-500">
              {p.data.nayin}
            </div>
          ))}
        </div>
      </div>

      {/* Day Master */}
      <div className="bg-white rounded-xl shadow-lg p-4 text-center">
        <span className="text-gray-500">日主</span>{" "}
        <span
          className="text-2xl font-bold"
          style={{
            color: WUXING_COLORS[chart.day_master_wuxing] || "#333",
          }}
        >
          {chart.day_master}
        </span>
        <span className="text-gray-400 ml-2">({chart.day_master_wuxing})</span>
      </div>

      {/* Fortune Cycles */}
      <div className="bg-white rounded-xl shadow-lg p-4">
        <h3 className="font-bold text-lg text-red-900 mb-3">
          大运走势 · 起运 {chart.qi_yun_age} 岁
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {chart.fortune_cycles.map((fc) => (
            <div
              key={fc.start_age}
              className="p-2 rounded-lg bg-amber-50 text-center text-sm"
            >
              <div className="text-red-800 font-bold">
                {fc.stem}{fc.branch}
              </div>
              <div className="text-gray-500 text-xs">
                {fc.start_age}岁 ({fc.start_year}-{fc.end_year})
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analyze Button */}
      <div className="text-center">
        <button
          onClick={loadAnalysis}
          disabled={analyzing}
          className="px-8 py-3 bg-red-700 text-white font-bold rounded-lg hover:bg-red-800 transition disabled:opacity-50"
        >
          {analyzing ? "分析中..." : showAnalysis ? "收起分析" : "查看命理分析"}
        </button>

        <Link
          to="/report"
          state={{ request }}
          className="ml-4 px-8 py-3 bg-amber-600 text-white font-bold rounded-lg hover:bg-amber-700 transition inline-block"
        >
          生成完整报告
        </Link>
      </div>

      {/* Inline Analysis */}
      {showAnalysis && analysis && (
        <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
          <h3 className="text-xl font-bold text-red-900">命理分析</h3>

          <div>
            <h4 className="font-bold text-gray-700">旺衰</h4>
            <p className="text-gray-600">
              {analysis.wang_shuai_level} (得分 {analysis.wang_shuai_score.toFixed(1)})
            </p>
          </div>

          <div>
            <h4 className="font-bold text-gray-700">格局</h4>
            <p className="text-gray-600">
              {analysis.geju} ({analysis.geju_category})
            </p>
          </div>

          <div>
            <h4 className="font-bold text-gray-700">用神</h4>
            <p className="text-gray-600">
              {analysis.yong_shen.join(", ")} · 忌: {analysis.ji_shen.join(", ")}
            </p>
          </div>

          <div>
            <h4 className="font-bold text-gray-700">十神分布</h4>
            <div className="flex flex-wrap gap-2 mt-1">
              {analysis.shishen.slice(0, 6).map((s) => (
                <span
                  key={s.shishen}
                  className="px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-700"
                >
                  {s.shishen} ×{s.total}
                </span>
              ))}
            </div>
          </div>

          {analysis.shensha.length > 0 && (
            <div>
              <h4 className="font-bold text-gray-700">神煞</h4>
              <div className="flex flex-wrap gap-2 mt-1">
                {analysis.shensha.map((r, i) => (
                  <span
                    key={i}
                    className={`px-2 py-1 rounded-full text-xs ${
                      r.category === "吉神"
                        ? "bg-green-100 text-green-700"
                        : r.category === "凶神"
                          ? "bg-red-100 text-red-700"
                          : "bg-gray-100 text-gray-700"
                    }`}
                  >
                    {r.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {analysis.suggestions.length > 0 && (
            <div>
              <h4 className="font-bold text-gray-700">建议</h4>
              <ul className="text-gray-600 text-sm list-disc pl-4">
                {analysis.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
