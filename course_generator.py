"""
Course Generator Module
=======================
Dynamically generates gamified course structures using the Gemini API.
Allows users to create learning paths for any topic.
"""

import json
import os
import streamlit as st
from explainer import get_client, MODEL_NAME

# Cache file for generated courses
COURSES_CACHE_FILE = "generated_courses.json"


def load_cached_courses():
    """
    Load cached courses from JSON file.
    
    Returns:
        dict: Dictionary of cached courses keyed by topic
    """
    if os.path.exists(COURSES_CACHE_FILE):
        try:
            with open(COURSES_CACHE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cached_courses(courses):
    """
    Save courses to cache file.
    
    Args:
        courses (dict): Dictionary of courses to cache
    """
    with open(COURSES_CACHE_FILE, 'w') as f:
        json.dump(courses, f, indent=2)


def get_cache_key(topic, difficulty):
    """
    Generate a cache key for a topic/difficulty combination.
    
    Args:
        topic (str): Course topic
        difficulty (str): Difficulty level
        
    Returns:
        str: Cache key
    """
    return f"{topic.lower().strip()}_{difficulty.lower()}"


def generate_course(topic, difficulty="Intermediate"):
    """
    Generate a gamified course structure for any topic using Gemini API.
    
    Args:
        topic (str): The topic to create a course for
        difficulty (str): Difficulty level (Beginner, Intermediate, Advanced, Expert)
        
    Returns:
        dict: Course structure with title, levels, and boss battle
              Example: {
                  "course_title": "Machine Learning Quest",
                  "course_id": "machine_learning_quest",
                  "topic": "Machine Learning",
                  "difficulty": "Intermediate",
                  "color_1": "#6bcb77",
                  "color_2": "#4d96ff",
                  "levels": [
                      {"id": 1, "name": "Introduction to ML", "topic": "..."},
                      ...
                  ],
                  "boss_battle": {"topic": "...", "challenge": "..."}
              }
    """
    # Check cache first
    cache_key = get_cache_key(topic, difficulty)
    cached_courses = load_cached_courses()
    
    if cache_key in cached_courses:
        return cached_courses[cache_key]
    
    # Generate new course using Anthropic Claude
    try:
        client = get_client()
        
        prompt = f"""You are an expert curriculum designer creating a gamified learning course.

Topic: {topic}
Difficulty Level: {difficulty}

Create a structured learning path with an appropriate number of levels (between 3 and 8) based on the topic's complexity. Simpler topics need fewer levels, complex topics need more. Each level should build upon the previous one. The course should feel like a game quest with increasing challenge.

Respond ONLY with valid JSON in this exact format:
{{
    "course_title": "Creative Quest-Style Title",
    "levels": [
        "Level 1 Topic Name - Foundation concepts",
        "Level 2 Topic Name - Building blocks", 
        "Level 3 Topic Name - More advanced concepts"
    ],
    "boss_battle": "Final challenge description that tests all concepts learned"
}}

Requirements:
- Course title should be catchy and game-like (e.g., "Machine Learning Quest", "Python Odyssey")
- Include between 3 and 8 levels depending on topic complexity
- Level names should be specific subtopics, not generic
- Each level should naturally lead to the next
- Boss battle should be a comprehensive challenge
- Tailor complexity to the {difficulty} level
- Make it educational but engaging

Return ONLY the JSON, no explanations or markdown formatting."""

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.content[0].text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()
        
        # Parse JSON response
        course_data = json.loads(response_text)
        
        # Build structured course object
        course = build_course_structure(topic, difficulty, course_data)
        
        # Cache the course
        cached_courses[cache_key] = course
        save_cached_courses(cached_courses)
        
        return course
        
    except json.JSONDecodeError as e:
        # Fallback course structure if JSON parsing fails
        return build_fallback_course(topic, difficulty)
    except Exception as e:
        print(f"Course generation error: {e}")
        return build_fallback_course(topic, difficulty)


def build_course_structure(topic, difficulty, course_data):
    """
    Build a complete course structure from AI-generated data.
    
    Args:
        topic (str): Original topic
        difficulty (str): Difficulty level
        course_data (dict): AI-generated course data
        
    Returns:
        dict: Complete course structure
    """
    # Generate course ID from title
    course_title = course_data.get("course_title", f"{topic} Quest")
    course_id = course_title.lower().replace(" ", "_").replace("-", "_")
    course_id = "".join(c for c in course_id if c.isalnum() or c == "_")
    
    # Assign colors based on topic hash for variety
    colors = get_course_colors(topic)
    
    # Build levels array
    levels = []
    level_names = course_data.get("levels", [])
    
    # Support 3-8 levels based on what AI returns
    num_levels = min(max(len(level_names), 3), 8)
    
    for i, level_name in enumerate(level_names[:num_levels], 1):
        levels.append({
            "id": i,
            "name": level_name.split(" - ")[0] if " - " in level_name else level_name,
            "icon": f"{i:02d}",
            "topic": level_name,
            "is_boss": False
        })
    
    # Add boss battle as final level
    boss_level_id = len(levels) + 1
    boss_battle = course_data.get("boss_battle", f"Master Challenge: {topic}")
    levels.append({
        "id": boss_level_id,
        "name": "BOSS BATTLE",
        "icon": "BOSS",
        "topic": boss_battle,
        "is_boss": True
    })
    
    return {
        "course_title": course_title,
        "course_id": course_id,
        "topic": topic,
        "difficulty": difficulty,
        "color_1": colors[0],
        "color_2": colors[1],
        "levels": levels,
        "total_levels": len(levels),
        "boss_battle": boss_battle,
        "is_dynamic": True
    }


def build_fallback_course(topic, difficulty):
    """
    Build a fallback course structure when AI generation fails.
    
    Args:
        topic (str): Course topic
        difficulty (str): Difficulty level
        
    Returns:
        dict: Basic course structure
    """
    course_title = f"{topic} Quest"
    course_id = topic.lower().replace(" ", "_")
    course_id = "".join(c for c in course_id if c.isalnum() or c == "_")
    
    colors = get_course_colors(topic)
    
    levels = [
        {"id": 1, "name": "Foundations", "icon": "01", "topic": f"Introduction to {topic}", "is_boss": False},
        {"id": 2, "name": "Core Concepts", "icon": "02", "topic": f"Core concepts of {topic}", "is_boss": False},
        {"id": 3, "name": "Intermediate", "icon": "03", "topic": f"Intermediate {topic} concepts", "is_boss": False},
        {"id": 4, "name": "Advanced", "icon": "04", "topic": f"Advanced {topic} techniques", "is_boss": False},
        {"id": 5, "name": "BOSS BATTLE", "icon": "BOSS", "topic": f"Ultimate {topic} Challenge", "is_boss": True}
    ]
    
    return {
        "course_title": course_title,
        "course_id": course_id,
        "topic": topic,
        "difficulty": difficulty,
        "color_1": colors[0],
        "color_2": colors[1],
        "levels": levels,
        "total_levels": len(levels),
        "boss_battle": f"Ultimate {topic} Challenge",
        "is_dynamic": True
    }


def get_course_colors(topic):
    """
    Generate consistent colors for a topic based on its hash.
    
    Args:
        topic (str): Course topic
        
    Returns:
        tuple: (color_1, color_2) hex color codes
    """
    color_palettes = [
        ("#ff6b6b", "#ffd93d"),  # Red-Yellow
        ("#6bcb77", "#4d96ff"),  # Green-Blue
        ("#a855f7", "#ec4899"),  # Purple-Pink
        ("#00d4ff", "#7c3aed"),  # Cyan-Violet
        ("#f97316", "#eab308"),  # Orange-Yellow
        ("#14b8a6", "#06b6d4"),  # Teal-Cyan
        ("#8b5cf6", "#d946ef"),  # Violet-Fuchsia
        ("#10b981", "#3b82f6"),  # Emerald-Blue
    ]
    
    # Use topic hash to consistently assign colors
    topic_hash = sum(ord(c) for c in topic.lower())
    palette_idx = topic_hash % len(color_palettes)
    
    return color_palettes[palette_idx]


def get_user_dynamic_courses():
    """
    Get list of dynamic courses the current user has started.
    
    Returns:
        list: List of course dictionaries
    """
    from gamification import load_progress
    
    progress = load_progress()
    dynamic_courses = []
    
    if "games" in progress:
        for game_id, game_data in progress["games"].items():
            # Check if this is a dynamic course (not dsa, dbms, maths)
            if game_id not in ["dsa", "dbms", "maths"]:
                # Try to find course info in cache
                cached_courses = load_cached_courses()
                course_info = None
                
                # Search cache for this course
                for key, course in cached_courses.items():
                    if course.get("course_id") == game_id:
                        course_info = course
                        break
                
                if course_info:
                    course_info["progress"] = game_data
                    dynamic_courses.append(course_info)
    
    return dynamic_courses


def delete_generated_course(course_id):
    """
    Delete a generated course from cache.
    
    Args:
        course_id (str): Course identifier to delete
    """
    cached_courses = load_cached_courses()
    
    # Find and remove course by ID
    keys_to_remove = []
    for key, course in cached_courses.items():
        if course.get("course_id") == course_id:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del cached_courses[key]
    
    save_cached_courses(cached_courses)
