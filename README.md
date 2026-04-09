# NEXUS AI Tic-Tac-Toe

A simple and fast Tic-Tac-Toe game powered by a perfect AI engine. The system focuses on clean logic, reliable gameplay, and an optional AI explanation layer for better user experience.

---

## 1. Project Structure

```bash
.
├── backend.py        # FastAPI backend with AI logic
├── index.html        # Frontend UI
└── README.md
```

---

## 2. How It Works

The game uses a hybrid approach.

The move decision is handled by the Minimax algorithm. This ensures the AI always plays the best possible move and never makes mistakes.

An optional OpenAI layer is used only to generate explanations for moves. It does not control gameplay.

This separation keeps the system stable and accurate while still giving an intelligent feel.

---

## 3. How to Use

1. Install dependencies

```bash
pip install fastapi uvicorn openai
```

2. Run the backend

```bash
python backend.py
```

3. Open the frontend

Open the `index.html` file in your browser.

4. Play the game

Click on any empty cell to make your move. The AI will respond instantly.

---

## 4. Feature Description

* Unbeatable AI
  Uses Minimax algorithm to ensure optimal moves every time

* Valid Move Selection
  AI only chooses from available cells and never overlaps

* Fast Response
  No heavy computation or external dependency for gameplay

* Optional AI Reasoning
  OpenAI can generate short explanations for each move

* Clean Architecture
  Simple backend and frontend separation for easy understanding and extension

---
