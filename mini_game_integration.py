"""
Mini-Game Integration Module
=============================
Embeds HTML/JS mini-games into Streamlit using iframes.
Handles communication between games and Streamlit backend.
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path


def render_mini_game(game_name: str, username: str, game_id: str, level_id: int, difficulty: str = "intermediate"):
    """
    Render a mini-game by loading its HTML content directly.
    
    Args:
        game_name: Name of the game folder (e.g., 'stack-tower')
        username: Current user's username
        game_id: Game identifier (e.g., 'dsa', 'dbms')
        level_id: Current level number
        difficulty: Difficulty level
    """
    # Get game directory path
    game_dir = Path(__file__).parent / "mini-games" / game_name
    game_html_path = game_dir / "index.html"
    game_css_path = game_dir / "style.css"
    game_js_path = game_dir / "game.js"
    
    if not game_html_path.exists():
        st.error(f"Game not found: {game_name}")
        st.info(f"Expected path: {game_html_path}")
        return
    
    # Read game files
    try:
        with open(game_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if this is a self-contained HTML file (has embedded <style> and <script>)
        is_self_contained = '<style>' in html_content and '</script>' in html_content
        
        if is_self_contained:
            # Self-contained HTML - inject game params and render directly
            params_script = f"""
    <script>
        window.GAME_PARAMS = {{
            username: '{username}',
            gameId: '{game_id}',
            levelId: {level_id},
            difficulty: '{difficulty}'
        }};
    </script>
    """
            # Inject params right after <head>
            if '<head>' in html_content:
                full_html = html_content.replace('<head>', f'<head>\n{params_script}')
            else:
                full_html = params_script + html_content
            
            components.html(full_html, height=850, scrolling=True)
            return
        
        # Traditional multi-file game - load separate CSS/JS
        with open(game_css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        with open(game_js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Read shared API client
        api_client_path = Path(__file__).parent / "mini-games" / "shared" / "api-client.js"
        with open(api_client_path, 'r', encoding='utf-8') as f:
            api_client_js = f.read()
        
    except Exception as e:
        st.error(f"Error loading game files: {str(e)}")
        return
    
    # Inject game parameters via script
    params_script = f"""
    <script>
        window.GAME_PARAMS = {{
            username: '{username}',
            gameId: '{game_id}',
            levelId: {level_id},
            difficulty: '{difficulty}'
        }};
    </script>
    """
    
    # Combine all content
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            {css_content}
        </style>
        {params_script}
    </head>
    <body>
        {html_content.split('<body>')[1].split('</body>')[0] if '<body>' in html_content else html_content}
        
        <script>
            {api_client_js}
        </script>
        <script>
            {js_content}
        </script>
    </body>
    </html>
    """
    
    # Render the complete HTML
    components.html(full_html, height=850, scrolling=True)


def get_available_mini_games():
    """
    Get list of available mini-games.
    
    Returns:
        dict: Dictionary mapping game IDs to game info
    """
    return {
        "sorting-arena": {
            "name": "Sorting Arena",
            "description": "Master sorting algorithms in an interactive arena",
            "subject": "DSA",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "array-sorter": {
            "name": "Array Sorter",
            "description": "Sort arrays by swapping elements - learn sorting basics",
            "subject": "DSA",
            "difficulty": "Beginner",
            "icon": ""
        },
        "link-builder": {
            "name": "Link Chain Builder",
            "description": "Build linked lists by connecting nodes",
            "subject": "DSA",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "stack-tower": {
            "name": "Stack Tower",
            "description": "Learn Stack (LIFO) by building towers",
            "subject": "DSA",
            "difficulty": "Beginner",
            "icon": ""
        },
        "tree-builder": {
            "name": "Binary Tree Builder",
            "description": "Build and traverse binary trees",
            "subject": "DSA",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "graph-explorer": {
            "name": "Graph Path Explorer",
            "description": "Navigate through graphs and find shortest paths",
            "subject": "DSA",
            "difficulty": "Advanced",
            "icon": ""
        },
        "hash-defender": {
            "name": "Hash Defender",
            "description": "Insert keys into hash tables and handle collisions",
            "subject": "DSA",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "queue-controller": {
            "name": "Queue Traffic Controller",
            "description": "Release cars in FIFO order - learn queue operations",
            "subject": "DSA",
            "difficulty": "Beginner",
            "icon": ""
        },
        "algorithm-race": {
            "name": "Algorithm Race",
            "description": "Watch algorithms compete and predict the winner",
            "subject": "DSA",
            "difficulty": "Expert",
            "icon": ""
        },
        "algorithm-boss": {
            "name": "Algorithm Arena",
            "description": "Epic 3-phase boss battle - Theory, Design, Optimization",
            "subject": "DSA",
            "difficulty": "Boss",
            "icon": ""
        },
        "sql-detective": {
            "name": "SQL Detective",
            "description": "Solve database queries to find data",
            "subject": "DBMS",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "schema-builder": {
            "name": "Schema Builder",
            "description": "Design ER diagrams with entities and relationships",
            "subject": "DBMS",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "query-optimizer": {
            "name": "Query Optimizer",
            "description": "Learn database indexing strategies",
            "subject": "DBMS",
            "difficulty": "Advanced",
            "icon": ""
        },
        "transaction-simulator": {
            "name": "Transaction Simulator",
            "description": "Master ACID properties with bank transactions",
            "subject": "DBMS",
            "difficulty": "Advanced",
            "icon": ""
        },
        "equation-shooter": {
            "name": "Equation Shooter",
            "description": "Shoot correct answers to falling equations",
            "subject": "Maths",
            "difficulty": "Beginner",
            "icon": ""
        },
        "matrix-master": {
            "name": "Matrix Master",
            "description": "Solve matrix operations - addition, multiplication, determinants",
            "subject": "Maths",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "probability-dice": {
            "name": "Probability Dice",
            "description": "Learn probability with interactive dice challenges",
            "subject": "Maths",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "logic-gates": {
            "name": "Logic Gates",
            "description": "Master AND, OR, XOR and other logic gates",
            "subject": "Maths",
            "difficulty": "Intermediate",
            "icon": ""
        },
        "prime-hunter": {
            "name": "Prime Hunter",
            "description": "Hunt primes, find GCD/LCM - number theory fun",
            "subject": "Maths",
            "difficulty": "Intermediate",
            "icon": ""
        }
    }


def render_mini_game_selector(subject: str):
    """
    Render a selector for mini-games by subject.
    
    Args:
        subject: Subject filter ('DSA', 'DBMS', 'Maths', or 'All')
        
    Returns:
        str: Selected game ID or None
    """
    games = get_available_mini_games()
    
    # Filter by subject
    if subject != 'All':
        games = {k: v for k, v in games.items() if v['subject'] == subject}
    
    if not games:
        st.info(f"No mini-games available for {subject} yet.")
        return None
    
    # Display game cards
    st.markdown("### MINI-GAMES")
    
    cols = st.columns(min(len(games), 3))
    
    selected_game = None
    for idx, (game_id, game_info) in enumerate(games.items()):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, #1a1a2e, #2d2d44);
                    border: 2px solid #ff6b6b44;
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                ">
                    <div style="font-size: 3rem;">{game_info['icon']}</div>
                    <h4 style="color: #ff6b6b; font-family: 'Orbitron', sans-serif;">
                        {game_info['name']}
                    </h4>
                    <p style="color: #888; font-family: 'Rajdhani', sans-serif; font-size: 0.9rem;">
                        {game_info['description']}
                    </p>
                    <p style="color: #00ff88; font-family: 'Rajdhani', sans-serif; font-size: 0.85rem;">
                        {game_info['difficulty']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"PLAY {game_info['name'].upper()}", key=f"play_{game_id}"):
                selected_game = game_id
    
    return selected_game


def check_game_completion():
    """
    Check if a game was completed (called from iframe message).
    
    Returns:
        dict or None: Game completion data
    """
    # This would be called via Streamlit's component callback
    # For now, it's a placeholder for the architecture
    if 'game_completion_data' in st.session_state:
        data = st.session_state.game_completion_data
        del st.session_state.game_completion_data
        return data
    return None
