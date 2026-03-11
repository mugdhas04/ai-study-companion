"""
Gamification System Module
==========================
Manages XP, levels, badges, and progress tracking for the AI Study Companion.
"""

import json
import os
import streamlit as st

# Path to progress file
PROGRESS_FILE = "progress.json"

# XP thresholds
XP_PER_CORRECT_ANSWER = 10
XP_PER_BOSS_BATTLE = 50
XP_PER_LEVEL = 100

# Badge definitions
BADGES = {
    "first_question": {"name": "First Steps", "description": "Answered your first question", "requirement": 1},
    "ten_correct": {"name": "Quick Learner", "description": "Got 10 correct answers", "requirement": 10},
    "fifty_correct": {"name": "Knowledge Seeker", "description": "Got 50 correct answers", "requirement": 50},
    "hundred_correct": {"name": "Master Mind", "description": "Got 100 correct answers", "requirement": 100},
    "boss_slayer": {"name": "Boss Slayer", "description": "Won your first boss battle", "requirement": "boss_win"},
    "level_5": {"name": "Rising Star", "description": "Reached Level 5", "requirement": "level_5"},
    "level_10": {"name": "Expert Scholar", "description": "Reached Level 10", "requirement": "level_10"},
    "perfect_streak": {"name": "Perfect Streak", "description": "Got 5 correct answers in a row", "requirement": "streak_5"},
}


def get_current_username():
    """Get the current logged-in username."""
    return st.session_state.get("username", "Guest")


def get_progress_file():
    """Get the progress file path for the current user."""
    username = get_current_username()
    if username == "Guest":
        return "progress_guest.json"
    return f"progress_{username}.json"


def get_default_progress():
    """
    Returns the default progress structure for new users.
    """
    return {
        "xp": 0,
        "level": 1,
        "badges": [],
        "questions_attempted": 0,
        "correct_answers": 0,
        "boss_battles_won": 0,
        "current_streak": 0,
        "best_streak": 0,
        "games": {
            "dsa": {"completed_levels": 0, "levels_completed": []},
            "dbms": {"completed_levels": 0, "levels_completed": []},
            "maths": {"completed_levels": 0, "levels_completed": []}
        }
    }


def load_progress():
    """
    Load student progress from JSON file.
    Creates default progress if file doesn't exist.
    
    Returns:
        dict: Progress data containing XP, level, badges, and statistics
    """
    progress_file = get_progress_file()
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)
                # Ensure all keys exist (for backwards compatibility)
                default = get_default_progress()
                for key in default:
                    if key not in progress:
                        progress[key] = default[key]
                return progress
        except (json.JSONDecodeError, IOError):
            return get_default_progress()
    return get_default_progress()


def save_progress(progress):
    """
    Save student progress to JSON file.
    
    Args:
        progress (dict): Progress data to save
    """
    progress_file = get_progress_file()
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)


def calculate_level(xp):
    """
    Calculate level based on XP.
    
    Level progression:
    - 0-99 XP → Level 1
    - 100-199 XP → Level 2
    - 200-299 XP → Level 3
    - etc.
    
    Args:
        xp (int): Current XP points
        
    Returns:
        int: Current level
    """
    return (xp // XP_PER_LEVEL) + 1


def add_xp(amount, is_boss_battle=False):
    """
    Add XP to student progress and update level.
    
    Args:
        amount (int): Base XP amount to add
        is_boss_battle (bool): Whether this is from a boss battle
        
    Returns:
        dict: Updated progress with new XP and level
    """
    progress = load_progress()
    
    # Add XP (boss battles have bonus multiplier)
    xp_gained = XP_PER_BOSS_BATTLE if is_boss_battle else amount
    progress["xp"] += xp_gained
    
    # Update level
    old_level = progress["level"]
    progress["level"] = calculate_level(progress["xp"])
    
    # Check for level-up badges
    if progress["level"] >= 5 and "level_5" not in progress["badges"]:
        progress["badges"].append("level_5")
    if progress["level"] >= 10 and "level_10" not in progress["badges"]:
        progress["badges"].append("level_10")
    
    save_progress(progress)
    
    return {
        "progress": progress,
        "xp_gained": xp_gained,
        "leveled_up": progress["level"] > old_level,
        "new_level": progress["level"]
    }


def record_answer(is_correct, is_boss_battle=False, game_id=None):
    """
    Record an answer attempt and update statistics.
    
    Args:
        is_correct (bool): Whether the answer was correct
        is_boss_battle (bool): Whether this was a boss battle question
        game_id (str): Optional game identifier for game-specific tracking
        
    Returns:
        dict: Result containing XP gained, badges earned, etc.
    """
    progress = load_progress()
    result = {
        "xp_gained": 0,
        "new_badges": [],
        "leveled_up": False,
        "new_level": progress["level"]
    }
    
    # Update attempt count
    progress["questions_attempted"] += 1
    
    if is_correct:
        progress["correct_answers"] += 1
        progress["current_streak"] += 1
        
        # Update best streak
        if progress["current_streak"] > progress["best_streak"]:
            progress["best_streak"] = progress["current_streak"]
        
        # Track boss battle wins
        if is_boss_battle:
            progress["boss_battles_won"] += 1
        
        # Add XP
        xp_amount = XP_PER_BOSS_BATTLE if is_boss_battle else XP_PER_CORRECT_ANSWER
        progress["xp"] += xp_amount
        result["xp_gained"] = xp_amount
        
        # Update level
        old_level = progress["level"]
        progress["level"] = calculate_level(progress["xp"])
        result["new_level"] = progress["level"]
        result["leveled_up"] = progress["level"] > old_level
        
        # Check for badges
        new_badges = check_badges(progress)
        for badge in new_badges:
            if badge not in progress["badges"]:
                progress["badges"].append(badge)
                result["new_badges"].append(badge)
    else:
        # Reset streak on wrong answer
        progress["current_streak"] = 0
    
    save_progress(progress)
    result["progress"] = progress
    
    return result


def check_badges(progress):
    """
    Check which badges the student has earned.
    
    Args:
        progress (dict): Current progress data
        
    Returns:
        list: List of badge keys earned
    """
    earned_badges = []
    
    # First question badge
    if progress["questions_attempted"] >= 1:
        earned_badges.append("first_question")
    
    # Correct answer milestones
    if progress["correct_answers"] >= 10:
        earned_badges.append("ten_correct")
    if progress["correct_answers"] >= 50:
        earned_badges.append("fifty_correct")
    if progress["correct_answers"] >= 100:
        earned_badges.append("hundred_correct")
    
    # Boss slayer badge
    if progress["boss_battles_won"] >= 1:
        earned_badges.append("boss_slayer")
    
    # Level badges
    if progress["level"] >= 5:
        earned_badges.append("level_5")
    if progress["level"] >= 10:
        earned_badges.append("level_10")
    
    # Streak badge
    if progress["best_streak"] >= 5:
        earned_badges.append("perfect_streak")
    
    return earned_badges


def get_badge_info(badge_key):
    """
    Get display information for a badge.
    
    Args:
        badge_key (str): Badge identifier
        
    Returns:
        dict: Badge name and description
    """
    if badge_key in BADGES:
        return BADGES[badge_key]
    return {"name": badge_key, "description": "Achievement unlocked!"}


def calculate_accuracy(progress):
    """
    Calculate the student's accuracy percentage.
    
    Args:
        progress (dict): Progress data
        
    Returns:
        float: Accuracy percentage (0-100)
    """
    if progress["questions_attempted"] == 0:
        return 0.0
    return (progress["correct_answers"] / progress["questions_attempted"]) * 100


def get_progress_summary():
    """
    Get a formatted summary of student progress.
    
    Returns:
        dict: Summary containing all progress metrics
    """
    progress = load_progress()
    accuracy = calculate_accuracy(progress)
    
    # Calculate XP needed for next level
    current_level_xp = (progress["level"] - 1) * XP_PER_LEVEL
    next_level_xp = progress["level"] * XP_PER_LEVEL
    xp_progress = progress["xp"] - current_level_xp
    xp_needed = XP_PER_LEVEL
    
    return {
        "xp": progress["xp"],
        "level": progress["level"],
        "badges": progress["badges"],
        "badge_count": len(progress["badges"]),
        "questions_attempted": progress["questions_attempted"],
        "correct_answers": progress["correct_answers"],
        "accuracy": round(accuracy, 1),
        "current_streak": progress["current_streak"],
        "best_streak": progress["best_streak"],
        "boss_battles_won": progress["boss_battles_won"],
        "xp_progress": xp_progress,
        "xp_needed": xp_needed,
        "progress_percentage": (xp_progress / xp_needed) * 100
    }


def reset_progress():
    """
    Reset all progress to default values.
    """
    save_progress(get_default_progress())


def get_game_progress(game_id):
    """
    Get progress for a specific game (predefined or dynamic).
    
    Args:
        game_id (str): Game identifier ('dsa', 'dbms', 'maths', or dynamic course ID)
        
    Returns:
        dict: Game progress containing completed_levels and levels_completed list
    """
    progress = load_progress()
    
    # Ensure games structure exists
    if "games" not in progress:
        progress["games"] = {
            "dsa": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False},
            "dbms": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False},
            "maths": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False}
        }
        save_progress(progress)
    
    # Ensure specific game exists (supports dynamic courses)
    if game_id not in progress["games"]:
        progress["games"][game_id] = {
            "completed_levels": 0, 
            "levels_completed": [],
            "boss_defeated": False
        }
        save_progress(progress)
    
    return progress["games"][game_id]


def complete_level(game_id, level_id):
    """
    Mark a level as completed for a specific game (predefined or dynamic).
    
    Args:
        game_id (str): Game identifier ('dsa', 'dbms', 'maths', or dynamic course ID)
        level_id (int): Level number completed
        
    Returns:
        dict: Updated game progress
    """
    progress = load_progress()
    
    # Ensure structure exists
    if "games" not in progress:
        progress["games"] = {
            "dsa": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False},
            "dbms": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False},
            "maths": {"completed_levels": 0, "levels_completed": [], "boss_defeated": False}
        }
    
    # Initialize game if it doesn't exist (supports dynamic courses)
    if game_id not in progress["games"]:
        progress["games"][game_id] = {
            "completed_levels": 0, 
            "levels_completed": [],
            "boss_defeated": False
        }
    
    # Add level if not already completed
    if level_id not in progress["games"][game_id]["levels_completed"]:
        progress["games"][game_id]["levels_completed"].append(level_id)
        progress["games"][game_id]["completed_levels"] = len(progress["games"][game_id]["levels_completed"])
        
        # Check if boss level (level 6) was completed
        if level_id == 6:
            progress["games"][game_id]["boss_defeated"] = True
    
    save_progress(progress)
    return progress["games"][game_id]


def get_dynamic_courses_progress():
    """
    Get progress for all dynamic (non-predefined) courses.
    
    Returns:
        dict: Dictionary of dynamic course progress keyed by course_id
    """
    progress = load_progress()
    predefined = {"dsa", "dbms", "maths"}
    
    dynamic_progress = {}
    if "games" in progress:
        for game_id, game_data in progress["games"].items():
            if game_id not in predefined:
                dynamic_progress[game_id] = game_data
    
    return dynamic_progress


def get_total_game_progress():
    """
    Get aggregated progress across all games.
    
    Returns:
        dict: Total levels completed, games started, etc.
    """
    progress = load_progress()
    
    if "games" not in progress:
        return {"total_levels": 0, "games_started": 0, "games_completed": 0}
    
    total_levels = 0
    games_started = 0
    games_completed = 0
    
    for game_id, game_data in progress["games"].items():
        levels = len(game_data.get("levels_completed", []))
        total_levels += levels
        if levels > 0:
            games_started += 1
        if levels >= 6:  # 6 levels per game including boss
            games_completed += 1
    
    return {
        "total_levels": total_levels,
        "games_started": games_started,
        "games_completed": games_completed
    }
