import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleSignup() {
    const res = await fetch(`${API_BASE}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      alert("Signup failed");
      return;
    }
    const data = await res.json();
    localStorage.setItem("dsa_token", data.access_token);
    navigate("/dashboard");
  }

  return (
    <section
      className="h-screen bg-cover bg-center flex items-center justify-center relative"
      style={{
        backgroundImage:
          "url('https://www.epl.ca/wp-content/uploads/sites/18/2020/12/CodingSnowflakes_Dec2020_BlogCard_890x445.png')",
      }}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/70"></div>

      <div className="relative z-10 bg-black/80 p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-2xl font-bold text-white mb-4">Create an account</h2>
        <input
          className="w-full mb-3 px-4 py-2 rounded bg-gray-800 text-white"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          className="w-full mb-3 px-4 py-2 rounded bg-gray-800 text-white"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleSignup}
          className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-xl"
        >
          Sign Up
        </button>
        <p
          onClick={() => navigate("/login")}
          className="mt-3 text-sm text-gray-300 hover:underline cursor-pointer"
        >
          Already have an account? Log in
        </p>
      </div>
    </section>
  );
}
