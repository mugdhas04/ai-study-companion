"""
Login & Authentication Module
=============================
Handles user login, registration, and session management.
"""

import streamlit as st
import json
import os
import hashlib
from datetime import datetime

USERS_FILE = "users.json"

# Avatar codes (letters for now, no emojis)
AVATAR_CODES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
AVATAR_COLORS = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#a855f7", "#ec4899", 
                 "#00ff88", "#00d4ff", "#ff00ff", "#ffd700", "#ff8800", "#00ff00"]


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load users from JSON file."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_users(users):
    """Save users to JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def register_user(username, password, display_name):
    """
    Register a new user.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    users = load_users()
    
    if not username or not password:
        return False, "Username and password are required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters"
    
    if username.lower() in [u.lower() for u in users.keys()]:
        return False, "Username already taken"
    
    users[username] = {
        "password_hash": hash_password(password),
        "display_name": display_name or username,
        "avatar": username[0].upper(),
        "avatar_color": AVATAR_COLORS[len(users) % len(AVATAR_COLORS)],
        "title": "Novice Learner",
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat(),
        "bio": "Ready to learn!",
        "favorite_game": None
    }
    
    save_users(users)
    return True, "Account created successfully!"


def authenticate_user(username, password):
    """
    Authenticate a user.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    users = load_users()
    
    if username not in users:
        return False, "Invalid username or password"
    
    if users[username]["password_hash"] != hash_password(password):
        return False, "Invalid username or password"
    
    # Update last login
    users[username]["last_login"] = datetime.now().isoformat()
    save_users(users)
    
    return True, "Login successful!"


def get_user_data(username):
    """Get user data by username."""
    users = load_users()
    return users.get(username, None)


def update_user_data(username, data):
    """Update user data."""
    users = load_users()
    if username in users:
        users[username].update(data)
        save_users(users)
        return True
    return False


def inject_login_css():
    """Inject CSS for login page."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a1628 100%);
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .hero-section {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
        }
        
        .hero-logo {
            width: 120px;
            height: 120px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #00ff88, #00d4ff);
            border-radius: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 40px rgba(0, 255, 136, 0.4);
            animation: logoPulse 2s ease-in-out infinite;
        }
        
        @keyframes logoPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(0, 255, 136, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 0 60px rgba(0, 212, 255, 0.6); }
        }
        
        .hero-logo-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            color: #0a0a0f;
        }
        
        .hero-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.8rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00ff88, #00d4ff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 4px;
            margin-bottom: 15px;
            animation: titleShine 3s ease-in-out infinite;
        }
        
        @keyframes titleShine {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.3); }
        }
        
        .hero-tagline {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.4rem;
            color: #888;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 30px;
        }
        
        .login-card {
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 2px solid rgba(0, 255, 136, 0.3);
            border-radius: 25px;
            padding: 35px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        
        .form-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            color: #00ff88;
            text-align: center;
            margin-bottom: 25px;
            letter-spacing: 3px;
        }
        
        .avatar-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #0a0a0f;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid transparent;
        }
        
        .avatar-circle:hover {
            transform: scale(1.1);
        }
        
        .avatar-circle.selected {
            border-color: #fff;
            box-shadow: 0 0 20px currentColor;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 25px 0;
            color: #444;
        }
        
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, transparent, #444, transparent);
        }
        
        .divider span {
            padding: 0 15px;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 2px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_login_page():
    """Render the login/register page."""
    inject_login_css()
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-logo">
                <span class="hero-logo-text">AI</span>
            </div>
            <h1 class="hero-title">AI STUDY GAME HUB</h1>
            <p class="hero-tagline">Level Up Your Knowledge</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Tabs for Login/Register
        tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
        
        with tab1:
            st.markdown('<div class="form-title">WELCOME BACK</div>', unsafe_allow_html=True)
            
            login_username = st.text_input("Username", key="login_user", placeholder="Enter your username")
            login_password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("ENTER THE HUB", use_container_width=True, type="primary"):
                if login_username and login_password:
                    success, message = authenticate_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.user_data = get_user_data(login_username)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter username and password")
        
        with tab2:
            st.markdown('<div class="form-title">JOIN THE ADVENTURE</div>', unsafe_allow_html=True)
            
            reg_username = st.text_input("Choose Username", key="reg_user", placeholder="Your unique username")
            reg_display = st.text_input("Display Name", key="reg_display", placeholder="How should we call you?")
            reg_password = st.text_input("Create Password", type="password", key="reg_pass", placeholder="Min 4 characters")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
            
            # Avatar color selection
            st.markdown("<p style='color: #888; font-family: Rajdhani, sans-serif; margin-top: 15px;'>Choose your avatar color:</p>", unsafe_allow_html=True)
            
            if "selected_avatar_idx" not in st.session_state:
                st.session_state.selected_avatar_idx = 0
            
            avatar_cols = st.columns(6)
            for idx, color in enumerate(AVATAR_COLORS[:6]):
                with avatar_cols[idx]:
                    is_selected = st.session_state.selected_avatar_idx == idx
                    if st.button(
                        AVATAR_CODES[idx],
                        key=f"avatar_{idx}",
                        type="primary" if is_selected else "secondary"
                    ):
                        st.session_state.selected_avatar_idx = idx
                        st.rerun()
            
            avatar_cols2 = st.columns(6)
            for idx, color in enumerate(AVATAR_COLORS[6:]):
                with avatar_cols2[idx]:
                    is_selected = st.session_state.selected_avatar_idx == idx + 6
                    if st.button(
                        AVATAR_CODES[idx + 6],
                        key=f"avatar_{idx + 6}",
                        type="primary" if is_selected else "secondary"
                    ):
                        st.session_state.selected_avatar_idx = idx + 6
                        st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("CREATE ACCOUNT", use_container_width=True, type="primary"):
                if not reg_username or not reg_password:
                    st.warning("Username and password are required")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(reg_username, reg_password, reg_display)
                    if success:
                        # Update avatar color
                        update_user_data(reg_username, {
                            "avatar": reg_username[0].upper(),
                            "avatar_color": AVATAR_COLORS[st.session_state.selected_avatar_idx]
                        })
                        st.success(message)
                        st.info("You can now login with your credentials!")
                    else:
                        st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Guest login option
        st.markdown("""
            <div class="divider"><span>OR</span></div>
        """, unsafe_allow_html=True)
        
        if st.button("CONTINUE AS GUEST", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.session_state.user_data = {
                "display_name": "Guest Player",
                "avatar": "G",
                "avatar_color": "#888888",
                "title": "Explorer",
                "bio": "Just exploring!",
                "favorite_game": None
            }
            st.rerun()


def is_logged_in():
    """Check if user is logged in."""
    return st.session_state.get("logged_in", False)


def logout():
    """Logout current user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.current_game = None
    st.session_state.current_level = None
