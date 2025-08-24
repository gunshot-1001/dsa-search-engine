import React, { useState } from "react";

export default function AuthModal({ mode, onClose, onAuth, switchMode }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await onAuth(`/${mode}`, { username, password });
      onClose();
    } catch (err) {
      setError(err.message || "Auth failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
        <h2 className="text-2xl font-bold text-green-700 mb-4">
          {mode === "signup" ? "Sign Up" : "Log In"}
        </h2>

        {error && <div className="text-sm text-red-600 mb-3">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            className="w-full rounded-lg border px-4 py-2 focus:ring-2 focus:ring-green-500"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full rounded-lg border px-4 py-2 focus:ring-2 focus:ring-green-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg px-4 py-2 bg-green-600 text-white hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? "Please wait..." : mode === "signup" ? "Sign Up" : "Log In"}
          </button>
        </form>

        <div className="mt-4 text-sm text-gray-600 text-center">
          {mode === "signup" ? (
            <>
              Already have an account?{" "}
              <button onClick={() => switchMode("login")} className="text-green-600 hover:underline">
                Log in
              </button>
            </>
          ) : (
            <>
              Don’t have an account?{" "}
              <button onClick={() => switchMode("signup")} className="text-green-600 hover:underline">
                Sign up
              </button>
            </>
          )}
        </div>

        <button
          onClick={onClose}
          className="absolute top-2 right-3 text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>
      </div>
    </div>
  );
}
