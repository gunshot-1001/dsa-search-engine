DSA Search & AI Assistant for BNP Paribas

🚀 Master DSA faster! Curated problems from LeetCode & HackerRank, ranked by relevance using NLP and TF-IDF.
🤖 Gemini AI Assistant explains algorithms, suggests practice problems, and helps debug your solutions.
📊 Track your progress with user accounts and difficulty filters.
💻 Interactive dashboard built with React, TailwindCSS, and Framer Motion.
⚡ End-to-end pipeline: web scraping → preprocessing → search indexing → AI-powered guidance.

Features : 
Web Scraping & Problem Database - 
     Scrapes HackerRank and LeetCode problems using Selenium.
     Stores title, URL, domain, tag, and snippet.
Preprocessing & Search Index - 
     preprocessing/build_index.py:
     Normalizes problem text (Title + Domain + Tag).
     Builds TF-IDF vectorizer and sparse matrix.
     Saves index map and models for fast search.
Search Engine - 
     Search endpoint /search?q=<query> ranks problems by relevance.
     Supports difficulty filtering (Easy, Medium, Hard).
User Accounts & Progress - 
     Sign up / login with JWT authentication.
     Track solved/in-progress problems.
AI Learning Assistant - 
     Gemini chat interface (/gemini) for DSA guidance.
     Can summarize concepts, suggest practice problems, and debug user code.
Frontend - 
     React + TailwindCSS, fully responsive.
     Framer Motion for smooth chat animations.
     Dashboard with search, filters, and AI assistant.
