"""
Game Arcade UI
==============
Visual interface for selecting and playing arcade-style learning games.
Replaces traditional quiz selection with game library.
"""

import streamlit as st
from game_library import get_games_by_category, get_game_by_id


def render_game_arcade(subject: str, subject_color: str):
    """Render the game arcade for a specific subject."""
    
    games = get_games_by_category(subject)
    
    # Arcade Title
    st.markdown(f"""
        <style>
            .arcade-title {{
                font-family: 'Orbitron', sans-serif;
                font-size: 2.5rem;
                font-weight: 900;
                text-align: center;
                color: {subject_color};
                margin: 30px 0 10px 0;
                text-transform: uppercase;
                letter-spacing: 3px;
            }}
            
            .arcade-subtitle {{
                font-family: 'Rajdhani', sans-serif;
                text-align: center;
                color: #888;
                font-size: 1.1rem;
                margin-bottom: 40px;
            }}
            
            .game-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            
            .game-card {{
                background: linear-gradient(145deg, #1a1a2e, #2d2d44);
                border: 2px solid {subject_color}44;
                border-radius: 15px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
            }}
            
            .game-card:hover {{
                border-color: {subject_color};
                transform: translateY(-5px);
                box-shadow: 0 10px 30px {subject_color}66;
            }}
            
            .game-card.locked {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .game-card.boss {{
                border: 3px solid #ff4444;
                background: linear-gradient(145deg, #2d1a1a, #1a1a2e);
            }}
            
            .game-icon {{
                font-size: 3rem;
                text-align: center;
                margin-bottom: 10px;
            }}
            
            .game-name {{
                font-family: 'Orbitron', sans-serif;
                font-size: 1.3rem;
                font-weight: 700;
                text-align: center;
                color: {subject_color};
                margin-bottom: 5px;
            }}
            
            .game-difficulty {{
                text-align: center;
                color: #888;
                font-size: 0.8rem;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}
            
            .game-description {{
                text-align: center;
                color: #aaa;
                font-size: 0.9rem;
                line-height: 1.4;
                margin-bottom: 15px;
            }}
            
            .game-inspired {{
                text-align: center;
                color: #666;
                font-size: 0.75rem;
                font-style: italic;
                margin-bottom: 15px;
            }}
            
            .game-rewards {{
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }}
            
            .reward-item {{
                display: flex;
                justify-content: space-between;
                color: #888;
                font-size: 0.85rem;
                margin: 5px 0;
            }}
            
            .reward-value {{
                color: {subject_color};
                font-weight: 700;
            }}
            
            .difficulty-badge {{
                display: inline-block;
                padding: 3px 10px;
                border-radius: 10px;
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
            }}
            
            .difficulty-beginner {{
                background: #2ecc71;
                color: #fff;
            }}
            
            .difficulty-intermediate {{
                background: #f39c12;
                color: #fff;
            }}
            
            .difficulty-advanced {{
                background: #e74c3c;
                color: #fff;
            }}
            
            .difficulty-expert {{
                background: #9b59b6;
                color: #fff;
            }}
            
            .difficulty-boss {{
                background: linear-gradient(135deg, #ff0000, #ff6b00);
                color: #fff;
                animation: bossPulse 2s ease-in-out infinite;
            }}
            
            @keyframes bossPulse {{
                0%, 100% {{ box-shadow: 0 0 10px #ff000066; }}
                50% {{ box-shadow: 0 0 20px #ff0000cc; }}
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    arcade_titles = {
        "dsa": "DSA Arcade",
        "dbms": "Database Arcade",
        "math": "Math Arcade"
    }
    
    st.markdown(f'<div class="arcade-title">{arcade_titles.get(subject, "Game Arcade")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">Choose your game and start playing!</div>', unsafe_allow_html=True)
    
    # Render games in grid
    cols = st.columns(3)
    
    for idx, (game_id, game_data) in enumerate(games.items()):
        col_idx = idx % 3
        
        with cols[col_idx]:
            is_boss = game_data.get("category") == "boss"
            card_class = "game-card boss" if is_boss else "game-card"
            
            difficulty = game_data["difficulty"].lower()
            diff_class = f"difficulty-{difficulty}"
            
            st.markdown(f'''
                <div class="{card_class}">
                    <div class="game-icon">{game_data["icon"]}</div>
                    <div class="game-name">{game_data["name"]}</div>
                    <div class="game-difficulty">
                        <span class="difficulty-badge {diff_class}">{game_data["difficulty"]}</span>
                    </div>
                    <div class="game-description">{game_data["description"]}</div>
                    <div class="game-inspired">Inspired by: {game_data["inspired_by"]}</div>
                    <div class="game-rewards">
                        <div class="reward-item">
                            <span>Base XP:</span>
                            <span class="reward-value">+{game_data["rewards"]["xp_base"]}</span>
                        </div>
                        <div class="reward-item">
                            <span>Perfect XP:</span>
                            <span class="reward-value">+{game_data["rewards"]["xp_perfect"]}</span>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Play button
            button_label = "FIGHT BOSS" if is_boss else "PLAY GAME"
            button_type = "primary" if not is_boss else "secondary"
            
            if st.button(button_label, key=f"play_{game_id}", use_container_width=True, type=button_type):
                # Convert game ID to folder name (underscores to hyphens)
                folder_name = game_data.get("file", game_id.replace("_", "-"))
                
                # Set session state for mini-game integration
                st.session_state.selected_mini_game = folder_name
                st.session_state.show_mini_game = True
                st.session_state.show_arcade = False
                st.session_state.show_quiz = False
                st.rerun()
            
            # Info button
            with st.expander(f"How to Play"):
                st.markdown(f"**Gameplay:** {game_data['gameplay']}")
                
                if "modes" in game_data:
                    st.markdown("**Modes:**")
                    for mode in game_data["modes"]:
                        st.markdown(f"- {mode}")
                
                if "mechanics" in game_data:
                    st.markdown("**Game Mechanics:**")
                    for mechanic, enabled in game_data["mechanics"].items():
                        if enabled:
                            st.markdown(f"- {mechanic.replace('_', ' ').title()}")


def render_game_selector_compact(subject: str, subject_color: str):
    """Render a compact game selector for level pages."""
    
    games = get_games_by_category(subject)
    
    st.markdown(f"""
        <style>
            .compact-game-selector {{
                background: linear-gradient(145deg, #1a1a2e, #2d2d44);
                border: 2px solid {subject_color}44;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
            }}
            
            .selector-title {{
                font-family: 'Orbitron', sans-serif;
                font-size: 1.5rem;
                color: {subject_color};
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .game-option {{
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid {subject_color}44;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                gap: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .game-option:hover {{
                border-color: {subject_color};
                background: rgba(0, 0, 0, 0.5);
            }}
            
            .game-option-icon {{
                font-size: 2rem;
            }}
            
            .game-option-info {{
                flex: 1;
            }}
            
            .game-option-name {{
                font-family: 'Orbitron', sans-serif;
                font-size: 1.1rem;
                color: {subject_color};
                font-weight: 700;
            }}
            
            .game-option-desc {{
                color: #888;
                font-size: 0.85rem;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="compact-game-selector">', unsafe_allow_html=True)
    st.markdown(f'<div class="selector-title">Choose Your Game</div>', unsafe_allow_html=True)
    
    # Show 3-4 most relevant games
    game_list = list(games.items())[:4]
    
    for game_id, game_data in game_list:
        col1, col2, col3 = st.columns([1, 4, 2])
        
        with col1:
            st.markdown(f'<div style="font-size: 2.5rem; text-align: center;">{game_data["icon"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div style="font-family: Orbitron, sans-serif; color: {subject_color}; font-weight: 700;">{game_data["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #888; font-size: 0.85rem;">{game_data["description"][:60]}...</div>', unsafe_allow_html=True)
        
        with col3:
            if st.button("PLAY", key=f"quick_{game_id}", use_container_width=True):
                st.session_state.selected_game = game_id
                st.session_state.view = "game_play"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # View all games button
    if st.button("VIEW ALL GAMES", use_container_width=True):
        st.session_state.view = "game_arcade"
        st.rerun()
