import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiFilter } from "react-icons/fi";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function Dashboard() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const [filters, setFilters] = useState({
    difficulties: [],
  });

  const navigate = useNavigate();

  async function doSearch() {
    setLoading(true);

    // Always query backend (if no input, fallback default query)
    const query = q.trim() ? q : "DSA";
    const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}&top_k=50`);
    const data = await res.json();

    // Apply Difficulty filter only
    let filtered = data;
    if (filters.difficulties.length > 0) {
      filtered = filtered.filter((r) =>
        filters.difficulties.some((d) => (r.tag || "").toLowerCase() === d.toLowerCase())
      );
    }

    setResults(filtered);
    setLoading(false);
  }

  function toggleFilter(value) {
    setFilters((prev) => {
      const list = prev.difficulties;
      if (list.includes(value)) {
        return { difficulties: list.filter((v) => v !== value) };
      } else {
        return { difficulties: [...list, value] };
      }
    });
  }

  function handleLogout() {
    localStorage.removeItem("dsa_token");
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white flex">
      {/* 🔹 Constant Sidebar */}
      <aside className="w-20 bg-[#111] flex flex-col items-center py-6 justify-between fixed left-0 top-0 h-full">
        <div></div>
        <div className="flex flex-col gap-8 items-center">
          {/* Gemini → Redirect */}
          <button onClick={() => navigate("/gemini")} className="hover:opacity-80">
            <img
              src="https://t3.ftcdn.net/jpg/08/15/97/26/360_F_815972611_RfHmGN2bO5HAfRpennZXV5l6wJ9PVFrE.jpg"
              alt="Gemini"
              className="w-10 h-10 rounded-full object-cover"
            />
          </button>

          {/* Account */}
          <button onClick={() => navigate("/profile")} className="hover:opacity-80">
            <img
              src="https://png.pngtree.com/png-vector/20191001/ourlarge/pngtree-account-icon-isolated-on-abstract-background-png-image_1769246.jpg"
              alt="Account"
              className="w-10 h-10 rounded-full object-cover"
            />
          </button>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-600"
          >
            <FiLogOut size={24} />
          </button>
        </div>
      </aside>

      {/* 🔹 Main content */}
      <main className="flex-1 flex flex-col items-center justify-center ml-20 px-6">
        {/* Heading */}
        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-8">
          DSA Problems
        </h1>

        {/* Search Bar + Filter Button */}
        <div className="w-full max-w-2xl flex items-center bg-[#1a1a1a] rounded-xl px-4 py-3 mb-6">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && doSearch()}
            placeholder="Search DSA topics, e.g., 'binary search'"
            className="flex-1 bg-transparent outline-none text-white placeholder-gray-500"
          />
          <button
            onClick={doSearch}
            disabled={loading}
            className="ml-3 px-5 py-2 rounded-lg bg-green-600 hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? "..." : "Go"}
          </button>
          <button
            onClick={() => setShowFilters((v) => !v)}
            className="ml-2 p-2 rounded-lg bg-gray-800 hover:bg-gray-700"
          >
            <FiFilter size={20} />
          </button>
        </div>

        {/* Filter Panel → Difficulty only */}
        {showFilters && (
          <div className="w-full max-w-2xl bg-[#1a1a1a] rounded-xl p-4 mb-8 shadow-lg text-sm">
            <p className="mb-2 text-gray-300 font-semibold">Difficulty</p>
            <div className="flex gap-4">
              {["Easy", "Medium", "Hard"].map((level) => (
                <label key={level} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={filters.difficulties.includes(level)}
                    onChange={() => toggleFilter(level)}
                  />
                  {level}
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Results → only after Go */}
        {results.length > 0 && (
          <div className="w-full max-w-5xl grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((r, idx) => (
              <div
                key={idx}
                className="p-6 bg-[#1a1a1a] rounded-2xl shadow hover:shadow-lg transition"
              >
                <a
                  href={r.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-green-400 font-bold text-lg hover:underline"
                >
                  {r.title}
                </a>
                <p className="text-gray-400 text-sm mt-2">{r.snippet}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {r.domain} • {r.tag || "untagged"}
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
