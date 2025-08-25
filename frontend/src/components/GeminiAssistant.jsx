import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function GeminiAssistant() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]); // stores messages
  const [started, setStarted] = useState(false); // toggle mockup → chat

  async function handleSend() {
    if (!input.trim()) return;

    // Add user message
    const newChat = [...chat, { role: "user", content: input }];
    setChat(newChat);
    setInput("");
    setStarted(true);

    // Call backend
    const res = await fetch("http://localhost:8000/gemini", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input }),
    });
    const data = await res.json();

    // Add Gemini reply
    setChat((prev) => [...prev, { role: "assistant", content: data.response }]);
  }

  return (
    <div className="flex flex-col h-screen bg-[#0d0d0d] text-white">
      <AnimatePresence mode="wait">
        {!started ? (
          // Mockup state
          <motion.div
            key="intro"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex-1 flex flex-col items-center justify-center text-center"
          >
            <div className="flex flex-col items-center gap-4">
              {/* Gemini logo */}
              <div className="w-16 h-16 rounded-full bg-gray-800 flex items-center justify-center">
                <span className="text-2xl">✨</span>
              </div>
              <h1 className="text-3xl font-bold">Gemini Assistant</h1>
              <p className="text-gray-400">
                Your smart assistant for DSA and problem-solving
              </p>

              {/* Example prompts */}
              <div className="grid grid-cols-2 gap-3 mt-6 w-[500px]">
                {[
                  "Explain dynamic programming",
                  "Give me problems on binary search",
                  "Show easy LeetCode array questions",
                  "Summarize quicksort algorithm",
                ].map((ex, idx) => (
                  <button
                    key={idx}
                    onClick={() => setInput(ex)}
                    className="p-3 bg-[#1a1a1a] rounded-xl text-left hover:bg-[#222]"
                  >
                    {ex}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          // Chat state
          <motion.div
            key="chat"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex-1 overflow-y-auto p-6 space-y-6"
          >
            {chat.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xl px-4 py-3 rounded-2xl ${
                    msg.role === "user"
                      ? "bg-green-600 text-white"
                      : "bg-[#1a1a1a] text-gray-200"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input bar */}
      <div className="p-4 border-t border-gray-800 flex items-center">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask Gemini anything..."
          className="flex-1 bg-[#1a1a1a] px-4 py-3 rounded-xl outline-none"
        />
        <button
          onClick={handleSend}
          className="ml-3 px-5 py-2 rounded-xl bg-green-600 hover:bg-green-700"
        >
          Go
        </button>
      </div>
    </div>
  );
}