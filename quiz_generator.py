"""
Quiz Generator Module
=====================
Generates quizzes, boss battle questions, and hints using Anthropic Claude API.
"""

import os
import json
import re
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Configure Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = None
if ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Model configuration
MODEL_NAME = "claude-sonnet-4-20250514"

# Difficulty descriptions for each level
DIFFICULTY_PROMPTS = {
    "Beginner": """
        Generate basic questions focusing on:
        - Definitions and terminology
        - Simple facts and fundamentals
        - Recognition of concepts
        - Easy recall questions
        Questions should be straightforward and test basic understanding.
    """,
    "Intermediate": """
        Generate conceptual questions focusing on:
        - Understanding of how concepts work
        - Relationships between ideas
        - Simple applications
        - "Why" and "How" questions
        Questions should test deeper understanding beyond memorization.
    """,
    "Advanced": """
        Generate application-based questions focusing on:
        - Applying concepts to problems
        - Analysis and comparison
        - Problem-solving scenarios
        - Technical details and edge cases
        Questions should require critical thinking and application of knowledge.
    """,
    "Expert": """
        Generate scenario-based questions focusing on:
        - Real-world complex scenarios
        - System design considerations
        - Trade-offs and optimization
        - Advanced edge cases
        - Integration of multiple concepts
        Questions should challenge expert-level understanding.
    """
}


def get_client():
    """
    Get the Anthropic client.
    
    Returns:
        anthropic.Anthropic: Configured Anthropic client instance
        
    Raises:
        ValueError: If API key is not configured
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not found. Please set it in your .env file.")
    
    return client


def parse_quiz_response(response_text):
    """
    Parse the LLM response into structured quiz format.
    
    Args:
        response_text (str): Raw response from the LLM
        
    Returns:
        list: List of question dictionaries
    """
    # Try to extract JSON from the response
    try:
        # Look for JSON array in the response
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if json_match:
            questions = json.loads(json_match.group())
            return questions
    except json.JSONDecodeError:
        pass
    
    # Fallback: Try to parse manually
    questions = []
    
    # Split by question numbers
    parts = re.split(r'\n(?=\d+[\.\)])', response_text)
    
    for part in parts:
        if not part.strip():
            continue
            
        question_dict = {
            "question": "",
            "options": [],
            "correct_answer": ""
        }
        
        lines = part.strip().split('\n')
        
        # Extract question
        if lines:
            # Remove question number prefix
            q_text = re.sub(r'^\d+[\.\)]\s*', '', lines[0])
            question_dict["question"] = q_text.strip()
        
        # Extract options
        options = []
        correct = ""
        for line in lines[1:]:
            line = line.strip()
            # Match options like "A)", "A.", "a)", etc.
            option_match = re.match(r'^([A-Da-d])[\.\)]\s*(.+)', line)
            if option_match:
                option_letter = option_match.group(1).upper()
                option_text = option_match.group(2).strip()
                options.append(f"{option_letter}. {option_text}")
                
                # Check if this is marked as correct
                if '✓' in line or '*' in line or '(correct)' in line.lower():
                    correct = option_letter
            
            # Check for explicit correct answer line
            if 'correct' in line.lower() and 'answer' in line.lower():
                answer_match = re.search(r'[A-Da-d]', line)
                if answer_match:
                    correct = answer_match.group().upper()
        
        if question_dict["question"] and len(options) >= 4:
            question_dict["options"] = options[:4]
            question_dict["correct_answer"] = correct if correct else "A"
            questions.append(question_dict)
    
    return questions


def generate_quiz(topic, level):
    """
    Generate a quiz with 5 MCQ questions about the topic.
    
    Args:
        topic (str): The topic for the quiz (e.g., "OSI Model", "Binary Trees")
        level (str): Skill level - "Beginner", "Intermediate", "Advanced", or "Expert"
        
    Returns:
        list: List of question dictionaries with format:
              {"question": str, "options": list, "correct_answer": str}
    """
    # Validate level
    if level not in DIFFICULTY_PROMPTS:
        level = "Intermediate"
    
    difficulty_instruction = DIFFICULTY_PROMPTS[level]
    
    prompt = f"""
    Generate exactly 5 multiple choice questions about: {topic}
    
    Difficulty Level: {level}
    
    {difficulty_instruction}
    
    IMPORTANT: Return the questions as a valid JSON array with this exact format:
    [
        {{
            "question": "The question text here?",
            "options": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],
            "correct_answer": "A"
        }},
        ...
    ]
    
    Requirements:
    - Generate exactly 5 questions
    - Each question must have exactly 4 options (A, B, C, D)
    - Options must start with the letter followed by a period
    - correct_answer must be just the letter (A, B, C, or D)
    - Questions should be clear and unambiguous
    - Only one answer should be clearly correct
    
    Return ONLY the JSON array, no additional text:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse the response
        questions = parse_quiz_response(message.content[0].text)
        
        # Validate we got questions
        if not questions:
            # Return a fallback error question
            return [{
                "question": f"Error generating quiz about {topic}. Please try again.",
                "options": ["A. Retry", "B. Try different topic", "C. Change level", "D. Contact support"],
                "correct_answer": "A"
            }]
        
        return questions
        
    except Exception as e:
        return [{
            "question": f"Error: {str(e)}",
            "options": ["A. Check API key", "B. Try again", "C. Change topic", "D. Restart app"],
            "correct_answer": "A"
        }]


def generate_boss_question(topic, level):
    """
    Generate a challenging boss battle question worth higher XP.
    Boss questions are harder and more comprehensive than regular quiz questions.
    
    Args:
        topic (str): The topic for the boss question
        level (str): Skill level (boss questions are always challenging)
        
    Returns:
        dict: Single question dictionary with format:
              {"question": str, "options": list, "correct_answer": str, "explanation": str}
    """
    # Boss questions are always at least Advanced difficulty
    if level in ["Beginner", "Intermediate"]:
        effective_level = "Advanced"
    else:
        effective_level = "Expert"
    
    prompt = f"""
    Generate ONE challenging "Boss Battle" question about: {topic}
    
    This is a special challenge question that should:
    - Test deep understanding of the topic
    - Require critical thinking and analysis
    - Be more difficult than regular quiz questions
    - Possibly combine multiple concepts
    - Have one clearly correct answer
    
    Level: {effective_level}
    
    Return the question as a valid JSON object with this exact format:
    {{
        "question": "The challenging question text here?",
        "options": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],
        "correct_answer": "A",
        "explanation": "Brief explanation of why this answer is correct"
    }}
    
    Requirements:
    - Question should be comprehensive and challenging
    - Include a scenario or real-world application if possible
    - All options should seem plausible
    - Only one answer should be clearly correct
    - Include a brief explanation for the correct answer
    
    Return ONLY the JSON object, no additional text:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Try to parse JSON from response
        try:
            json_match = re.search(r'\{[\s\S]*\}', message.content[0].text)
            if json_match:
                question = json.loads(json_match.group())
                
                # Ensure all required fields exist
                if "question" in question and "options" in question and "correct_answer" in question:
                    if "explanation" not in question:
                        question["explanation"] = "Great job solving this challenging question!"
                    return question
        except json.JSONDecodeError:
            pass
        
        # Fallback
        return {
            "question": f"Boss Battle: Explain the most critical aspect of {topic} and its real-world implications.",
            "options": [
                "A. Error generating boss question - Try again",
                "B. Could not parse response",
                "C. API response format issue",
                "D. Please retry the boss battle"
            ],
            "correct_answer": "A",
            "explanation": "Please retry the boss battle."
        }
        
    except Exception as e:
        return {
            "question": f"Error generating boss question: {str(e)}",
            "options": ["A. Retry", "B. Check API", "C. Try different topic", "D. Cancel"],
            "correct_answer": "A",
            "explanation": str(e)
        }


def generate_hint(question, options=None):
    """
    Generate a helpful hint for a question without revealing the answer.
    
    Args:
        question (str): The question text
        options (list, optional): List of answer options
        
    Returns:
        str: A helpful hint
    """
    options_text = ""
    if options:
        options_text = f"\nOptions: {', '.join(options)}"
    
    prompt = f"""
    A student is struggling with this question and needs a hint:
    
    Question: {question}{options_text}
    
    Provide a helpful hint that:
    - Guides the student towards understanding the concept
    - Does NOT reveal the correct answer directly
    - Gives a clue or thinking direction
    - Is encouraging and supportive
    - Is concise (2-3 sentences max)
    
    IMPORTANT: Do not mention which option is correct. Only provide conceptual guidance.
    
    Hint:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return f"**Hint:** {message.content[0].text.strip()}"
        
    except Exception as e:
        return f"**Hint:** Think about the core concepts involved. Break down the question and consider what each option implies. You've got this!"


def validate_answer(question, user_answer, correct_answer):
    """
    Validate if the user's answer is correct.
    
    Args:
        question (str): The question text
        user_answer (str): User's selected answer (A, B, C, or D)
        correct_answer (str): The correct answer (A, B, C, or D)
        
    Returns:
        dict: Result containing is_correct, feedback, and explanation
    """
    # Normalize answers
    user_answer = user_answer.strip().upper()
    correct_answer = correct_answer.strip().upper()
    
    is_correct = user_answer == correct_answer
    
    return {
        "is_correct": is_correct,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "feedback": "Correct! Great job!" if is_correct else f"Incorrect. The correct answer was {correct_answer}."
    }


def generate_explanation(question, correct_answer, topic):
    """
    Generate an explanation for why an answer is correct.
    
    Args:
        question (str): The question text
        correct_answer (str): The correct answer
        topic (str): The topic area
        
    Returns:
        str: Explanation of the correct answer
    """
    prompt = f"""
    Explain why this answer is correct:
    
    Topic: {topic}
    Question: {question}
    Correct Answer: {correct_answer}
    
    Provide a clear, educational explanation in 2-3 sentences.
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
        
    except Exception as e:
        return "The correct answer is based on fundamental principles of this topic."


# For testing the module directly
if __name__ == "__main__":
    print("Testing Quiz Generator Module...")
    print("-" * 50)
    
    test_topic = "Binary Search"
    test_level = "Beginner"
    
    print(f"Topic: {test_topic}")
    print(f"Level: {test_level}")
    print("-" * 50)
    
    print("\nGenerating quiz...")
    quiz = generate_quiz(test_topic, test_level)
    
    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i}: {q['question']}")
        for opt in q['options']:
            print(f"   {opt}")
        print(f"   Correct: {q['correct_answer']}")
    
    print("\n" + "-" * 50)
    print("Generating boss question...")
    boss = generate_boss_question(test_topic, test_level)
    print(f"\nBoss: {boss['question']}")
    for opt in boss['options']:
        print(f"   {opt}")
    print(f"   Correct: {boss['correct_answer']}")
