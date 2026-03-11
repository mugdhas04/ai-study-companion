"""
API Server for Mini-Game Progress Sync
=======================================
FastAPI server to handle progress updates from embedded mini-games.
Run with: uvicorn api_server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="AI Study Game API", version="1.0.0")

# Enable CORS for mini-games running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class GameProgressUpdate(BaseModel):
    username: str
    game_id: str
    level_id: int
    xp_earned: int
    score: int
    completed: bool


class QuizResult(BaseModel):
    username: str
    game_id: str
    level_id: int
    correct_answers: int
    total_questions: int
    xp_earned: int


class ProgressResponse(BaseModel):
    success: bool
    message: str
    new_xp: int
    new_level: int


# Helper Functions
def load_progress(username: str) -> dict:
    """Load user progress from JSON file."""
    progress_file = f"progress_{username}.json"
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    
    # Default progress structure
    return {
        "xp": 0,
        "level": 1,
        "questions_attempted": 0,
        "correct_answers": 0,
        "current_streak": 0,
        "best_streak": 0,
        "games": {},
        "badges": []
    }


def save_progress(username: str, progress: dict):
    """Save user progress to JSON file."""
    progress_file = f"progress_{username}.json"
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


def calculate_level(xp: int) -> int:
    """Calculate level from XP."""
    return (xp // 100) + 1


# API Endpoints
@app.get("/")
def root():
    """API health check."""
    return {"status": "online", "message": "AI Study Game API"}


@app.get("/api/progress/{username}")
def get_progress(username: str):
    """Get user progress."""
    try:
        progress = load_progress(username)
        return {"success": True, "progress": progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/progress/update")
def update_progress(update: GameProgressUpdate) -> ProgressResponse:
    """
    Update user progress after mini-game completion.
    
    Args:
        update: Game progress data
        
    Returns:
        Updated XP and level info
    """
    try:
        # Load current progress
        progress = load_progress(update.username)
        
        # Add XP
        old_xp = progress["xp"]
        progress["xp"] += update.xp_earned
        new_level = calculate_level(progress["xp"])
        
        # Update game progress
        if update.game_id not in progress["games"]:
            progress["games"][update.game_id] = {
                "completed_levels": 0,
                "levels_completed": [],
                "boss_defeated": False
            }
        
        # Mark level complete if not already
        if update.completed and update.level_id not in progress["games"][update.game_id]["levels_completed"]:
            progress["games"][update.game_id]["levels_completed"].append(update.level_id)
            progress["games"][update.game_id]["completed_levels"] = len(
                progress["games"][update.game_id]["levels_completed"]
            )
            
            # Check if boss level
            if update.level_id == 6:
                progress["games"][update.game_id]["boss_defeated"] = True
        
        # Save progress
        save_progress(update.username, progress)
        
        return ProgressResponse(
            success=True,
            message=f"Progress updated! +{update.xp_earned} XP",
            new_xp=progress["xp"],
            new_level=new_level
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz/submit")
def submit_quiz_result(result: QuizResult) -> ProgressResponse:
    """
    Submit quiz results and update progress.
    
    Args:
        result: Quiz completion data
        
    Returns:
        Updated XP and level info
    """
    try:
        # Load current progress
        progress = load_progress(result.username)
        
        # Update stats
        progress["xp"] += result.xp_earned
        progress["questions_attempted"] += result.total_questions
        progress["correct_answers"] += result.correct_answers
        
        # Update streak
        if result.correct_answers == result.total_questions:
            progress["current_streak"] += 1
            if progress["current_streak"] > progress["best_streak"]:
                progress["best_streak"] = progress["current_streak"]
        else:
            progress["current_streak"] = 0
        
        # Check for badges
        if result.correct_answers == result.total_questions and "perfect_quiz" not in progress["badges"]:
            progress["badges"].append("perfect_quiz")
        
        # Save progress
        new_level = calculate_level(progress["xp"])
        save_progress(result.username, progress)
        
        return ProgressResponse(
            success=True,
            message=f"Quiz completed! +{result.xp_earned} XP",
            new_xp=progress["xp"],
            new_level=new_level
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/leaderboard")
def get_leaderboard():
    """Get top players by XP."""
    try:
        # Load all progress files
        leaderboard = []
        
        for filename in os.listdir('.'):
            if filename.startswith('progress_') and filename.endswith('.json'):
                username = filename.replace('progress_', '').replace('.json', '')
                progress = load_progress(username)
                
                leaderboard.append({
                    "username": username,
                    "xp": progress["xp"],
                    "level": calculate_level(progress["xp"]),
                    "badges": len(progress.get("badges", []))
                })
        
        # Sort by XP
        leaderboard.sort(key=lambda x: x["xp"], reverse=True)
        
        return {"success": True, "leaderboard": leaderboard[:10]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("Starting AI Study Game API on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
