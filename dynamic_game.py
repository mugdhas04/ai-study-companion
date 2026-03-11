"""
Dynamic Game Module
===================
Renders and manages gameplay for dynamically generated AI courses.
Reuses the same gamification engine and UI patterns as predefined courses.
"""

import streamlit as st
from explainer import explain_topic
from quiz_generator import generate_quiz, generate_boss_question, generate_hint
from gamification import record_answer, get_game_progress, complete_level, get_progress_summary
from components import render_explanation_with_flashcards
from topic_game_generator import render_topic_game


def inject_dynamic_game_css(color_1, color_2):
    """Inject CSS for dynamic game with custom colors."""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 50%, #0a1a2e 100%);
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        .game-header {{
            background: linear-gradient(135deg, {color_1}22, {color_2}22);
            border: 2px solid {color_1};
            border-radius: 20px;
            padding: 20px 40px;
            margin-bottom: 30px;
        }}
        
        .game-header-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, {color_1}, {color_2});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
        }}
        
        .level-badge {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .level-badge.completed {{
            background: linear-gradient(135deg, {color_1}, {color_2});
            border: 4px solid #ffd700;
            box-shadow: 0 0 20px {color_1}66;
        }}
        
        .level-badge.current {{
            background: linear-gradient(135deg, {color_1}88, {color_2}88);
            border: 4px solid {color_1};
            animation: currentPulse 2s ease-in-out infinite;
        }}
        
        @keyframes currentPulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 20px {color_1}66; }}
            50% {{ transform: scale(1.05); box-shadow: 0 0 40px {color_1}aa; }}
        }}
        
        .level-badge.locked {{
            background: linear-gradient(135deg, #2a2a3a, #1a1a2a);
            border: 4px solid #444;
            opacity: 0.6;
        }}
        
        .level-badge.boss {{
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #ff4444, #ff8800);
            border: 4px solid #ff0000;
            animation: bossPulse 1.5s ease-in-out infinite;
        }}
        
        @keyframes bossPulse {{
            0%, 100% {{ box-shadow: 0 0 20px #ff000044; }}
            50% {{ box-shadow: 0 0 50px #ff0000aa; }}
        }}
        
        .quiz-question {{
            background: linear-gradient(145deg, #1a1a2e, #2d2d44);
            border: 2px solid {color_1}44;
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
        }}
        
        .quiz-question-number {{
            font-family: 'Orbitron', sans-serif;
            color: {color_1};
            font-size: 0.85rem;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        
        .quiz-question-text {{
            font-family: 'Rajdhani', sans-serif;
            color: #fff;
            font-size: 1.2rem;
            line-height: 1.6;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_dynamic_game(course):
    """
    Render a dynamic game based on course structure.
    
    Args:
        course (dict): Course structure from course_generator
    """
    inject_dynamic_game_css(course["color_1"], course["color_2"])
    
    game_id = course["course_id"]
    game_progress = get_game_progress(game_id)
    summary = get_progress_summary()
    
    # If a level is selected, render level content
    if st.session_state.current_level:
        render_dynamic_level(course, st.session_state.current_level)
        return
    
    # Render game landing page (level map)
    render_game_header(course, game_progress, summary)
    render_level_map(course, game_progress)


def render_game_header(course, game_progress, summary):
    """Render the game header with title and stats."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("< BACK TO HUB"):
            st.session_state.current_game = None
            st.session_state.current_level = None
            st.session_state.dynamic_course = None
            st.rerun()
    
    with col2:
        st.markdown(f'''
            <div style="text-align: center;">
                <span style="font-family: 'Orbitron', sans-serif; font-size: 2rem; font-weight: 900; color: {course["color_1"]};">
                    {course["course_title"][:3].upper()}
                </span>
                <h1 class="game-header-title">{course["course_title"]}</h1>
                <p style="font-family: 'Rajdhani', sans-serif; color: #888; margin-top: -10px;">
                    {course["difficulty"]} Level
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    total_levels = course.get("total_levels", len(course.get("levels", [])))
    
    with col3:
        st.markdown(f'''
            <div style="text-align: right; padding-top: 20px;">
                <span style="font-family: 'Orbitron', sans-serif; color: {course["color_1"]}; font-size: 1.5rem;">
                    {game_progress["completed_levels"]}/{total_levels}
                </span>
                <br>
                <span style="font-family: 'Rajdhani', sans-serif; color: #666; font-size: 0.8rem;">
                    LEVELS COMPLETE
                </span>
            </div>
        ''', unsafe_allow_html=True)


def render_level_map(course, game_progress):
    """Render the visual level progression map."""
    st.markdown("<br>", unsafe_allow_html=True)
    
    completed_levels = game_progress.get("levels_completed", [])
    total_completed = len(completed_levels)
    
    # Render levels in a vertical path layout
    for level in course["levels"]:
        level_id = level["id"]
        is_completed = level_id in completed_levels
        is_boss = level.get("is_boss", False)
        is_unlocked = level_id <= total_completed + 1
        
        # Determine badge class
        if is_completed:
            badge_class = "completed"
        elif is_unlocked:
            badge_class = "current"
        else:
            badge_class = "locked"
        
        if is_boss:
            badge_class = "boss" if is_unlocked else "locked"
        
        # Create button label
        button_label = f"L{level_id}: {level['name']}"
        if is_completed:
            button_label = f"[DONE] {level['name']}"
        elif not is_unlocked:
            button_label = f"[LOCKED] {level['name']}"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                button_label,
                key=f"dynamic_level_{level_id}",
                disabled=not is_unlocked,
                use_container_width=True
            ):
                st.session_state.current_level = level_id
                st.session_state.show_quiz = False
                st.session_state.explanation_result = None
                st.session_state.boss_mode = is_boss
                st.rerun()
        
        # Show connector line between levels
        if level_id < 6:
            st.markdown(f'''
                <div style="text-align: center; color: {course["color_1"]}44;">│</div>
            ''', unsafe_allow_html=True)


def render_dynamic_level(course, level_id):
    """Render a specific level's content."""
    level = None
    for lvl in course["levels"]:
        if lvl["id"] == level_id:
            level = lvl
            break
    
    if not level:
        st.error("Level not found")
        return
    
    inject_dynamic_game_css(course["color_1"], course["color_2"])
    
    # Back button
    if st.button("< BACK TO LEVELS"):
        st.session_state.current_level = None
        st.session_state.show_quiz = False
        st.session_state.explanation_result = None
        st.session_state.show_topic_game = False
        st.rerun()
    
    is_boss = level.get("is_boss", False)
    
    if is_boss:
        render_boss_battle(course, level)
    else:
        render_regular_level(course, level)


def render_regular_level(course, level):
    """Render a regular learning level."""
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="display: inline-block; width: 80px; height: 80px; border-radius: 20px; 
                        background: linear-gradient(135deg, {course["color_1"]}, {course["color_2"]}); 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px;">
                <span style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 900; color: #0a0a0f;">
                    {level["icon"]}
                </span>
            </div>
            <h2 style="font-family: 'Orbitron', sans-serif; color: {course["color_1"]}; letter-spacing: 3px;">
                LEVEL {level["id"]}: {level["name"].upper()}
            </h2>
        </div>
    ''', unsafe_allow_html=True)
    
    # Difficulty is already set in course
    difficulty = course.get("difficulty", "Intermediate").capitalize()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 LEARN CONCEPT", use_container_width=True, type="primary"):
            with st.spinner("Generating explanation..."):
                explanation = explain_topic(level["topic"], difficulty)
                st.session_state.explanation_result = explanation
                st.session_state.show_quiz = False
                st.session_state.show_topic_game = False
                st.session_state.chat_history = []
                st.session_state.current_topic = level["topic"]
    
    with col2:
        if st.button("📝 START QUIZ", use_container_width=True):
            with st.spinner("Generating quiz..."):
                quiz = generate_quiz(level["topic"], difficulty)
                st.session_state.current_quiz = quiz
                st.session_state.quiz_index = 0
                st.session_state.quiz_answers = [None] * len(quiz)
                st.session_state.quiz_hints = {}
                st.session_state.show_quiz = True
                st.session_state.show_topic_game = False
                st.session_state.explanation_result = None
                st.rerun()
    
    with col3:
        if st.button("🎮 PLAY GAMES", use_container_width=True):
            st.session_state.show_topic_game = True
            st.session_state.show_quiz = False
            st.session_state.explanation_result = None
            st.rerun()
    
    # Show topic-specific game
    if st.session_state.get('show_topic_game', False):
        st.markdown("---")
        total_levels = len(course.get("levels", []))
        render_topic_game(
            topic=course.get("topic", course.get("course_title", "Topic")),
            level_name=level["name"],
            level_topic=level["topic"],
            level_number=level["id"],
            total_levels=total_levels,
            colors=(course["color_1"], course["color_2"])
        )
    
    # Show explanation
    elif st.session_state.get('explanation_result'):
        st.markdown("---")
        render_explanation_with_flashcards(st.session_state.explanation_result, course["color_1"])
        render_followup_chat(level["topic"], course["color_1"])
    
    # Show quiz
    elif st.session_state.get('show_quiz', False) and st.session_state.get('current_quiz'):
        render_quiz(course, level)


def render_followup_chat(topic, game_color):
    """Render follow-up chat interface."""
    st.markdown(f"""
        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid {game_color}44;">
            <h3 style="font-family: 'Orbitron', sans-serif; color: {game_color}; text-align: center;">
                ASK FOLLOW-UP QUESTIONS
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
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
            key="dynamic_chat_input",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button("ASK", use_container_width=True, type="primary", key="dynamic_send_btn")
    
    if send_btn and user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        with st.spinner("Thinking..."):
            response = get_followup_answer(topic, user_question, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()


def get_followup_answer(topic, question, chat_history):
    """Generate an answer for a follow-up question."""
    from explainer import get_client, MODEL_NAME
    
    try:
        client = get_client()
        
        context = f"Topic being studied: {topic}\n\n"
        if len(chat_history) > 1:
            context += "Previous conversation:\n"
            for chat in chat_history[:-1]:
                role = "Student" if chat["role"] == "user" else "Tutor"
                context += f"{role}: {chat['content']}\n"
        
        prompt = f"""You are a helpful AI tutor. A student is learning about {topic} and has a follow-up question.

{context}

Current question: {question}

Provide a clear, concise, and helpful answer. Keep it under 200 words. Be encouraging."""

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Sorry, I couldn't process that question. Please try again."


def render_quiz(course, level):
    """Render the quiz interface."""
    quiz = st.session_state.current_quiz
    
    st.markdown("---")
    st.markdown(f'''
        <h3 style="font-family: 'Orbitron', sans-serif; color: {course["color_1"]}; text-align: center;">
            QUIZ CHALLENGE
        </h3>
    ''', unsafe_allow_html=True)
    
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
        
        # Hint button
        hint_key = f"hint_{current_idx}"
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("GET HINT", key=f"dyn_hint_btn_{current_idx}", use_container_width=True):
                if hint_key not in st.session_state.quiz_hints:
                    with st.spinner("Getting hint..."):
                        hint = generate_hint(q["question"], q["options"])
                        st.session_state.quiz_hints[hint_key] = hint
                        st.rerun()
        
        # Display hint
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
            key=f"dyn_quiz_q_{current_idx}",
            index=None,
            label_visibility="collapsed"
        )
        
        if selected:
            st.session_state.quiz_answers[current_idx] = selected[0]
        
        # Navigation buttons
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
                    show_quiz_results(course, level, quiz)


def show_quiz_results(course, level, quiz):
    """Show quiz results and award XP."""
    answers = st.session_state.quiz_answers
    correct = 0
    
    for i, q in enumerate(quiz):
        if answers[i] == q.get("correct_answer", q.get("correct", "A")):
            correct += 1
    
    total = len(quiz)
    percentage = (correct / total) * 100
    
    # Record each answer
    for i, q in enumerate(quiz):
        is_correct = answers[i] == q.get("correct_answer", q.get("correct", "A"))
        record_answer(is_correct, game_id=course["course_id"])
    
    # Complete level if passed (60%)
    passed = percentage >= 60
    if passed:
        complete_level(course["course_id"], level["id"])
    
    # Display results
    st.markdown("---")
    result_color = "#00ff88" if passed else "#ff6b6b"
    
    st.markdown(f'''
        <div style="text-align: center; padding: 30px;">
            <h2 style="font-family: 'Orbitron', sans-serif; color: {result_color};">
                {"QUEST COMPLETE!" if passed else "TRY AGAIN"}
            </h2>
            <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.5rem; color: #fff;">
                Score: {correct}/{total} ({percentage:.0f}%)
            </p>
            <p style="font-family: 'Rajdhani', sans-serif; color: #888;">
                {"Level completed! +{} XP".format(correct * 10) if passed else "Need 60% to pass"}
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("RETRY QUIZ"):
            st.session_state.show_quiz = False
            st.rerun()
    with col2:
        if st.button("BACK TO LEVELS"):
            st.session_state.current_level = None
            st.session_state.show_quiz = False
            st.rerun()


def render_boss_battle(course, level):
    """Render the boss battle challenge."""
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 4rem; margin-bottom: 10px;">BOSS</div>
            <h2 style="font-family: 'Orbitron', sans-serif; color: #ff4444; letter-spacing: 3px;">
                BOSS BATTLE
            </h2>
            <p style="font-family: 'Rajdhani', sans-serif; color: #ff8800; font-size: 1.2rem;">
                Defeat the Final Challenge!
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    if "boss_question" not in st.session_state or st.session_state.boss_question is None:
        if st.button("CHALLENGE THE BOSS", type="primary", use_container_width=True):
            with st.spinner("The boss approaches..."):
                boss_q = generate_boss_question(level["topic"], course.get("difficulty", "Intermediate").capitalize())
                st.session_state.boss_question = boss_q
                st.session_state.boss_answered = False
                st.rerun()
    else:
        boss_q = st.session_state.boss_question
        
        st.markdown(f'''
            <div style="background: linear-gradient(145deg, #2a1a1a, #3a2a2a); 
                        border: 2px solid #ff4444; border-radius: 20px; 
                        padding: 30px; margin: 20px 0;">
                <p style="font-family: 'Rajdhani', sans-serif; color: #fff; font-size: 1.2rem;">
                    {boss_q["question"]}
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        selected = st.radio(
            "Choose your answer:",
            boss_q["options"],
            key="boss_answer_dynamic",
            index=None,
            label_visibility="collapsed"
        )
        
        if selected and not st.session_state.boss_answered:
            if st.button("SUBMIT ANSWER", type="primary"):
                is_correct = selected[0] == boss_q["correct"]
                st.session_state.boss_answered = True
                
                result = record_answer(is_correct, is_boss_battle=True, game_id=course["course_id"])
                
                if is_correct:
                    complete_level(course["course_id"], level["id"])
                    st.balloons()
                    st.success(f"BOSS DEFEATED! +{result['xp_gained']} XP")
                else:
                    st.error("The boss wins this round. Try again!")
                
                st.session_state.boss_question = None
                st.rerun()
