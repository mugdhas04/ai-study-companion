"""
AI STUDY GAME HUB - Main Application
=====================================
A gamified learning platform with multiple subject games.
Each subject is an independent mini-game with levels and boss battles.

Run with: streamlit run app.py
"""

import streamlit as st
from gamification import get_progress_summary, get_game_progress, get_dynamic_courses_progress
from login import render_login_page, is_logged_in, logout
from profile import render_profile_page

# Import game modules
from dsa_game import render_dsa_game
from dbms_game import render_dbms_game
from maths_game import render_maths_game

# Import dynamic course modules
from course_generator import generate_course, get_user_dynamic_courses, load_cached_courses
from dynamic_game import render_dynamic_game

# Page configuration
st.set_page_config(
    page_title="AI STUDY GAME HUB",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cyberpunk Game Hub CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Press+Start+2P&display=swap');
    
    /* Dark cyberpunk theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a1628 100%);
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Hub Title */
    .hub-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 50%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 8px;
        margin: 30px 0 10px 0;
        animation: titlePulse 3s ease-in-out infinite;
    }
    
    @keyframes titlePulse {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.5)); }
        50% { filter: drop-shadow(0 0 40px rgba(0, 212, 255, 0.8)); }
    }
    
    .hub-subtitle {
        font-family: 'Rajdhani', sans-serif;
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }
    
    /* Player Stats Bar */
    .stats-bar {
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 212, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 15px;
        padding: 20px 40px;
        margin: 0 auto 30px auto;
        max-width: 700px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #00ff88;
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }
    
    /* Game Card */
    .game-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 25px;
        padding: 35px 25px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 3px solid transparent;
        height: 320px;
        cursor: pointer;
    }
    
    .game-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 22px;
        padding: 3px;
        background: var(--card-gradient);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    .game-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    /* Clickable card button styling */
    .clickable-card-btn button {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%) !important;
        border-radius: 25px !important;
        padding: 35px 25px !important;
        text-align: center !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: 3px solid transparent !important;
        height: 320px !important;
        cursor: pointer !important;
        width: 100% !important;
    }
    
    .clickable-card-btn button:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    }
    
    .clickable-card-btn.dsa button {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 20px rgba(255,107,107,0.3) !important;
    }
    
    .clickable-card-btn.dbms button {
        border-color: #4d96ff !important;
        box-shadow: 0 0 20px rgba(77,150,255,0.3) !important;
    }
    
    .clickable-card-btn.maths button {
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px rgba(168,85,247,0.3) !important;
    }
    
    /* Card click zone - hide the play button and make card clickable */
    .card-click-zone {
        margin-top: -50px;
        position: relative;
        z-index: 10;
    }
    
    .card-click-zone button {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        color: #fff !important;
        font-size: 1.5rem !important;
        padding: 15px !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .card-click-zone button:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1)) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important;
    }
    
    .game-card.dsa {
        --card-gradient: linear-gradient(135deg, #ff6b6b, #ffd93d);
    }
    
    .game-card.dbms {
        --card-gradient: linear-gradient(135deg, #6bcb77, #4d96ff);
    }
    
    .game-card.maths {
        --card-gradient: linear-gradient(135deg, #a855f7, #ec4899);
    }
    
    .game-icon {
        font-size: 4rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .game-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 8px;
        letter-spacing: 2px;
    }
    
    .game-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        color: #888;
        margin-bottom: 20px;
    }
    
    .game-progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 10px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .game-progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .game-progress-fill.dsa {
        background: linear-gradient(90deg, #ff6b6b, #ffd93d);
    }
    
    .game-progress-fill.dbms {
        background: linear-gradient(90deg, #6bcb77, #4d96ff);
    }
    
    .game-progress-fill.maths {
        background: linear-gradient(90deg, #a855f7, #ec4899);
    }
    
    .game-levels {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 20px;
    }
    
    /* Footer */
    .hub-footer {
        text-align: center;
        padding: 30px;
        color: #333;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 2px;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 25px;
        padding: 12px 30px;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'current_game' not in st.session_state:
        st.session_state.current_game = None
    if 'current_level' not in st.session_state:
        st.session_state.current_level = None
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = None
    if 'show_quiz' not in st.session_state:
        st.session_state.show_quiz = False
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = []
    if 'explanation_result' not in st.session_state:
        st.session_state.explanation_result = None
    if 'boss_mode' not in st.session_state:
        st.session_state.boss_mode = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'flipped_cards' not in st.session_state:
        st.session_state.flipped_cards = {}
    # Dynamic course states
    if 'dynamic_course' not in st.session_state:
        st.session_state.dynamic_course = None
    if 'generating_course' not in st.session_state:
        st.session_state.generating_course = False


def render_game_hub():
    """Render the main game hub landing page."""
    summary = get_progress_summary()
    user_data = st.session_state.get("user_data", {})
    username = st.session_state.get("username", "")
    
    # Top bar with user info and profile button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        avatar = user_data.get("avatar", "P")
        avatar_color = user_data.get("avatar_color", "#00ff88")
        name = user_data.get("display_name", "Player")
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: {avatar_color}; display: flex; align-items: center; justify-content: center; font-family: 'Orbitron', sans-serif; font-weight: 700; color: #0a0a0f;">{avatar}</div>
                <span style="font-family: 'Rajdhani', sans-serif; color: #888;">{name}</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("PROFILE", key="profile_btn"):
            st.session_state.show_profile = True
            st.rerun()
    
    # Title
    st.markdown('<h1 class="hub-title">AI STUDY GAME HUB</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hub-subtitle">Select Your Learning Quest</p>', unsafe_allow_html=True)
    
    # Player Stats Bar
    st.markdown(f'''
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{summary["level"]}</div>
                <div class="stat-label">Level</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{summary["xp"]}</div>
                <div class="stat-label">Total XP</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{summary["accuracy"]}%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{len(summary["badges"])}</div>
                <div class="stat-label">Badges</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # ==================== CONTINUE LEARNING SECTION ====================
    # Collect all in-progress courses (started but not completed)
    in_progress = []
    
    # Check predefined games
    predefined = [
        {"id": "dsa", "name": "DSA ADVENTURE", "color": "#ff6b6b", "gradient": "linear-gradient(135deg, #ff6b6b, #ffd93d)"},
        {"id": "dbms", "name": "DATABASE QUEST", "color": "#4d96ff", "gradient": "linear-gradient(135deg, #6bcb77, #4d96ff)"},
        {"id": "maths", "name": "MATH ARENA", "color": "#a855f7", "gradient": "linear-gradient(135deg, #a855f7, #ec4899)"}
    ]
    
    for game in predefined:
        gp = get_game_progress(game["id"])
        completed = gp.get("completed_levels", 0)
        # In progress = started (>0) but not finished (<6)
        if completed > 0 and completed < 6:
            in_progress.append({
                "id": game["id"],
                "name": game["name"],
                "color": game["color"],
                "gradient": game["gradient"],
                "progress": gp,
                "is_dynamic": False,
                "course": None
            })
    
    # Check dynamic courses
    user_dynamic_courses = get_user_dynamic_courses()
    for course in user_dynamic_courses:
        gp = get_game_progress(course["course_id"])
        completed = gp.get("completed_levels", 0)
        total_lvls = course.get("total_levels", len(course.get("levels", [])))
        if completed > 0 and completed < total_lvls:
            colors = course.get("colors", {"primary": "#00d4ff", "secondary": "#00ff88"})
            in_progress.append({
                "id": course["course_id"],
                "name": course.get("course_title", "AI Course").upper(),
                "color": colors.get("primary", "#00d4ff"),
                "gradient": f"linear-gradient(135deg, {colors.get('primary', '#00d4ff')}, {colors.get('secondary', '#00ff88')})",
                "progress": gp,
                "is_dynamic": True,
                "course": course,
                "total_levels": total_lvls
            })
    
    # Show Continue Learning section if there are in-progress courses
    if in_progress:
        st.markdown("""
            <h2 style="font-family: 'Orbitron', sans-serif; color: #ffd700; font-size: 1.5rem; 
                letter-spacing: 3px; margin: 40px 0 20px 0; text-align: center;">
                CONTINUE LEARNING
            </h2>
        """, unsafe_allow_html=True)
        
        # Show up to 3 in-progress courses
        cols = st.columns(min(len(in_progress), 3))
        for idx, course_data in enumerate(in_progress[:3]):
            with cols[idx]:
                gp = course_data["progress"]
                total_lvls = course_data.get("total_levels", 6)
                pct = (gp["completed_levels"] / total_lvls) * 100
                next_level = gp["completed_levels"] + 1
                
                # Add dynamic CSS for this course
                st.markdown(f'''
                    <style>
                        .continue-card-{idx} {{
                            --card-gradient: {course_data["gradient"]};
                        }}
                        .continue-fill-{idx} {{
                            background: {course_data["gradient"]};
                        }}
                    </style>
                    <div class="game-card continue-card-{idx}" style="height: auto; padding: 25px;">
                        <span style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: {course_data["color"]};">
                            {"[AI]" if course_data["is_dynamic"] else ""} LEVEL {next_level}
                        </span>
                        <div class="game-title" style="font-size: 1.1rem; margin: 10px 0;">{course_data["name"][:20]}</div>
                        <div class="game-progress-container">
                            <div class="continue-fill-{idx}" style="width: {pct}%; height: 100%; border-radius: 10px;"></div>
                        </div>
                        <div class="game-levels">{gp["completed_levels"]}/{total_lvls} Complete</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"RESUME", key=f"resume_{course_data['id']}", use_container_width=True):
                    if course_data["is_dynamic"]:
                        st.session_state.dynamic_course = course_data["course"]
                        st.session_state.current_game = "dynamic"
                    else:
                        st.session_state.current_game = course_data["id"]
                    st.session_state.current_level = None
                    st.rerun()
    
    # ==================== FEATURED GAMES SECTION ====================
    st.markdown("""
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 1.5rem; 
            letter-spacing: 3px; margin: 40px 0 20px 0; text-align: center;">
            FEATURED GAMES
        </h2>
    """, unsafe_allow_html=True)
    
    # Game progress for each game
    dsa_progress = get_game_progress("dsa")
    dbms_progress = get_game_progress("dbms")
    maths_progress = get_game_progress("maths")
    
    # Game Selection Cards - Clickable cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dsa_pct = (dsa_progress["completed_levels"] / 6) * 100
        with st.container():
            st.markdown(f'''
                <div class="game-card dsa" style="cursor: pointer;">
                    <span class="game-icon" style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #ff6b6b;">DSA</span>
                    <div class="game-title">DSA ADVENTURE</div>
                    <div class="game-subtitle">Master Data Structures & Algorithms</div>
                    <div class="game-progress-container">
                        <div class="game-progress-fill dsa" style="width: {dsa_pct}%;"></div>
                    </div>
                    <div class="game-levels">{dsa_progress["completed_levels"]}/6 Levels Complete</div>
                </div>
            ''', unsafe_allow_html=True)
            # Invisible button overlay
            st.markdown('<div class="card-click-zone">', unsafe_allow_html=True)
            if st.button("▶", key="play_dsa", use_container_width=True, help="Click to enter DSA Adventure"):
                st.session_state.current_game = "dsa"
                st.session_state.current_level = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        dbms_pct = (dbms_progress["completed_levels"] / 6) * 100
        with st.container():
            st.markdown(f'''
                <div class="game-card dbms" style="cursor: pointer;">
                    <span class="game-icon" style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #4d96ff;">SQL</span>
                    <div class="game-title">DATABASE QUEST</div>
                    <div class="game-subtitle">Conquer Database Management</div>
                    <div class="game-progress-container">
                        <div class="game-progress-fill dbms" style="width: {dbms_pct}%;"></div>
                    </div>
                    <div class="game-levels">{dbms_progress["completed_levels"]}/6 Levels Complete</div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown('<div class="card-click-zone">', unsafe_allow_html=True)
            if st.button("▶", key="play_dbms", use_container_width=True, help="Click to enter Database Quest"):
                st.session_state.current_game = "dbms"
                st.session_state.current_level = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        maths_pct = (maths_progress["completed_levels"] / 6) * 100
        with st.container():
            st.markdown(f'''
                <div class="game-card maths" style="cursor: pointer;">
                    <span class="game-icon" style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #a855f7;">MATH</span>
                    <div class="game-title">MATH ARENA</div>
                    <div class="game-subtitle">Challenge Mathematical Concepts</div>
                    <div class="game-progress-container">
                        <div class="game-progress-fill maths" style="width: {maths_pct}%;"></div>
                    </div>
                    <div class="game-levels">{maths_progress["completed_levels"]}/6 Levels Complete</div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown('<div class="card-click-zone">', unsafe_allow_html=True)
            if st.button("▶", key="play_maths", use_container_width=True, help="Click to enter Math Arena"):
                st.session_state.current_game = "maths"
                st.session_state.current_level = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== CREATE NEW COURSE SECTION ====================
    st.markdown("""
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00d4ff; font-size: 1.5rem; 
            letter-spacing: 3px; margin: 50px 0 20px 0; text-align: center;">
            CREATE NEW AI COURSE
        </h2>
        <p style="font-family: 'Rajdhani', sans-serif; color: #666; text-align: center; 
            font-size: 1rem; margin-bottom: 25px;">
            Enter any topic and let AI generate a personalized learning adventure
        </p>
    """, unsafe_allow_html=True)
    
    # Course creation form
    create_col1, create_col2, create_col3 = st.columns([2, 1, 1])
    
    with create_col1:
        topic_input = st.text_input(
            "Topic",
            placeholder="e.g., Machine Learning, Web Development, Physics...",
            key="topic_input",
            label_visibility="collapsed"
        )
    
    with create_col2:
        difficulty = st.selectbox(
            "Difficulty",
            options=["beginner", "intermediate", "advanced"],
            index=1,
            key="difficulty_select",
            label_visibility="collapsed"
        )
    
    with create_col3:
        generate_btn = st.button(
            "GENERATE COURSE",
            key="generate_course_btn",
            use_container_width=True,
            disabled=st.session_state.generating_course
        )
    
    # Handle course generation
    if generate_btn and topic_input.strip():
        st.session_state.generating_course = True
        with st.spinner("AI is crafting your learning adventure..."):
            course = generate_course(topic_input.strip(), difficulty)
            if course:
                st.session_state.dynamic_course = course
                st.session_state.current_game = "dynamic"
                st.session_state.current_level = None
                st.session_state.generating_course = False
                st.rerun()
            else:
                st.error("Failed to generate course. Please try again.")
                st.session_state.generating_course = False
    
    # ==================== MY GENERATED COURSES SECTION ====================
    user_courses = get_user_dynamic_courses()
    
    if user_courses:
        st.markdown("""
            <h2 style="font-family: 'Orbitron', sans-serif; color: #ff00ff; font-size: 1.5rem; 
                letter-spacing: 3px; margin: 50px 0 20px 0; text-align: center;">
                MY GENERATED COURSES
            </h2>
        """, unsafe_allow_html=True)
        
        # Display courses in rows of 3
        course_list = user_courses
        for i in range(0, len(course_list), 3):
            cols = st.columns(3)
            for j, course in enumerate(course_list[i:i+3]):
                with cols[j]:
                    course_progress = get_game_progress(course["course_id"])
                    total_lvls = course.get("total_levels", len(course.get("levels", [])))
                    course_pct = (course_progress["completed_levels"] / total_lvls) * 100 if total_lvls > 0 else 0
                    colors = course.get("colors", {"primary": "#00d4ff", "secondary": "#00ff88"})
                    
                    # Custom CSS for this course card
                    st.markdown(f'''
                        <style>
                            .game-card.course-{course["course_id"][:8]} {{
                                --card-gradient: linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]});
                            }}
                            .game-progress-fill.course-{course["course_id"][:8]} {{
                                background: linear-gradient(90deg, {colors["primary"]}, {colors["secondary"]});
                            }}
                        </style>
                        <div class="game-card course-{course["course_id"][:8]}">
                            <span class="game-icon" style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: {colors["primary"]};">AI</span>
                            <div class="game-title">{course["course_title"][:20].upper()}</div>
                            <div class="game-subtitle">{course.get("difficulty", "intermediate").title()} Level | {total_lvls} Levels</div>
                            <div class="game-progress-container">
                                <div class="game-progress-fill course-{course["course_id"][:8]}" style="width: {course_pct}%;"></div>
                            </div>
                            <div class="game-levels">{course_progress["completed_levels"]}/{total_lvls} Levels Complete</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button(f"CONTINUE", key=f"play_{course['course_id']}", use_container_width=True):
                        st.session_state.dynamic_course = course
                        st.session_state.current_game = "dynamic"
                        st.session_state.current_level = None
                        st.rerun()
    
    # Footer
    st.markdown('<div class="hub-footer">LEARN • PLAY • LEVEL UP</div>', unsafe_allow_html=True)


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Check login first
    if not is_logged_in():
        render_login_page()
        return
    
    # Check if showing profile
    if st.session_state.show_profile:
        render_profile_page()
        return
    
    # Route to appropriate game or hub
    if st.session_state.current_game == "dsa":
        render_dsa_game()
    elif st.session_state.current_game == "dbms":
        render_dbms_game()
    elif st.session_state.current_game == "maths":
        render_maths_game()
    elif st.session_state.current_game == "dynamic" and st.session_state.dynamic_course:
        render_dynamic_game(st.session_state.dynamic_course)
    else:
        render_game_hub()


if __name__ == "__main__":
    main()
