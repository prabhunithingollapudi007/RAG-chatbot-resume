---
title: Prabhu Nithin Gollapudi - Personal AI Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.50.0
app_file: app.py
pinned: true
---

# Prabhu Nithin Gollapudi - Personalized Chatbot
A personalized AI chatbot that responds as if it's Prabhu Nithin Gollapudi himself, using LangChain, FAISS, Streamlit, and Google's Gemini API. It pre-loads Prabhu's resume so anyone can chat with him about his experience, skills, and interests.

## Features
- Auto-loads resume—no uploads needed.
- RAG for accurate, grounded responses.
- Fully free (no paid APIs).

## Setup
1. Clone repo.
2. Add your own `resume.md` (or use the included one).
3. (Optional) Add a profile image named `profile_image.png` to the root directory.
4. `pip install -r requirements.txt`
5. Create a `.env` file with your `GOOGLE_API_KEY`.
6. `streamlit run app.py`

Demo: [Link to HF Space](https://huggingface.co/spaces/prabhu-nithin/chatbot)