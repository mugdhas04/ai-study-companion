"""
Topic Game Generator (Simplified)
==================================
Generates ONE topic-specific game per level using AI.
Simple, focused game types that work for any subject.
"""

import json
import streamlit as st
from explainer import get_client, MODEL_NAME
import random

# Simple game types - only 3 options
GAME_TYPES = {
    "match": {
        "name": "Concept Match",
        "icon": "[M]",
        "description": "Match terms with definitions"
    },
    "quiz": {
        "name": "Quick Quiz", 
        "icon": "[Q]",
        "description": "Answer rapid-fire questions"
    },
    "sort": {
        "name": "Category Sort",
        "icon": "[S]",
        "description": "Sort items into categories"
    }
}


def get_game_for_level(level_number):
    """Assign a game type based on level number."""
    game_cycle = ["match", "quiz", "sort"]
    return game_cycle[(level_number - 1) % 3]


def generate_game_content(topic, level_topic, game_type):
    """Generate game content for the topic."""
    client = get_client()
    
    prompts = {
        "match": f"""Create a matching game for: {level_topic}

Generate 5 term-definition pairs.

Respond ONLY with JSON:
{{
    "pairs": [
        {{"term": "Term1", "definition": "Definition1"}},
        {{"term": "Term2", "definition": "Definition2"}},
        {{"term": "Term3", "definition": "Definition3"}},
        {{"term": "Term4", "definition": "Definition4"}},
        {{"term": "Term5", "definition": "Definition5"}}
    ]
}}""",

        "quiz": f"""Create a quick quiz for: {level_topic}

Generate 5 multiple choice questions.

Respond ONLY with JSON:
{{
    "questions": [
        {{
            "question": "Question text?",
            "options": ["A", "B", "C", "D"],
            "correct": 0,
            "explanation": "Why this is correct"
        }}
    ]
}}""",

        "sort": f"""Create a sorting game for: {level_topic}

Create 2 categories with 4 items each that students must sort.

Respond ONLY with JSON:
{{
    "category1": {{"name": "Category 1", "items": ["item1", "item2", "item3", "item4"]}},
    "category2": {{"name": "Category 2", "items": ["item5", "item6", "item7", "item8"]}}
}}"""
    }
    
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompts[game_type]}]
        )
        
        content = response.content[0].text.strip()
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content)
        
    except Exception as e:
        st.error(f"Error generating game: {e}")
        return None


def render_topic_game(topic, level_name, level_topic, level_number, total_levels, colors):
    """Render the topic-specific game for this level."""
    color_1, color_2 = colors
    
    game_type = get_game_for_level(level_number)
    game_info = GAME_TYPES[game_type]
    
    game_key = f"topic_game_{topic}_{level_number}"
    
    # Initialize game state (also reset if old format)
    if game_key not in st.session_state or "data" not in st.session_state[game_key]:
        st.session_state[game_key] = {
            "data": None,
            "score": 0,
            "completed": False,
            "current_idx": 0,
            "matched": [],
            "sorted": {"cat1": [], "cat2": []},
            "shuffled": None
        }
    
    state = st.session_state[game_key]
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color_1}22, {color_2}22);
                border: 2px solid {color_1}; border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <h3 style="color: {color_1}; margin: 0;">
            {game_info['icon']} {game_info['name']}: {level_topic}
        </h3>
        <p style="color: #888; margin: 5px 0 0 0;">{game_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate game data if not exists
    if state["data"] is None:
        if st.button("Start Game", type="primary", use_container_width=True):
            with st.spinner(f"Creating {game_info['name']} for {level_topic}..."):
                data = generate_game_content(topic, level_topic, game_type)
                if data:
                    state["data"] = data
                    st.rerun()
        return
    
    # Render game based on type
    if game_type == "match":
        render_match_game(state, colors)
    elif game_type == "quiz":
        render_quiz_game(state, colors)
    elif game_type == "sort":
        render_sort_game(state, colors)
    
    # Reset button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again"):
            st.session_state[game_key] = {
                "data": None, "score": 0, "completed": False,
                "current_idx": 0, "matched": [], 
                "sorted": {"cat1": [], "cat2": []}, "shuffled": None
            }
            st.rerun()


def render_match_game(state, colors):
    """Render matching game."""
    color_1, color_2 = colors
    data = state["data"]
    pairs = data.get("pairs", [])
    
    if not pairs:
        st.error("No pairs available")
        return
    
    matched = state["matched"]
    
    # Check completion
    if len(matched) >= len(pairs):
        st.success(f"All matched! Score: {state['score']} points")
        state["completed"] = True
        return
    
    # Shuffle on first load
    if state["shuffled"] is None:
        terms = [p["term"] for p in pairs]
        definitions = [p["definition"] for p in pairs]
        random.shuffle(terms)
        random.shuffle(definitions)
        state["shuffled"] = {"terms": terms, "definitions": definitions}
        state["selected_term"] = None
        state["selected_def"] = None
    
    st.markdown("### Match terms with definitions")
    st.markdown(f"**Score: {state['score']}** | Matched: {len(matched)}/{len(pairs)}")
    
    col1, col2 = st.columns(2)
    
    # Terms column
    with col1:
        st.markdown(f"**Terms**")
        for term in state["shuffled"]["terms"]:
            # Check if already matched
            is_matched = any(pairs[i]["term"] == term for i in matched)
            if is_matched:
                st.markdown(f"~~{term}~~ [done]")
            else:
                is_selected = state.get("selected_term") == term
                if st.button(
                    f"{'> ' if is_selected else ''}{term}",
                    key=f"term_{term}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    state["selected_term"] = term
                    check_match(state, pairs, matched)
                    st.rerun()
    
    # Definitions column
    with col2:
        st.markdown(f"**Definitions**")
        for defn in state["shuffled"]["definitions"]:
            is_matched = any(pairs[i]["definition"] == defn for i in matched)
            if is_matched:
                st.markdown(f"~~{defn[:40]}...~~ [done]" if len(defn) > 40 else f"~~{defn}~~ [done]")
            else:
                is_selected = state.get("selected_def") == defn
                display = defn[:40] + "..." if len(defn) > 40 else defn
                if st.button(
                    f"{'> ' if is_selected else ''}{display}",
                    key=f"def_{defn[:30]}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                    help=defn
                ):
                    state["selected_def"] = defn
                    check_match(state, pairs, matched)
                    st.rerun()
    
    st.progress(len(matched) / len(pairs))


def check_match(state, pairs, matched):
    """Check if selected term and definition match."""
    term = state.get("selected_term")
    defn = state.get("selected_def")
    
    if term and defn:
        # Find match
        for idx, pair in enumerate(pairs):
            if pair["term"] == term and pair["definition"] == defn:
                matched.append(idx)
                state["score"] += 20
                st.toast("Correct match!")
                break
        else:
            st.toast("Not a match")
        
        state["selected_term"] = None
        state["selected_def"] = None


def render_quiz_game(state, colors):
    """Render quiz game."""
    color_1, color_2 = colors
    data = state["data"]
    questions = data.get("questions", [])
    
    if not questions:
        st.error("No questions available")
        return
    
    current = state["current_idx"]
    
    # Check completion
    if current >= len(questions):
        accuracy = (state["score"] / (len(questions) * 20)) * 100
        st.success(f"Quiz Complete! Score: {state['score']} ({accuracy:.0f}% accuracy)")
        state["completed"] = True
        return
    
    q = questions[current]
    
    st.markdown(f"**Question {current + 1} of {len(questions)}** | Score: {state['score']}")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color_1}22, {color_2}22);
                border-radius: 10px; padding: 20px; margin: 15px 0;">
        <h4 style="color: white; margin: 0;">{q['question']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    options = q.get("options", [])
    for idx, opt in enumerate(options):
        if st.button(f"{chr(65+idx)}. {opt}", key=f"quiz_opt_{current}_{idx}", use_container_width=True):
            correct = q.get("correct", 0)
            if idx == correct:
                st.success(f"Correct! {q.get('explanation', '')}")
                state["score"] += 20
            else:
                st.error(f"Wrong. {q.get('explanation', '')}")
            state["current_idx"] = current + 1
            st.rerun()
    
    st.progress((current) / len(questions))


def render_sort_game(state, colors):
    """Render sorting game."""
    color_1, color_2 = colors
    data = state["data"]
    
    cat1 = data.get("category1", {})
    cat2 = data.get("category2", {})
    
    if not cat1 or not cat2:
        st.error("Categories not available")
        return
    
    # Initialize shuffled items
    if state["shuffled"] is None:
        all_items = []
        for item in cat1.get("items", []):
            all_items.append({"item": item, "correct_cat": 1})
        for item in cat2.get("items", []):
            all_items.append({"item": item, "correct_cat": 2})
        random.shuffle(all_items)
        state["shuffled"] = all_items
        state["current_idx"] = 0
    
    sorted_items = state["sorted"]
    current = state["current_idx"]
    all_items = state["shuffled"]
    
    # Check completion
    if current >= len(all_items):
        # Calculate score
        correct = 0
        for item in sorted_items["cat1"]:
            if item["correct_cat"] == 1:
                correct += 1
        for item in sorted_items["cat2"]:
            if item["correct_cat"] == 2:
                correct += 1
        
        st.success(f"Sorted! {correct}/{len(all_items)} correct")
        state["completed"] = True
        return
    
    current_item = all_items[current]
    
    st.markdown(f"**Sort this item:** | Progress: {current}/{len(all_items)}")
    
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, {color_1}33, {color_2}33);
                border-radius: 15px; padding: 25px; margin: 20px 0;">
        <h2 style="color: white; margin: 0;">{current_item['item']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{cat1['name']}**")
        if st.button(f"Add to {cat1['name']}", key="sort_1", use_container_width=True, type="primary"):
            sorted_items["cat1"].append(current_item)
            is_correct = current_item["correct_cat"] == 1
            if is_correct:
                st.toast("Correct!")
                state["score"] += 15
            else:
                st.toast("Wrong category")
            state["current_idx"] = current + 1
            st.rerun()
        
        for item in sorted_items["cat1"]:
            mark = "[OK]" if item["correct_cat"] == 1 else "[X]"
            st.markdown(f"- {item['item']} {mark}")
    
    with col2:
        st.markdown(f"**{cat2['name']}**")
        if st.button(f"Add to {cat2['name']}", key="sort_2", use_container_width=True, type="primary"):
            sorted_items["cat2"].append(current_item)
            is_correct = current_item["correct_cat"] == 2
            if is_correct:
                st.toast("Correct!")
                state["score"] += 15
            else:
                st.toast("Wrong category")
            state["current_idx"] = current + 1
            st.rerun()
        
        for item in sorted_items["cat2"]:
            mark = "[OK]" if item["correct_cat"] == 2 else "[X]"
            st.markdown(f"- {item['item']} {mark}")
    
    st.progress(current / len(all_items))
