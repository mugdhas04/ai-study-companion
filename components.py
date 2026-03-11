"""
Interactive UI Components
=========================
Reusable interactive components for the game hub.
"""

import streamlit as st
import re


def parse_flashcards(explanation_text):
    """
    Parse flashcards from the AI-generated explanation.
    
    Args:
        explanation_text (str): The full explanation with flashcard markdown
        
    Returns:
        list: List of flashcard dictionaries with title, idea, visual, remember
    """
    flashcards = []
    
    # Find all CARD sections
    card_pattern = r'###\s*CARD\s*\d+:\s*(.+?)\n\*\*THE IDEA:\*\*\s*(.+?)\n\*\*VISUAL:\*\*\s*(.+?)\n\*\*REMEMBER:\*\*\s*(.+?)(?=\n###|\n---|\n##|$)'
    
    matches = re.findall(card_pattern, explanation_text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        flashcards.append({
            "title": match[0].strip(),
            "idea": match[1].strip(),
            "visual": match[2].strip(),
            "remember": match[3].strip()
        })
    
    return flashcards


def render_interactive_flashcards(flashcards, game_color="#00ff88"):
    """
    Render interactive flip flashcards.
    
    Args:
        flashcards (list): List of flashcard dictionaries
        game_color (str): Accent color for the game theme
    """
    if not flashcards:
        return
    
    # Initialize flip states
    if "flipped_cards" not in st.session_state:
        st.session_state.flipped_cards = {}
    
    st.markdown(f"""
    <style>
        .flashcard-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }}
        
        .flashcard {{
            width: 280px;
            height: 200px;
            perspective: 1000px;
            cursor: pointer;
        }}
        
        .flashcard-inner {{
            position: relative;
            width: 100%;
            height: 100%;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }}
        
        .flashcard-front, .flashcard-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 15px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        
        .flashcard-front {{
            background: linear-gradient(135deg, {game_color}22, {game_color}44);
            border: 2px solid {game_color};
        }}
        
        .flashcard-back {{
            background: linear-gradient(135deg, #1a1a2e, #2d2d44);
            border: 2px solid {game_color}88;
            transform: rotateY(180deg);
        }}
        
        .flashcard-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
            color: {game_color};
            margin-bottom: 10px;
        }}
        
        .flashcard-hint {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.8rem;
            color: #666;
        }}
        
        .flashcard-content {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.95rem;
            color: #fff;
            line-height: 1.4;
        }}
        
        .flashcard-remember {{
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.85rem;
            color: #ffd700;
            margin-top: 10px;
            font-style: italic;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <h3 style="font-family: 'Orbitron', sans-serif; color: {game_color}; text-align: center; margin: 20px 0;">
            KEY CONCEPT CARDS
        </h3>
        <p style="text-align: center; color: #888; font-family: 'Rajdhani', sans-serif;">
            Click a card to flip and reveal more details
        </p>
    """, unsafe_allow_html=True)
    
    # Create columns for cards
    cols = st.columns(min(3, len(flashcards)))
    
    for idx, card in enumerate(flashcards):
        col_idx = idx % len(cols)
        card_key = f"card_{idx}"
        
        with cols[col_idx]:
            # Check if this card is flipped
            is_flipped = st.session_state.flipped_cards.get(card_key, False)
            
            # Render the card
            if not is_flipped:
                # FRONT of card
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {game_color}22, {game_color}44);
                        border: 2px solid {game_color};
                        border-radius: 15px;
                        padding: 25px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-bottom: 15px;
                    ">
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1rem; color: {game_color}; margin-bottom: 15px;">
                            {card['title']}
                        </div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: #fff; line-height: 1.5;">
                            {card['idea']}
                        </div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.75rem; color: #888; margin-top: 15px;">
                            TAP TO FLIP
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # BACK of card
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1a1a2e, #2d2d44);
                        border: 2px solid {game_color}88;
                        border-radius: 15px;
                        padding: 25px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        text-align: center;
                        margin-bottom: 15px;
                    ">
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.85rem; color: #aaa; margin-bottom: 10px;">
                            VISUAL
                        </div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: #fff; line-height: 1.4;">
                            {card['visual']}
                        </div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.85rem; color: #ffd700; margin-top: 15px; font-style: italic;">
                            {card['remember']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Flip button
            if st.button("FLIP" if not is_flipped else "FLIP BACK", key=f"flip_{idx}", use_container_width=True):
                st.session_state.flipped_cards[card_key] = not is_flipped
                st.rerun()


def render_explanation_with_flashcards(explanation_text, game_color="#00ff88"):
    """
    Render the full explanation with interactive flashcards.
    
    Args:
        explanation_text (str): The AI-generated explanation
        game_color (str): Accent color for styling
    """
    # Parse flashcards
    flashcards = parse_flashcards(explanation_text)
    
    # Split content into sections
    sections = explanation_text.split("---")
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Check if this is the flashcard section
        if "KEY CONCEPT CARDS" in section.upper() or "CARD 1:" in section:
            # Render interactive flashcards instead
            if flashcards:
                render_interactive_flashcards(flashcards, game_color)
        else:
            # Render other sections as styled markdown
            # Style chapter headers
            if "CHAPTER" in section:
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1a1a2e, #2d2d44);
                        border-left: 4px solid {game_color};
                        padding: 20px;
                        margin: 15px 0;
                        border-radius: 0 15px 15px 0;
                    ">
                """, unsafe_allow_html=True)
                st.markdown(section)
                st.markdown("</div>", unsafe_allow_html=True)
            elif "REAL WORLD" in section.upper() or "PRO TIP" in section.upper() or "CHALLENGE" in section.upper():
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {game_color}11, {game_color}22);
                        border: 1px solid {game_color}44;
                        padding: 20px;
                        margin: 15px 0;
                        border-radius: 15px;
                    ">
                """, unsafe_allow_html=True)
                st.markdown(section)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(section)
