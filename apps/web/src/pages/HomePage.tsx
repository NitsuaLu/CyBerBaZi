import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { CalculateRequest, CalculateResponse } from "../types/bazi";
import { calculateBazi } from "../api/client";

export default function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    birth_date: "2000-06-15",
    birth_time: "12:00",
    sex: "male" as "male" | "female",
    longitude: "120",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const req: CalculateRequest = {
      birth_date: form.birth_date,
      birth_time: form.birth_time + ":00",
      sex: form.sex,
      longitude: parseFloat(form.longitude) || 120,
    };

    try {
      const data: CalculateResponse = await calculateBazi(req);
      navigate("/chart", { state: { chart: data, request: req } });
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "请求失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto">
      <h2 className="text-3xl font-bold text-center text-red-900 mb-8">
        八字排盘
      </h2>
      <p className="text-gray-500 text-center mb-8">
        请输入出生信息，系统将为您排出八字命盘
      </p>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-6 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            出生日期
          </label>
          <input
            type="date"
            value={form.birth_date}
            onChange={(e) => setForm({ ...form, birth_date: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            出生时间
          </label>
          <input
            type="time"
            value={form.birth_time}
            onChange={(e) => setForm({ ...form, birth_time: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            性别
          </label>
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setForm({ ...form, sex: "male" })}
              className={`flex-1 py-2 rounded-lg font-medium transition ${
                form.sex === "male"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              男
            </button>
            <button
              type="button"
              onClick={() => setForm({ ...form, sex: "female" })}
              className={`flex-1 py-2 rounded-lg font-medium transition ${
                form.sex === "female"
                  ? "bg-pink-500 text-white"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              女
            </button>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            出生地经度
            <span className="text-gray-400 font-normal ml-1">
              (默认120°=北京时间)
            </span>
          </label>
          <input
            type="number"
            value={form.longitude}
            onChange={(e) => setForm({ ...form, longitude: e.target.value })}
            min="0"
            max="360"
            step="0.1"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-red-700 text-white font-bold text-lg rounded-lg hover:bg-red-800 transition disabled:opacity-50"
        >
          {loading ? "排盘中..." : "开始排盘"}
        </button>
      </form>
    </div>
  );
}
