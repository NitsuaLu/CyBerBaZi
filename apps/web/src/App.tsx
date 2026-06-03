import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ChartPage from "./pages/ChartPage";
import ReportPage from "./pages/ReportPage";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-b from-amber-50 to-white">
        <header className="bg-red-800 text-white py-4 shadow-lg">
          <div className="max-w-4xl mx-auto px-4 flex items-center justify-between">
            <a href="/" className="text-2xl font-bold tracking-wider">
              八字命理
            </a>
            <span className="text-red-200 text-sm">传统命理学工具</span>
          </div>
        </header>
        <main className="max-w-4xl mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/chart" element={<ChartPage />} />
            <Route path="/report" element={<ReportPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
