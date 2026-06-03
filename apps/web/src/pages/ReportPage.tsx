import React, { useState, useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import type { CalculateRequest, ReportResponse } from "../types/bazi";
import { reportBazi } from "../api/client";

export default function ReportPage() {
  const location = useLocation();
  const request = location.state?.request as CalculateRequest;

  const [report, setReport] = useState<ReportResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!request) {
      setError("未找到排盘请求，请先排盘");
      setLoading(false);
      return;
    }
    reportBazi(request)
      .then(setReport)
      .catch((err) => setError(err?.response?.data?.detail || err.message || "生成报告失败"))
      .finally(() => setLoading(false));
  }, [request]);

  if (loading) {
    return (
      <div className="text-center py-16">
        <div className="animate-spin text-4xl mb-4">☯</div>
        <p className="text-gray-500">正在生成命理报告...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
        <Link to="/" className="text-red-600 underline mt-4 inline-block">
          返回首页
        </Link>
      </div>
    );
  }

  if (!report) return null;

  return (
    <div className="space-y-4">
      <Link to="/chart" className="text-red-600 hover:text-red-800">
        ← 返回命盘
      </Link>

      <div className="bg-white rounded-xl shadow-lg p-6">
        {/* Render markdown content safely */}
        {report.sections.map((section, i) => {
          // Parse simple markdown: headers, lists, tables, bold
          const lines = section.content.split("\n");
          const elements: React.JSX.Element[] = [];
          let key = 0;

          for (const line of lines) {
            if (!line.trim()) {
              elements.push(<div key={key++} className="h-2" />);
            } else if (line.startsWith("### ")) {
              elements.push(
                <h4 key={key++} className="text-base font-bold text-gray-700 mt-3 mb-1">
                  {line.slice(4)}
                </h4>
              );
            } else if (line.startsWith("## ")) {
              elements.push(
                <h3 key={key++} className="text-lg font-bold text-red-900 mt-4 mb-2">
                  {line.slice(3)}
                </h3>
              );
            } else if (line.startsWith("- ")) {
              elements.push(
                <li key={key++} className="text-gray-600 ml-4 text-sm">
                  {renderBold(line.slice(2))}
                </li>
              );
            } else if (line.startsWith("|")) {
              // Simple table — render as pre
              elements.push(
                <pre key={key++} className="text-xs text-gray-500 overflow-x-auto bg-gray-50 p-2 rounded">
                  {line}
                </pre>
              );
            } else {
              elements.push(
                <p key={key++} className="text-gray-600 text-sm leading-relaxed">
                  {renderBold(line)}
                </p>
              );
            }
          }

          return (
            <div key={i} className="mb-6 pb-6 border-b border-gray-100 last:border-0">
              <h2 className="text-xl font-bold text-red-800 mb-3">
                {section.heading}
              </h2>
              <div>{elements}</div>
            </div>
          );
        })}
      </div>

      <div className="text-center pb-8">
        <Link
          to="/"
          className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
        >
          重新排盘
        </Link>
      </div>
    </div>
  );
}

/** Render **bold** markers in text. */
function renderBold(text: string): React.JSX.Element {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <strong key={i} className="text-gray-900 font-semibold">
            {part.slice(2, -2)}
          </strong>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}
