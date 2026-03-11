"""
Profile Page Module
===================
User profile display and settings.
"""

import streamlit as st
from datetime import datetime
from gamification import get_progress_summary, get_game_progress, get_total_game_progress
from login import get_user_data, update_user_data, logout, AVATAR_COLORS
from course_generator import get_user_dynamic_courses, load_cached_courses


def inject_profile_css():
    """Inject CSS for profile page."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a1628 100%);
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .profile-header {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 2px solid #00ff88;
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 30px;
        }
        
        .profile-avatar-large {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            color: #0a0a0f;
            box-shadow: 0 0 30px currentColor;
        }
        
        .profile-info {
            flex: 1;
        }
        
        .profile-name {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            background: linear-gradient(135deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        
        .profile-title {
            font-family: 'Rajdhani', sans-serif;
            color: #ffd700;
            font-size: 1.1rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .profile-bio {
            font-family: 'Rajdhani', sans-serif;
            color: #888;
            font-size: 1rem;
            margin-top: 10px;
            font-style: italic;
        }
        
        .profile-meta {
            font-family: 'Rajdhani', sans-serif;
            color: #666;
            font-size: 0.85rem;
            margin-top: 15px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: #00d4ff;
        }
        
        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            color: #00ff88;
        }
        
        .stat-label {
            font-family: 'Rajdhani', sans-serif;
            color: #888;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }
        
        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            margin: 30px 0 20px 0;
            letter-spacing: 3px;
        }
        
        .badge-container {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 2px solid #ffd700;
            border-radius: 15px;
            padding: 25px;
        }
        
        .badge-item {
            display: inline-block;
            background: linear-gradient(135deg, #ffd70011, #ffd70022);
            border: 1px solid #ffd700;
            border-radius: 10px;
            padding: 12px 18px;
            margin: 5px;
            font-family: 'Rajdhani', sans-serif;
            color: #ffd700;
            font-weight: 600;
        }
        
        .game-progress-card {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
        
        .progress-bar-bg {
            background: #1a1a2e;
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
        }
        
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }
        
        .detail-card {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 1px solid rgba(255, 0, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .detail-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: #ff00ff;
        }
        
        .detail-label {
            font-family: 'Rajdhani', sans-serif;
            color: #888;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .activity-card {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 15px;
            padding: 20px;
        }
        
        .activity-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .activity-row:last-child {
            border-bottom: none;
        }
        
        .activity-label {
            font-family: 'Rajdhani', sans-serif;
            color: #888;
        }
        
        .activity-value {
            font-family: 'Rajdhani', sans-serif;
            color: #00ff88;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


# Title assignments based on level and achievements
TITLES = {
    1: "Novice Learner",
    2: "Curious Explorer",
    3: "Knowledge Seeker",
    5: "Rising Star",
    7: "Scholar",
    10: "Expert Scholar",
    15: "Master Mind",
    20: "Grand Master",
    25: "Legend"
}

BADGES_INFO = {
    "first_question": {"name": "First Steps", "desc": "Answered first question"},
    "ten_correct": {"name": "Quick Learner", "desc": "10 correct answers"},
    "fifty_correct": {"name": "Knowledge Seeker", "desc": "50 correct answers"},
    "hundred_correct": {"name": "Master Mind", "desc": "100 correct answers"},
    "boss_slayer": {"name": "Boss Slayer", "desc": "Defeated a boss"},
    "level_5": {"name": "Rising Star", "desc": "Reached level 5"},
    "level_10": {"name": "Expert Scholar", "desc": "Reached level 10"},
    "perfect_streak": {"name": "Perfect Streak", "desc": "5 correct in a row"},
}


def get_title_for_level(level):
    """Get title based on level."""
    title = "Novice Learner"
    for lvl, t in TITLES.items():
        if level >= lvl:
            title = t
    return title


def format_date(iso_string):
    """Format ISO date string to readable format."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y")
    except:
        return "Unknown"


def calculate_time_played(progress):
    """Estimate time played based on activity."""
    # Rough estimate: 2 min per question attempted
    questions = progress.get("questions_attempted", 0)
    minutes = questions * 2
    if minutes < 60:
        return f"{minutes} min"
    else:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"


def render_profile_page():
    """Render the user profile page."""
    inject_profile_css()
    
    username = st.session_state.get("username", "Guest")
    user_data = st.session_state.get("user_data", {})
    progress = get_progress_summary()
    game_progress = get_total_game_progress()
    
    # Get current title based on level
    current_title = get_title_for_level(progress["level"])
    
    # Header with back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("< BACK TO HUB", key="back_hub"):
            st.session_state.show_profile = False
            st.rerun()
    with col3:
        if st.button("LOGOUT", key="logout_btn"):
            logout()
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Profile Header with Avatar
    avatar_letter = user_data.get('avatar', username[0].upper() if username else 'P')
    avatar_color = user_data.get('avatar_color', '#00ff88')
    
    st.markdown(f"""
        <div class="profile-header">
            <div class="profile-avatar-large" style="background: {avatar_color};">
                {avatar_letter}
            </div>
            <div class="profile-info">
                <div class="profile-name">{user_data.get('display_name', username)}</div>
                <div class="profile-title">{current_title}</div>
                <div class="profile-bio">"{user_data.get('bio', 'Ready to learn!')}"</div>
                <div class="profile-meta">
                    Member since {format_date(user_data.get('created_at', ''))} | 
                    Last seen {format_date(user_data.get('last_login', ''))}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Stats Grid
    st.markdown('<div class="section-title" style="color: #00ff88;">PLAYER STATISTICS</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{progress['level']}</div>
                <div class="stat-label">Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{progress['xp']}</div>
                <div class="stat-label">Total XP</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{progress['accuracy']:.0f}%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{progress['best_streak']}</div>
                <div class="stat-label">Best Streak</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Two columns - Achievements and Game Progress
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title" style="color: #ffd700;">ACHIEVEMENTS</div>', unsafe_allow_html=True)
        
        badges = progress.get("badges", [])
        if badges:
            badge_html = ""
            for badge in badges:
                badge_info = BADGES_INFO.get(badge, {"name": badge, "desc": ""})
                badge_html += f'<span class="badge-item">{badge_info["name"]}</span>'
            
            st.markdown(f"""
                <div class="badge-container">
                    {badge_html}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="badge-container" style="text-align: center; color: #666;">
                    No achievements yet. Start playing to earn badges!
                </div>
            """, unsafe_allow_html=True)
        
        # Available badges to unlock
        st.markdown("<br>", unsafe_allow_html=True)
        unlocked = len(badges)
        total_badges = len(BADGES_INFO)
        st.markdown(f"""
            <p style="font-family: 'Rajdhani', sans-serif; color: #888; text-align: center;">
                {unlocked} / {total_badges} badges unlocked
            </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title" style="color: #00d4ff;">COURSES IN PROGRESS</div>', unsafe_allow_html=True)
        
        # Predefined games - only show if started
        predefined_games = [
            {"id": "dsa", "name": "DSA Adventure", "color": "#ff6b6b"},
            {"id": "dbms", "name": "Database Quest", "color": "#00d4ff"},
            {"id": "maths", "name": "Math Arena", "color": "#00ff88"}
        ]
        
        started_courses = []
        
        # Check predefined games (always 6 levels)
        for game in predefined_games:
            gp = get_game_progress(game["id"])
            completed = gp.get("completed_levels", 0)
            levels_done = gp.get("levels_completed", [])
            # Only add if user has started this course
            if completed > 0 or len(levels_done) > 0:
                started_courses.append({
                    "id": game["id"],
                    "name": game["name"],
                    "color": game["color"],
                    "progress": gp,
                    "is_dynamic": False,
                    "total_levels": 6
                })
        
        # Add dynamic courses
        dynamic_courses = get_user_dynamic_courses()
        for course in dynamic_courses:
            gp = get_game_progress(course["course_id"])
            colors = course.get("colors", {"primary": "#00d4ff", "secondary": "#00ff88"})
            total_lvls = course.get("total_levels", len(course.get("levels", [])))
            started_courses.append({
                "id": course["course_id"],
                "name": course.get("course_title", "AI Course"),
                "color": colors.get("primary", "#00d4ff"),
                "progress": gp,
                "is_dynamic": True,
                "total_levels": total_lvls
            })
        
        if started_courses:
            for course in started_courses:
                gp = course["progress"]
                completed = gp.get("completed_levels", 0)
                total = course.get("total_levels", 6)
                percentage = (completed / total) * 100 if total > 0 else 0
                boss_defeated = gp.get("boss_defeated", False)
                
                badge = "[AI]" if course["is_dynamic"] else ""
                
                st.markdown(f"""
                    <div class="game-progress-card" style="border: 2px solid {course['color']}44;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-family: 'Rajdhani', sans-serif; color: #fff; font-weight: 600;">
                                {badge} {course['name'][:25]}
                            </span>
                            <span style="font-family: 'Orbitron', sans-serif; color: {course['color']}; font-size: 0.9rem;">
                                {completed}/{total} {'[BOSS DEFEATED]' if boss_defeated else ''}
                            </span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: {percentage}%; background: linear-gradient(90deg, {course['color']}, {course['color']}aa);"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="game-progress-card" style="border: 2px solid #33333344; text-align: center;">
                    <p style="font-family: 'Rajdhani', sans-serif; color: #666; margin: 0;">
                        No courses started yet. Enter a game to begin!
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Statistics Section
    st.markdown('<div class="section-title" style="color: #ff00ff;">DETAILED STATISTICS</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="detail-grid">
            <div class="detail-card">
                <div class="detail-value">{progress["questions_attempted"]}</div>
                <div class="detail-label">Questions Attempted</div>
            </div>
            <div class="detail-card">
                <div class="detail-value">{progress["correct_answers"]}</div>
                <div class="detail-label">Correct Answers</div>
            </div>
            <div class="detail-card">
                <div class="detail-value">{progress["boss_battles_won"]}</div>
                <div class="detail-label">Boss Battles Won</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Activity Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title" style="color: #00ff88;">ACTIVITY SUMMARY</div>', unsafe_allow_html=True)
        
        xp_to_next = 100 - (progress['xp'] % 100)
        time_played = calculate_time_played(progress)
        
        st.markdown(f"""
            <div class="activity-card">
                <div class="activity-row">
                    <span class="activity-label">XP to Next Level</span>
                    <span class="activity-value">{xp_to_next} XP</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Current Streak</span>
                    <span class="activity-value">{progress.get('current_streak', 0)}</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Est. Time Played</span>
                    <span class="activity-value">{time_played}</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Learning Efficiency</span>
                    <span class="activity-value">{progress['accuracy']:.0f}%</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title" style="color: #00d4ff;">PERFORMANCE BREAKDOWN</div>', unsafe_allow_html=True)
        
        # Calculate performance metrics
        total_q = progress["questions_attempted"]
        correct = progress["correct_answers"]
        wrong = total_q - correct
        
        # Count started courses
        courses_started = 0
        boss_wins = 0
        for game_id in ["dsa", "dbms", "maths"]:
            gp = get_game_progress(game_id)
            if gp.get("completed_levels", 0) > 0 or len(gp.get("levels_completed", [])) > 0:
                courses_started += 1
                if gp.get("boss_defeated", False):
                    boss_wins += 1
        
        # Add dynamic courses
        dynamic_courses = get_user_dynamic_courses()
        courses_started += len(dynamic_courses)
        for course in dynamic_courses:
            gp = get_game_progress(course["course_id"])
            if gp.get("boss_defeated", False):
                boss_wins += 1
        
        st.markdown(f"""
            <div class="activity-card">
                <div class="activity-row">
                    <span class="activity-label">Courses Started</span>
                    <span class="activity-value">{courses_started}</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Correct Answers</span>
                    <span class="activity-value" style="color: #00ff88;">{correct}</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Wrong Answers</span>
                    <span class="activity-value" style="color: #ff6b6b;">{wrong}</span>
                </div>
                <div class="activity-row">
                    <span class="activity-label">Boss Battles Won</span>
                    <span class="activity-value">{boss_wins}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Edit Profile Section (for non-guests)
    if username != "Guest":
        with st.expander("EDIT PROFILE"):
            new_display = st.text_input("Display Name", value=user_data.get("display_name", username))
            new_bio = st.text_input("Bio", value=user_data.get("bio", ""))
            
            # Avatar color selection
            st.write("Change Avatar Color:")
            color_cols = st.columns(6)
            
            current_color = user_data.get("avatar_color", "#00ff88")
            new_color = current_color
            
            for idx, color in enumerate(AVATAR_COLORS[:6]):
                with color_cols[idx]:
                    if st.button(f"Color {idx+1}", key=f"profile_color_{idx}"):
                        new_color = color
            
            color_cols2 = st.columns(6)
            for idx, color in enumerate(AVATAR_COLORS[6:]):
                with color_cols2[idx]:
                    if st.button(f"Color {idx+7}", key=f"profile_color_{idx+6}"):
                        new_color = color
            
            if st.button("SAVE CHANGES", type="primary"):
                update_user_data(username, {
                    "display_name": new_display,
                    "bio": new_bio,
                    "avatar_color": new_color
                })
                st.session_state.user_data = get_user_data(username)
                st.success("Profile updated!")
                st.rerun()
