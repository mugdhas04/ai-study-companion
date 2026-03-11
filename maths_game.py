"""
Math Arena - Game Module
========================
Mathematics learning game with levels and boss battles.
"""

import streamlit as st
from explainer import explain_topic
from quiz_generator import generate_quiz, generate_boss_question, generate_hint
from gamification import record_answer, get_game_progress, complete_level, get_progress_summary
from components import render_explanation_with_flashcards
from mini_game_integration import render_mini_game, get_available_mini_games

# Maths Game Configuration
GAME_ID = "maths"
GAME_TITLE = "MATH ARENA"
GAME_ICON = "MATH"
GAME_COLOR_1 = "#00ff88"
GAME_COLOR_2 = "#00d4ff"

# Level to mini-game mapping
LEVEL_TO_GAME_MAPPING = {
    1: "equation-shooter",  # Calculus Basics -> Equation Shooter
    2: "matrix-master",     # Linear Algebra -> Matrix Master
    3: "probability-dice",  # Probability -> Probability Dice
    4: "logic-gates",       # Discrete Math -> Logic Gates
    5: "prime-hunter",      # Number Theory -> Prime Hunter
}

# Level definitions
LEVELS = [
    {"id": 1, "name": "Calculus Basics", "icon": "01", "topic": "Introduction to Calculus - Limits and Derivatives"},
    {"id": 2, "name": "Linear Algebra", "icon": "02", "topic": "Linear Algebra - Matrices and Vectors"},
    {"id": 3, "name": "Probability", "icon": "03", "topic": "Probability Theory and Statistics"},
    {"id": 4, "name": "Discrete Math", "icon": "04", "topic": "Discrete Mathematics - Sets, Relations, and Logic"},
    {"id": 5, "name": "Number Theory", "icon": "05", "topic": "Number Theory and Cryptography Basics"},
    {"id": 6, "name": "BOSS BATTLE", "icon": "BOSS", "topic": "Advanced Mathematics", "is_boss": True}
]

# Inject game-specific CSS
def inject_game_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            background: linear-gradient(180deg, #0a1a0a 0%, #1a3a1a 50%, #0d2e1a 100%);
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Game Header */
        .game-header {{
            background: linear-gradient(135deg, {GAME_COLOR_1}22, {GAME_COLOR_2}22);
            border: 2px solid {GAME_COLOR_1};
            border-radius: 20px;
            padding: 20px 40px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .game-header-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, {GAME_COLOR_1}, {GAME_COLOR_2});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
        }}
        
        /* Level Node styling */
        .level-badge.completed {{
            background: linear-gradient(135deg, {GAME_COLOR_1}, {GAME_COLOR_2});
            border: 4px solid #ffd700;
            box-shadow: 0 0 20px {GAME_COLOR_1}66;
        }}
        
        .level-badge.current {{
            background: linear-gradient(135deg, {GAME_COLOR_1}88, {GAME_COLOR_2}88);
            border: 4px solid {GAME_COLOR_1};
            animation: currentPulse 2s ease-in-out infinite;
            box-shadow: 0 0 30px {GAME_COLOR_1}88;
        }}
        
        @keyframes currentPulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 20px {GAME_COLOR_1}66; }}
            50% {{ transform: scale(1.05); box-shadow: 0 0 40px {GAME_COLOR_1}aa; }}
        }}
        
        /* Quiz styling */
        .quiz-question {{
            background: linear-gradient(135deg, #1e301e, #2a452a);
            border-left: 4px solid {GAME_COLOR_1};
            padding: 20px;
            margin: 15px 0;
            border-radius: 0 15px 15px 0;
        }}
        
        .quiz-question-number {{
            font-family: 'Orbitron', sans-serif;
            color: {GAME_COLOR_1};
            font-size: 0.85rem;
            margin-bottom: 10px;
        }}
        
        .quiz-question-text {{
            font-family: 'Rajdhani', sans-serif;
            color: #fff;
            font-size: 1.2rem;
        }}
        
        /* Boss Battle styling */
        .boss-container {{
            background: linear-gradient(135deg, #1a3a1a, #0d2e1a);
            border: 3px solid #ffd700;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            animation: bossGlow 2s ease-in-out infinite;
        }}
        
        @keyframes bossGlow {{
            0%, 100% {{ box-shadow: 0 0 20px #ffd70044; }}
            50% {{ box-shadow: 0 0 50px #ffd700aa; }}
        }}
        
        .boss-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            color: #ffd700;
            margin-bottom: 10px;
            letter-spacing: 3px;
        }}
        
        .boss-subtitle {{
            font-family: 'Rajdhani', sans-serif;
            color: #ffee88;
            font-size: 1rem;
            margin-bottom: 20px;
        }}
        
        /* Results */
        .result-correct {{
            background: linear-gradient(135deg, #1a2e1a, #2d442d);
            border-left: 4px solid #00ff88;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
            color: #88ff88;
        }}
        
        .result-wrong {{
            background: linear-gradient(135deg, #2e1a1a, #442d2d);
            border-left: 4px solid #ff4444;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
            color: #ff8888;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_game_header():
    """Render the game header with stats."""
    game_progress = get_game_progress(GAME_ID)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("< BACK TO HUB", key="back_hub"):
            st.session_state.current_game = None
            st.session_state.current_level = None
            st.rerun()
    
    with col2:
        st.markdown(f'''
            <div style="text-align: center;">
                <span style="font-family: 'Orbitron', sans-serif; font-size: 2rem; font-weight: 900; color: {GAME_COLOR_1};">{GAME_ICON}</span>
                <h1 class="game-header-title">{GAME_TITLE}</h1>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div style="text-align: right; padding-top: 20px;">
                <span style="font-family: 'Orbitron', sans-serif; color: {GAME_COLOR_1}; font-size: 1.5rem;">
                    {game_progress["completed_levels"]}/6
                </span>
                <br>
                <span style="font-family: 'Rajdhani', sans-serif; color: #666; font-size: 0.8rem;">
                    LEVELS COMPLETE
                </span>
            </div>
        ''', unsafe_allow_html=True)


def render_learning_path():
    """Render the Duolingo-style learning path."""
    game_progress = get_game_progress(GAME_ID)
    completed = game_progress.get("levels_completed", [])
    
    st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <p style="font-family: 'Rajdhani', sans-serif; color: #888; font-size: 1rem;">
                SELECT A LEVEL TO BEGIN
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create the path layout
    for i, level in enumerate(LEVELS):
        level_id = level["id"]
        is_completed = level_id in completed
        is_boss = level.get("is_boss", False)
        
        # Determine if level is unlocked
        is_unlocked = (level_id == 1) or ((level_id - 1) in completed)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Create clickable button for each level
            button_label = f"L{level['id']}: {level['name']}"
            if is_completed:
                button_label = f"[DONE] {level['name']}"
            elif not is_unlocked:
                button_label = f"[LOCKED] {level['name']}"
            
            if st.button(
                button_label,
                key=f"level_{level_id}",
                disabled=not is_unlocked,
                use_container_width=True
            ):
                st.session_state.current_level = level_id
                st.session_state.show_quiz = False
                st.session_state.show_mini_game = False
                st.session_state.selected_mini_game = None
                st.session_state.explanation_result = None
                st.session_state.boss_mode = is_boss
                st.rerun()
            
            # Visual connector
            if i < len(LEVELS) - 1:
                st.markdown(f"""
                    <div style="text-align: center; color: {GAME_COLOR_1}44; font-size: 1.5rem;">
                        |<br>|
                    </div>
                """, unsafe_allow_html=True)


def render_level_content(level_id):
    """Render the content for a specific level."""
    level = LEVELS[level_id - 1]
    is_boss = level.get("is_boss", False)
    
    if st.button("< Back to Path", key="back_path"):
        st.session_state.current_level = None
        st.session_state.show_quiz = False
        st.session_state.explanation_result = None
        st.session_state.current_quiz = None
        st.rerun()
    
    st.markdown("---")
    
    if is_boss:
        render_boss_battle(level)
    else:
        render_regular_level(level)


def render_regular_level(level):
    """Render a regular learning level."""
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="display: inline-block; width: 80px; height: 80px; border-radius: 20px; background: linear-gradient(135deg, {GAME_COLOR_1}, {GAME_COLOR_2}); display: flex; align-items: center; justify-content: center; margin: 0 auto 15px;">
                <span style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 900; color: #0a0a0f;">{level["icon"]}</span>
            </div>
            <h2 style="font-family: 'Orbitron', sans-serif; color: {GAME_COLOR_1}; letter-spacing: 3px;">
                LEVEL {level["id"]}: {level["name"].upper()}
            </h2>
        </div>
    ''', unsafe_allow_html=True)
    
    # Get the game mapped to this level
    level_game = LEVEL_TO_GAME_MAPPING.get(level["id"])
    available_games = get_available_mini_games()
    game_info = available_games.get(level_game) if level_game else None
    
    col1, col2 = st.columns([2, 1])
    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced", "Expert"],
            key="difficulty_select"
        )
    
    # Action buttons - 3 options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("LEARN CONCEPT", use_container_width=True, type="primary"):
            with st.spinner("Generating explanation..."):
                explanation = explain_topic(level["topic"], difficulty)
                st.session_state.explanation_result = explanation
                st.session_state.show_quiz = False
                st.session_state.show_mini_game = False
                # Initialize chat history for this topic
                st.session_state.chat_history = []
                st.session_state.current_topic = level["topic"]
    
    with col2:
        if st.button("QUIZ", use_container_width=True):
            with st.spinner("Generating quiz..."):
                quiz = generate_quiz(level["topic"], difficulty)
                st.session_state.current_quiz = quiz
                st.session_state.quiz_index = 0
                st.session_state.quiz_answers = [None] * len(quiz)
                st.session_state.quiz_hints = {}  # Track hints per question
                st.session_state.show_quiz = True
                st.session_state.show_mini_game = False
                st.session_state.explanation_result = None
                st.rerun()
    
    with col3:
        # Show the level-specific game button
        game_name = game_info['name'] if game_info else "PLAY GAME"
        game_icon = game_info['icon'] if game_info else ""
        if st.button(f"{game_icon} {game_name.upper()}", use_container_width=True, type="secondary"):
            if level_game:
                st.session_state.selected_mini_game = level_game
                st.session_state.show_mini_game = True
            st.session_state.show_quiz = False
            st.session_state.explanation_result = None
    
    # Show mini-game if active
    if st.session_state.get('show_mini_game', False) and st.session_state.get('selected_mini_game'):
        st.markdown("---")
        mini_game_id = st.session_state.selected_mini_game
        mini_game_info = available_games.get(mini_game_id)
        
        if mini_game_info:
            st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <h3 style="font-family: 'Orbitron', sans-serif; color: {GAME_COLOR_1};">
                        {mini_game_info['icon']} {mini_game_info['name']}
                    </h3>
                    <p style="color: #888; font-family: 'Rajdhani', sans-serif;">
                        {mini_game_info['description']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            render_mini_game(
                game_name=mini_game_id,
                username=st.session_state.username,
                game_id=GAME_ID,
                level_id=level["id"],
                difficulty=difficulty
            )
    elif st.session_state.explanation_result:
        st.markdown("---")
        render_explanation_with_flashcards(st.session_state.explanation_result, GAME_COLOR_1)
        
        # Follow-up Chat Feature
        render_followup_chat(level["topic"], GAME_COLOR_1)
    elif st.session_state.show_quiz and st.session_state.current_quiz:
        render_quiz(level)


def render_followup_chat(topic, game_color):
    """Render the follow-up chat interface for asking questions."""
    st.markdown(f"""
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid {game_color}44;">
            <h3 style="font-family: 'Orbitron', sans-serif; color: {game_color}; text-align: center;">
                ASK FOLLOW-UP QUESTIONS
            </h3>
            <p style="text-align: center; color: #888; font-family: 'Rajdhani', sans-serif;">
                Have doubts? Ask anything about {topic}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, {game_color}22, {game_color}33); 
                            border-radius: 15px; padding: 15px; margin: 10px 0; 
                            border-left: 4px solid {game_color};">
                    <span style="font-family: 'Rajdhani', sans-serif; color: {game_color}; font-weight: 600;">YOU:</span>
                    <p style="font-family: 'Rajdhani', sans-serif; color: #fff; margin: 5px 0 0 0;">{chat["content"]}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e, #2d2d44); 
                            border-radius: 15px; padding: 15px; margin: 10px 0;
                            border-left: 4px solid #ffd700;">
                    <span style="font-family: 'Rajdhani', sans-serif; color: #ffd700; font-weight: 600;">AI TUTOR:</span>
                    <p style="font-family: 'Rajdhani', sans-serif; color: #fff; margin: 5px 0 0 0;">{chat["content"]}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_question = st.text_input(
            "Your question",
            placeholder="Type your question here...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button("ASK", use_container_width=True, type="primary")
    
    if send_btn and user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Generate AI response
        with st.spinner("Thinking..."):
            response = get_followup_answer(topic, user_question, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()


def get_followup_answer(topic, question, chat_history):
    """Generate an answer for a follow-up question."""
    from explainer import get_client, MODEL_NAME
    
    try:
        client = get_client()
        
        # Build context from chat history
        context = f"Topic being studied: {topic}\n\n"
        if len(chat_history) > 1:
            context += "Previous conversation:\n"
            for chat in chat_history[:-1]:  # Exclude the current question
                role = "Student" if chat["role"] == "user" else "Tutor"
                context += f"{role}: {chat['content']}\n"
        
        prompt = f"""You are a helpful AI tutor. A student is learning about {topic} and has a follow-up question.

{context}

Current question: {question}

Provide a clear, concise, and helpful answer. Use simple language and examples where appropriate. 
Keep the response focused and under 200 words unless a detailed explanation is truly needed.
Be encouraging and supportive."""

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Sorry, I couldn't process that question. Please try again. (Error: {str(e)})"


def render_quiz(level):
    """Render the quiz interface."""
    quiz = st.session_state.current_quiz
    
    st.markdown("---")
    st.markdown(f'''
        <h3 style="font-family: 'Orbitron', sans-serif; color: {GAME_COLOR_1}; text-align: center;">
            QUIZ CHALLENGE
        </h3>
    ''', unsafe_allow_html=True)
    
    # Initialize hints tracking
    if "quiz_hints" not in st.session_state:
        st.session_state.quiz_hints = {}
    
    current_idx = st.session_state.quiz_index
    
    if current_idx < len(quiz):
        q = quiz[current_idx]
        
        st.markdown(f'''
            <div class="quiz-question">
                <div class="quiz-question-number">QUESTION {current_idx + 1} OF {len(quiz)}</div>
                <div class="quiz-question-text">{q["question"]}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # GET HINT button for this question
        hint_key = f"hint_{current_idx}"
        col_hint1, col_hint2, col_hint3 = st.columns([2, 1, 2])
        with col_hint2:
            if st.button("GET HINT", key=f"hint_btn_{current_idx}", use_container_width=True):
                if hint_key not in st.session_state.quiz_hints:
                    with st.spinner("Getting hint..."):
                        hint = generate_hint(q["question"], q["options"])
                        st.session_state.quiz_hints[hint_key] = hint
                        st.rerun()
        
        # Display hint if available
        if hint_key in st.session_state.quiz_hints:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffd70011, #ffd70022); 
                            border: 1px solid #ffd700; border-radius: 10px; 
                            padding: 15px; margin: 10px 0;">
                    <span style="font-family: 'Rajdhani', sans-serif; color: #ffd700; font-weight: 600;">
                        HINT:
                    </span>
                    <p style="font-family: 'Rajdhani', sans-serif; color: #fff; margin: 5px 0 0 0;">
                        {st.session_state.quiz_hints[hint_key]}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        selected = st.radio(
            "Select your answer:",
            q["options"],
            key=f"quiz_q_{current_idx}",
            index=None,
            label_visibility="collapsed"
        )
        
        if selected:
            st.session_state.quiz_answers[current_idx] = selected[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_idx > 0:
                if st.button("< Previous"):
                    st.session_state.quiz_index -= 1
                    st.rerun()
        
        with col2:
            if current_idx < len(quiz) - 1:
                if st.button("Next >"):
                    st.session_state.quiz_index += 1
                    st.rerun()
        
        with col3:
            if current_idx == len(quiz) - 1:
                if st.button("Submit Quiz", type="primary"):
                    show_quiz_results(quiz, level)


def show_quiz_results(quiz, level):
    """Display quiz results and award XP."""
    answers = st.session_state.quiz_answers
    correct_count = 0
    
    st.markdown("---")
    st.markdown(f'''
        <h3 style="font-family: 'Orbitron', sans-serif; color: {GAME_COLOR_1}; text-align: center;">
            RESULTS
        </h3>
    ''', unsafe_allow_html=True)
    
    for i, (q, user_answer) in enumerate(zip(quiz, answers)):
        correct = q["correct_answer"]
        is_correct = user_answer == correct
        
        if is_correct:
            correct_count += 1
            st.markdown(f'<div class="result-correct">Q{i+1}: [OK] Correct!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-wrong">Q{i+1}: [X] Wrong (Answer: {correct})</div>', unsafe_allow_html=True)
        
        record_answer(is_correct, is_boss_battle=False, game_id=GAME_ID)
    
    xp_earned = correct_count * 10
    accuracy = (correct_count / len(quiz)) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{correct_count}/{len(quiz)}")
    with col2:
        st.metric("Accuracy", f"{accuracy:.0f}%")
    with col3:
        st.metric("XP Earned", f"+{xp_earned}")
    
    if accuracy >= 60:
        complete_level(GAME_ID, level["id"])
        st.success("LEVEL COMPLETE! You've unlocked the next level!")
        st.balloons()
    else:
        st.warning("Score 60% or higher to complete this level. Try again!")
    
    if st.button("Continue"):
        st.session_state.show_quiz = False
        st.session_state.current_quiz = None
        st.session_state.current_level = None
        st.rerun()


def render_boss_battle(level):
    """Render the boss battle interface."""
    st.markdown(f'''
        <div class="boss-container">
            <div class="boss-title">BOSS BATTLE</div>
            <div class="boss-subtitle">Defeat the Math Titan!</div>
            <div style="font-family: 'Orbitron', sans-serif; color: #ffd700; font-size: 1.2rem;">Reward: +50 XP</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("CHALLENGE THE BOSS", type="primary", use_container_width=True):
        with st.spinner("The titan awakens..."):
            boss_q = generate_boss_question(level["topic"], "Expert")
            st.session_state.boss_question = boss_q
            st.rerun()
    
    if hasattr(st.session_state, 'boss_question') and st.session_state.boss_question:
        boss_q = st.session_state.boss_question
        
        st.markdown(f'''
            <div class="quiz-question" style="border-color: #ffd700;">
                <div class="quiz-question-number" style="color: #ffd700;">BOSS CHALLENGE</div>
                <div class="quiz-question-text">{boss_q["question"]}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        selected = st.radio(
            "Choose wisely:",
            boss_q["options"],
            key="boss_answer",
            index=None,
            label_visibility="collapsed"
        )
        
        if st.button("SUBMIT ANSWER", type="primary"):
            if selected:
                user_answer = selected[0]
                correct = boss_q["correct_answer"]
                is_correct = user_answer == correct
                
                record_answer(is_correct, is_boss_battle=True, game_id=GAME_ID)
                
                if is_correct:
                    complete_level(GAME_ID, level["id"])
                    st.balloons()
                    st.success("BOSS DEFEATED! +50 XP")
                else:
                    st.error(f"DEFEATED! The answer was: {correct}")
                
                if "explanation" in boss_q:
                    st.info(f"Explanation: {boss_q['explanation']}")
                
                st.session_state.boss_question = None


def render_maths_game():
    """Main render function for Maths game."""
    inject_game_css()
    render_game_header()
    
    if st.session_state.current_level:
        render_level_content(st.session_state.current_level)
    else:
        render_learning_path()
