"""
AI Concept Explainer Module
===========================
Uses Anthropic Claude API to explain topics at different skill levels.
"""

import os
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

# Level-specific explanation styles (conceptual, not storytelling)
LEVEL_STYLES = {
    "Beginner": "simple terms with everyday analogies, suitable for someone new to the topic",
    "Intermediate": "clear technical explanations with practical examples, for someone with basic knowledge",
    "Advanced": "in-depth technical analysis with implementation details, for experienced learners",
    "Expert": "comprehensive coverage with edge cases, optimizations, and industry best practices"
}

# Alias for backward compatibility
LEVEL_PROMPTS = LEVEL_STYLES


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


def explain_topic(topic, level):
    """
    Generate a conceptual explanation with visuals and diagrams.
    
    Args:
        topic (str): The topic to explain
        level (str): Skill level
        
    Returns:
        str: Conceptual explanation with visual elements
    """
    # Validate level
    if level not in LEVEL_STYLES:
        raise ValueError(f"Invalid level: {level}. Must be one of: {list(LEVEL_STYLES.keys())}")
    
    style = LEVEL_STYLES[level]
    
    # Conceptual prompt with visuals and diagrams
    prompt = f"""You are an expert educator creating a clear, conceptual explanation.

TOPIC: {topic}
LEVEL: {level} - {style}

Create a structured, visual-rich explanation. Use ASCII diagrams, flowcharts, and code examples.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

---

## 🎯 WHAT IS IT?
[2-3 sentences giving a clear, direct definition. No stories - just explain what this concept IS.]

---

## 🔑 KEY CONCEPTS

### 1. [First Key Concept]
**Definition:** [One clear sentence]
**Visual:**
```
[ASCII diagram, flowchart, or visual representation]
```

### 2. [Second Key Concept]  
**Definition:** [One clear sentence]
**Visual:**
```
[ASCII diagram, flowchart, or visual representation]
```

### 3. [Third Key Concept]
**Definition:** [One clear sentence]
**Visual:**
```
[ASCII diagram, flowchart, or visual representation]
```

---

## 💻 CODE EXAMPLE
```python
# Practical code example demonstrating the concept
# Include comments explaining each step
```

**What this does:** [Brief explanation of the code]

---

## 📊 HOW IT WORKS (Step by Step)

```
[ASCII flowchart or step diagram showing the process]
Example:
INPUT → STEP 1 → STEP 2 → STEP 3 → OUTPUT
```

1. **Step 1:** [What happens first]
2. **Step 2:** [What happens next]
3. **Step 3:** [Final step]

---

## ⚡ QUICK COMPARISON
| Feature | This Concept | Alternative |
|---------|--------------|-------------|
| [Aspect] | [Value] | [Value] |
| [Aspect] | [Value] | [Value] |

---

## 🎓 KEY TAKEAWAYS
- ✅ [Most important point to remember]
- ✅ [Second important point]
- ✅ [Third important point]

---

## 🔗 REAL-WORLD USE
**Where it's used:** [Specific applications]
**Why it matters:** [Practical importance]

---

IMPORTANT RULES:
- NO storytelling or narrative - be direct and educational
- Use ASCII art/diagrams to visualize concepts
- Include working code examples where relevant
- Use tables for comparisons
- Use emojis for section headers for visual appeal
- Keep explanations concise but complete
- Tailor complexity to {level} level"""
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "authentication" in error_msg.lower():
            return "Error: Invalid or missing API key. Please check your ANTHROPIC_API_KEY in the .env file."
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return "Error: API quota exceeded. Please try again later or check your API limits."
        else:
            return f"Error generating explanation: {error_msg}"


def explain_with_examples(topic, level, num_examples=3):
    """
    Generate an explanation with a specific number of examples.
    
    Args:
        topic (str): The topic to explain
        level (str): Skill level
        num_examples (int): Number of examples to include
        
    Returns:
        str: Explanation with examples
    """
    level_instruction = LEVEL_PROMPTS.get(level, LEVEL_PROMPTS["Intermediate"])
    
    prompt = f"""
    You are an expert tutor helping students learn effectively.
    
    Topic to explain: {topic}
    
    Level: {level}
    
    Instructions:
    {level_instruction}
    
    IMPORTANT: Include exactly {num_examples} clear, practical examples that illustrate the concept.
    
    Format your response as follows:
    1. Brief overview of the topic
    2. Key concepts explained with bullet points
    3. {num_examples} numbered examples
    4. Summary of key takeaways
    
    Provide the explanation now:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"❌ Error generating explanation: {str(e)}"


def quick_explain(topic):
    """
    Generate a quick, concise explanation of a topic.
    Useful for quick reference or review.
    
    Args:
        topic (str): The topic to explain
        
    Returns:
        str: Brief explanation (2-3 sentences)
    """
    prompt = f"""
    Provide a very brief, clear explanation of: {topic}
    
    Requirements:
    - Maximum 3 sentences
    - Focus on the core concept only
    - Make it memorable and easy to understand
    
    Brief explanation:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def compare_topics(topic1, topic2, level="Intermediate"):
    """
    Generate a comparison between two related topics.
    
    Args:
        topic1 (str): First topic
        topic2 (str): Second topic
        level (str): Skill level for the explanation
        
    Returns:
        str: Comparison of the two topics
    """
    level_instruction = LEVEL_PROMPTS.get(level, LEVEL_PROMPTS["Intermediate"])
    
    prompt = f"""
    You are an expert tutor helping students understand the differences and similarities between concepts.
    
    Compare these two topics:
    1. {topic1}
    2. {topic2}
    
    Level: {level}
    
    Instructions:
    {level_instruction}
    
    Format your response as follows:
    - Brief overview of each topic
    - Key similarities (bullet points)
    - Key differences (bullet points)
    - When to use each one
    - Summary
    
    Provide the comparison now:
    """
    
    try:
        api_client = get_client()
        message = api_client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"❌ Error generating comparison: {str(e)}"


# For testing the module directly
if __name__ == "__main__":
    # Test the explainer
    print("Testing AI Explainer Module...")
    print("-" * 50)
    
    test_topic = "Binary Search"
    test_level = "Beginner"
    
    print(f"Topic: {test_topic}")
    print(f"Level: {test_level}")
    print("-" * 50)
    
    explanation = explain_topic(test_topic, test_level)
    print(explanation)
