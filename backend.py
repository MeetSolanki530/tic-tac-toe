# Loading Libraries
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Initializing FastAPI
app = FastAPI()

# CORS Handlation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for dev server)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading Secrets From Environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")
base_url = os.getenv("OPENAI_BASE_URL")

# Loading OpenAI Client Library
client = OpenAI(api_key=OPENAI_API_KEY,base_url = base_url)


# PyDantic Models Schemas

class AIMoveRequest(BaseModel):
    board: list[list[str]]
    human_symbol: str
    ai_symbol: str

class AIMoveResponse(BaseModel):
    row: int
    col: int
    reasoning: str

# Game Logics Functions

def get_available_moves(board):
    return [
        {"row": r, "col": c}
        for r in range(3)
        for c in range(3)
        if board[r][c] == ""
    ]

def check_winner(board):
    lines = [
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)],
    ]
    for line in lines:
        a,b,c = line
        if board[a[0]][a[1]] and board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]]:
            return board[a[0]][a[1]]
    return None

def minimax(board, is_max, ai, human):
    winner = check_winner(board)
    if winner == ai: return 1
    if winner == human: return -1
    if not get_available_moves(board): return 0

    if is_max:
        best = -999
        for m in get_available_moves(board):
            board[m["row"]][m["col"]] = ai
            best = max(best, minimax(board, False, ai, human))
            board[m["row"]][m["col"]] = ""
        return best
    else:
        best = 999
        for m in get_available_moves(board):
            board[m["row"]][m["col"]] = human
            best = min(best, minimax(board, True, ai, human))
            board[m["row"]][m["col"]] = ""
        return best

def best_move(board, ai, human):
    best_score = -999
    move = None
    for m in get_available_moves(board):
        board[m["row"]][m["col"]] = ai
        score = minimax(board, False, ai, human)
        board[m["row"]][m["col"]] = ""
        if score > best_score:
            best_score = score
            move = m
    return move

# AI Based reasoning for selected Move

def get_reasoning(board, move, ai, human):
    prompt = f"""
You are an expert Tic-Tac-Toe AI.

Board:
{board}

AI is {ai}, human is {human}.
AI played at {move}.

Explain briefly WHY this move is strong.
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60
    )

    print(res)

    return res.choices[0].message.content.strip()

# Backend API

@app.post("/api/ai-move", response_model=AIMoveResponse)
def ai_move(req: AIMoveRequest):

    move = best_move(req.board, req.ai_symbol, req.human_symbol)

    reasoning = get_reasoning(req.board, move, req.ai_symbol, req.human_symbol)

    return AIMoveResponse(
        row=move["row"],
        col=move["col"],
        reasoning=reasoning
    )

# ─────────────────────────────

if __name__ == "__main__":
    uvicorn.run("hybrid_backend:app", host="0.0.0.0", port=8080, reload=True)