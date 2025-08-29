DSA Search & AI Assistant

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

How to run from the start:
1. Run both Web Scrapping codes for both Hackerrank and Leeetcode on initalized public sites which dont require login to access. Scraping them for Title,Domain,Tag,URL. Limit set for 200 entries for demo steup, both scrapers then initalize it in JSON format within the data folder.
2. Run preprocess.py to preprocess these to clean HTML tags and normalize problem text
3. Run the build_index.py to create a single processed file integrating both Hackerrank and Leetcode problems and build TF-IDF vectorizer. Creates a index map for better searching.
4. To run backend use uvicorn.exe app.main:app. Starts backend which contains the Main.py code consisting of 
->Links to Authnetication of user when user signs up or login. Uses encrpytion using bycrypt to create a address using secret key and password for secure logins.
->Attaching the gemini API key which includes two trained consoles - Learning path and Explain code
->A database in db.py which includes SQLlite to store users and progress data.
5. For Frontend run npm run dev which starts 
-> The landing page consisting of signup and login button and restricts access to use search until login. 
-> Clicking on button will redirect to Signup/login page where user can login or create account.
-> After Logging in Dashboard provides a Search Bar where user can search keywords and in turn find problem statment with link. Also has filters to select Diffculty in the problems.
-> In bottom left has a Gemini button , when clicked redirects to a new page which includes suggestions for user to start and has two consoles one which provides learning path and other to explain code.
-> To exit you can come back to main Dashboard and then logout using the button below.

To start the code directly - Use the start.bat to start both frontend and backend or npm run dev in terminal
