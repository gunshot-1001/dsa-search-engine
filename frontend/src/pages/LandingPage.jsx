import React from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <section
      className="h-screen bg-cover bg-center flex flex-col items-center justify-center text-center px-6 relative"
      style={{
        backgroundImage:
          "url('https://miro.medium.com/v2/resize:fit:1400/0*7VyEZgzwUhQMeBqb')",
      }}
    >
      {/* Dark overlay for readability */}
      <div className="absolute inset-0 bg-black/70"></div>

      <div className="relative z-10">
        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-4">
          DSA Coding Platform
        </h1>
        <p className="max-w-2xl text-gray-200 text-lg mb-6">
          Curated LeetCode & HackerRank problems, AI help, and progress tracking — all in one place.
        </p>

        <button
          onClick={() => navigate("/signup")}
          className="mt-6 rounded-xl px-8 py-3 bg-red-600 hover:bg-red-700 text-white text-lg font-semibold shadow-lg"
        >
          Sign Up / Log In
        </button>

        <p className="mt-4 text-sm text-gray-300">
          Endless practice starting at ₹0 — it’s free.
        </p>
      </div>
    </section>
  );
}
