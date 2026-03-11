# 🎓 AI Study Game Hub

An AI-powered gamified learning platform where students learn through interactive games, quizzes, and challenges.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Claude](https://img.shields.io/badge/Anthropic-Claude-orange.svg)

---

## 🎮 What It Does

**AI Study Game Hub** transforms learning into a game:

- 📚 **Learn Concepts** - AI explains topics in a visual, conceptual way
- 📝 **Take Quizzes** - Test your understanding with MCQs
- 🎮 **Play Games** - Practice with topic-specific interactive games
- ⚔️ **Boss Battles** - Face challenging final questions
- 🏆 **Earn XP & Level Up** - Track progress and unlock achievements

---

## 🎯 Built-In Courses

| Course | Topics | Levels |
|--------|--------|--------|
| **DSA Adventure** | Arrays, Stacks, Queues, Trees, Graphs, Sorting | 6 |
| **DBMS Quest** | SQL, Normalization, Transactions, ER Models | 6 |
| **Math Arena** | Linear Algebra, Probability, Calculus, Logic | 6 |

---

## ✨ Create Your Own Course

Enter any topic and AI generates a complete learning path:

```
Input: "Machine Learning"

Generated Course:
├── Level 1: Introduction to ML
├── Level 2: Supervised Learning
├── Level 3: Neural Networks
├── Level 4: Deep Learning
├── Level 5: Model Evaluation
└── Boss Battle: Final Challenge
```

Each level includes:
- AI-generated concept explanations
- Interactive quizzes
- Topic-specific games (Matching, Quick Quiz, Sorting)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **AI Model** | Anthropic Claude |
| **Language** | Python 3.8+ |
| **Storage** | JSON files |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-study-companion/
├── app.py                  # Main Streamlit application
├── login.py                # User authentication
├── profile.py              # User profile page
├── explainer.py            # AI concept explanations
├── quiz_generator.py       # Quiz generation
├── gamification.py         # XP, levels, badges system
├── course_generator.py     # Dynamic course creation
├── dynamic_game.py         # Custom course gameplay
├── topic_game_generator.py # Topic-specific mini-games
├── dsa_game.py             # DSA course module
├── dbms_game.py            # DBMS course module
├── maths_game.py           # Math course module
├── components.py           # Shared UI components
├── mini-games/             # HTML/JS arcade games
└── requirements.txt        # Python dependencies
```

---

## 🎮 Game Types

### For Custom Topics (AI-Generated)

| Game | Description |
|------|-------------|
| 🧩 **Concept Match** | Match terms with definitions |
| ⚡ **Quick Quiz** | Answer rapid-fire questions |
| 📦 **Category Sort** | Sort items into categories |

### For Built-In Courses (Arcade)

| Game | Course | Description |
|------|--------|-------------|
| Array Sorter | DSA | Sort arrays visually |
| Stack Tower | DSA | Build and pop stacks |
| Tree Builder | DSA | Construct binary trees |
| SQL Detective | DBMS | Write SQL queries |
| Equation Shooter | Math | Solve equations fast |

---

## 👤 User Features

- **Register/Login** - Save progress across sessions
- **Guest Mode** - Try without registration
- **Profile** - View stats, badges, and activity
- **XP System** - Earn 10-50 XP per correct answer
- **Levels** - Level up every 100 XP

---

## 📄 License

MIT License
