"""
World Map UI Components
=======================
Visual interfaces for world navigation, region maps, and mission selection.
"""

import streamlit as st
from world_manager import WORLDS, get_player_world_progress, is_region_unlocked, get_region_progress_percent


def render_world_selection():
    """Render the main world selection screen."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');
            
            .universe-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 3rem;
                font-weight: 900;
                text-align: center;
                background: linear-gradient(135deg, #4a90e2, #a06ee1, #e91e63);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 5px;
            }
            
            .universe-subtitle {
                font-family: 'Rajdhani', sans-serif;
                text-align: center;
                color: #888;
                font-size: 1.2rem;
                margin-bottom: 40px;
            }
            
            .world-card {
                background: linear-gradient(145deg, #1a1a2e, #2d2d44);
                border: 2px solid var(--world-color);
                border-radius: 20px;
                padding: 30px;
                margin: 20px 0;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .world-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px var(--world-glow);
            }
            
            .world-icon {
                font-size: 4rem;
                text-align: center;
                margin-bottom: 15px;
            }
            
            .world-name {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.8rem;
                font-weight: 700;
                text-align: center;
                color: var(--world-color);
                margin-bottom: 10px;
            }
            
            .world-description {
                text-align: center;
                color: #aaa;
                font-size: 1rem;
                margin-bottom: 20px;
            }
            
            .world-progress {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin-top: 15px;
            }
            
            .progress-bar-container {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                height: 25px;
                overflow: hidden;
                margin-top: 10px;
            }
            
            .progress-bar-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--world-color), var(--world-secondary));
                transition: width 0.5s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 0.85rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="universe-title">AI Learning Universe</h1>', unsafe_allow_html=True)
    st.markdown('<p class="universe-subtitle">Choose your world and begin your adventure</p>', unsafe_allow_html=True)
    
    # Get player progress
    username = st.session_state.username
    progress = get_player_world_progress(username)
    
    # Render world cards
    for world_id, world_data in WORLDS.items():
        # Calculate world completion
        total_regions = len(world_data["regions"])
        completed_regions = sum(1 for rid in world_data["regions"].keys() 
                               if rid in progress.get("completed_regions", []))
        world_progress_percent = int((completed_regions / total_regions) * 100)
        
        # Create world card with custom colors
        st.markdown(f"""
            <style>
                #{world_id}-card {{
                    --world-color: {world_data['color_primary']};
                    --world-secondary: {world_data['color_secondary']};
                    --world-glow: {world_data['color_primary']}44;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col2:
            with st.container():
                st.markdown(f'<div class="world-card" id="{world_id}-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="world-icon">{world_data["icon"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="world-name">{world_data["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="world-description">{world_data["description"]}</div>', unsafe_allow_html=True)
                
                # Enter button
                if st.button(f"ENTER {world_data['name'].upper()}", key=f"enter_{world_id}", use_container_width=True):
                    st.session_state.current_world = world_id
                    st.session_state.view = "region_map"
                    st.rerun()
                
                # Progress
                st.markdown('<div class="world-progress">', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #888; font-size: 0.85rem; margin-bottom: 5px;">PROGRESS: {completed_regions}/{total_regions} regions complete</p>', unsafe_allow_html=True)
                st.markdown(f'''
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {world_progress_percent}%;">
                            {world_progress_percent}%
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)


def render_region_map(world_id: str):
    """Render the region map for a specific world."""
    world_data = WORLDS.get(world_id)
    if not world_data:
        st.error("World not found!")
        return
    
    username = st.session_state.username
    progress = get_player_world_progress(username)
    
    # Header
    st.markdown(f"""
        <style>
            .region-map-header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .region-map-title {{
                font-family: 'Orbitron', sans-serif;
                font-size: 2.5rem;
                font-weight: 900;
                color: {world_data['color_primary']};
                margin-bottom: 10px;
            }}
            
            .region-node {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                margin: 20px auto;
            }}
            
            .region-node.unlocked {{
                background: linear-gradient(135deg, {world_data['color_primary']}, {world_data['color_secondary']});
                border: 3px solid {world_data['color_primary']};
                box-shadow: 0 5px 20px {world_data['color_primary']}66;
            }}
            
            .region-node.locked {{
                background: linear-gradient(135deg, #333, #555);
                border: 3px solid #666;
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .region-node.completed {{
                background: linear-gradient(135deg, #2ecc71, #27ae60);
                border: 3px solid #2ecc71;
                box-shadow: 0 5px 20px #2ecc7166;
            }}
            
            .region-node:hover:not(.locked) {{
                transform: scale(1.1);
            }}
            
            .region-name {{
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.1rem;
                font-weight: 600;
                text-align: center;
                margin-top: 10px;
                color: #fff;
            }}
            
            .region-progress-badge {{
                position: absolute;
                top: -10px;
                right: -10px;
                background: #2ecc71;
                color: #fff;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.8rem;
                font-weight: 700;
                border: 2px solid #fff;
            }}
            
            .path-line {{
                width: 4px;
                height: 60px;
                background: linear-gradient(180deg, {world_data['color_primary']}, transparent);
                margin: 0 auto;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("< BACK TO WORLDS"):
            st.session_state.view = "world_selection"
            st.rerun()
    
    # Title
    st.markdown(f'''
        <div class="region-map-header">
            <div style="font-size: 4rem;">{world_data["icon"]}</div>
            <div class="region-map-title">{world_data["name"]}</div>
            <p style="color: #888; font-size: 1.1rem;">{world_data["description"]}</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Render regions in vertical path
    regions = list(world_data["regions"].values())
    regions.reverse()  # Bottom to top
    
    for i, region_data in enumerate(regions):
        region_id = region_data["id"]
        unlocked = is_region_unlocked(username, region_id)
        completed = region_id in progress.get("completed_regions", [])
        progress_percent = get_region_progress_percent(username, region_id)
        
        # Determine node state
        if completed:
            node_class = "completed"
            status_icon = "[Done]"
        elif unlocked:
            node_class = "unlocked"
            status_icon = region_data["icon"]
        else:
            node_class = "locked"
            status_icon = "[LOCKED]"
        
        # Show connecting path (except for first)
        if i > 0:
            st.markdown('<div class="path-line"></div>', unsafe_allow_html=True)
        
        # Region node
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'''
                <div class="region-node {node_class}">
                    {status_icon}
                    {f'<div class="region-progress-badge">{progress_percent}%</div>' if unlocked and not completed else ''}
                </div>
                <div class="region-name">{region_data["name"]}</div>
            ''', unsafe_allow_html=True)
            
            if unlocked:
                if st.button(f"EXPLORE {region_data['name'].upper()}", key=f"explore_{region_id}", use_container_width=True):
                    st.session_state.current_region = region_id
                    st.session_state.view = "mission_hub"
                    st.rerun()
            else:
                st.button(f"LOCKED", key=f"locked_{region_id}", disabled=True, use_container_width=True)


def render_player_resources():
    """Render player resources in sidebar."""
    username = st.session_state.username
    progress = get_player_world_progress(username)
    resources = progress.get("resources", {})
    
    st.sidebar.markdown("### Resources")
    
    # Energy
    energy = resources.get("energy", 100)
    max_energy = resources.get("max_energy", 100)
    energy_percent = int((energy / max_energy) * 100)
    
    st.sidebar.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Energy</span>
                <span>{energy}/{max_energy}</span>
            </div>
            <div style="background: rgba(0,0,0,0.5); border-radius: 10px; height: 20px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #f39c12, #e74c3c); width: {energy_percent}%; height: 100%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Gems
    gems = resources.get("knowledge_gems", 0)
    st.sidebar.metric("Knowledge Gems", gems)
    
    # Hints
    hints = resources.get("hint_tokens", 3)
    st.sidebar.metric("Hint Tokens", hints)
    
    # Abilities
    unlocked_abilities = progress.get("unlocked_abilities", [])
    st.sidebar.markdown(f"### Abilities Unlocked")
    st.sidebar.markdown(f"**{len(unlocked_abilities)}/14** abilities")
