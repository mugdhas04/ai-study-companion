"""
Game Library System
===================
Comprehensive game definitions for DSA, DBMS, and Math subjects.
Each game has specific mechanics, objectives, and rewards.
"""

# DSA GAME LIBRARY
DSA_GAMES = {
    "sorting_arena": {
        "id": "sorting_arena",
        "name": "Sorting Arena",
        "icon": "",
        "category": "arrays",
        "difficulty": "Beginner",
        "description": "Swap numbers until sorted. Master different sorting algorithms!",
        "inspired_by": "Bubble pop / tile swap games",
        "gameplay": "Click two numbers to swap them until the array is sorted",
        "modes": ["Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"],
        "mechanics": {
            "swap_based": True,
            "visual_feedback": True,
            "algorithm_comparison": True
        },
        "rewards": {
            "xp_base": 20,
            "xp_perfect": 50,
            "unlocks": "Algorithm Race"
        },
        "file": "sorting-arena"
    },
    "binary_tree_builder": {
        "id": "binary_tree_builder",
        "name": "Binary Tree Builder",
        "icon": "",
        "category": "trees",
        "difficulty": "Intermediate",
        "description": "Build binary search trees by inserting nodes correctly",
        "inspired_by": "Drag-and-drop puzzle games",
        "gameplay": "Insert nodes to build valid BST. Wrong placement breaks the tree!",
        "mechanics": {
            "drag_drop": True,
            "validation": True,
            "visual_tree": True
        },
        "rewards": {
            "xp_base": 30,
            "xp_perfect": 70,
            "unlocks": "Tree Traversal Game"
        },
        "file": "tree-builder"
    },
    "stack_tower": {
        "id": "stack_tower",
        "name": "Stack Tower",
        "icon": "",
        "category": "stacks",
        "difficulty": "Beginner",
        "description": "Perform stack operations to solve challenges",
        "inspired_by": "Stacking tower games",
        "gameplay": "Use PUSH, POP, PEEK to evaluate expressions and solve puzzles",
        "mechanics": {
            "lifo_operations": True,
            "expression_evaluation": True,
            "visual_stack": True
        },
        "rewards": {
            "xp_base": 25,
            "xp_perfect": 60,
            "unlocks": "Queue Traffic Controller"
        },
        "file": "stack-tower"
    },
    "queue_traffic_controller": {
        "id": "queue_traffic_controller",
        "name": "Queue Traffic Controller",
        "icon": "",
        "category": "queues",
        "difficulty": "Beginner",
        "description": "Release cars in FIFO order. Break order = system crash!",
        "inspired_by": "Traffic management games",
        "gameplay": "Cars arrive in queue. Release them in correct FIFO order",
        "mechanics": {
            "fifo_operations": True,
            "time_pressure": True,
            "system_crash": True
        },
        "rewards": {
            "xp_base": 25,
            "xp_perfect": 60,
            "unlocks": "Graph Maze Explorer"
        },
        "file": "queue-controller"
    },
    "graph_maze_explorer": {
        "id": "graph_maze_explorer",
        "name": "Graph Maze Explorer",
        "icon": "",
        "category": "graphs",
        "difficulty": "Advanced",
        "description": "Navigate maze using BFS, DFS, or Dijkstra to find shortest path",
        "inspired_by": "Maze exploration games",
        "gameplay": "Choose algorithm, watch path visualization, find shortest route",
        "mechanics": {
            "algorithm_selection": True,
            "path_visualization": True,
            "algorithm_comparison": True
        },
        "rewards": {
            "xp_base": 40,
            "xp_perfect": 100,
            "unlocks": "Hash Table Defender"
        },
        "file": "graph-explorer"
    },
    "hash_table_defender": {
        "id": "hash_table_defender",
        "name": "Hash Table Defender",
        "icon": "",
        "category": "hashing",
        "difficulty": "Advanced",
        "description": "Store keys in hash table slots. Resolve collisions!",
        "inspired_by": "Tower defense games",
        "gameplay": "Enemies are keys. Store in hash slots. Handle collisions with chaining/probing",
        "mechanics": {
            "hash_function": True,
            "collision_resolution": True,
            "strategy": True
        },
        "rewards": {
            "xp_base": 35,
            "xp_perfect": 80,
            "unlocks": "Algorithm Race"
        },
        "file": "hash-defender"
    },
    "algorithm_race": {
        "id": "algorithm_race",
        "name": "Algorithm Race",
        "icon": "",
        "category": "algorithms",
        "difficulty": "Expert",
        "description": "Watch algorithms race! See performance differences visually",
        "inspired_by": "Racing games",
        "gameplay": "Bubble Sort vs Quick Sort vs Merge Sort. See time differences!",
        "mechanics": {
            "algorithm_comparison": True,
            "visual_race": True,
            "performance_analysis": True
        },
        "rewards": {
            "xp_base": 50,
            "xp_perfect": 120,
            "unlocks": "Algorithm Arena Boss"
        },
        "file": "algorithm-race"
    },
    "algorithm_arena_boss": {
        "id": "algorithm_arena_boss",
        "name": "Algorithm Arena",
        "icon": "",
        "category": "boss",
        "difficulty": "Boss",
        "description": "Design system handling 1M searches/sec. Choose best structure!",
        "inspired_by": "Boss battle games",
        "gameplay": "Multi-stage: Theory -> Implementation -> Optimization",
        "mechanics": {
            "multi_phase": True,
            "design_challenge": True,
            "system_design": True
        },
        "rewards": {
            "xp_base": 200,
            "xp_perfect": 500,
            "unlocks": "Database City World"
        },
        "file": "algorithm-boss"
    }
}

# DBMS GAME LIBRARY
DBMS_GAMES = {
    "sql_detective": {
        "id": "sql_detective",
        "name": "SQL Detective",
        "icon": "",
        "category": "queries",
        "difficulty": "Beginner",
        "description": "Solve data crimes by building SQL queries",
        "inspired_by": "Mystery puzzle games",
        "gameplay": "Mystery: Find users who ordered >3 products. Build the query!",
        "mechanics": {
            "query_building": True,
            "mystery_solving": True,
            "visual_results": True
        },
        "rewards": {
            "xp_base": 25,
            "xp_perfect": 60,
            "unlocks": "Database Architect"
        },
        "file": "sql-detective"
    },
    "database_architect": {
        "id": "database_architect",
        "name": "Database Architect",
        "icon": "",
        "category": "schema",
        "difficulty": "Intermediate",
        "description": "Design database schemas. Drag tables, connect relationships",
        "inspired_by": "City builder games",
        "gameplay": "Build schema: Users -> Orders -> Products. Set keys and relationships",
        "mechanics": {
            "schema_design": True,
            "relationship_mapping": True,
            "key_assignment": True
        },
        "rewards": {
            "xp_base": 35,
            "xp_perfect": 80,
            "unlocks": "Query Optimizer"
        },
        "file": "db-architect"
    },
    "query_optimizer": {
        "id": "query_optimizer",
        "name": "Query Optimizer",
        "icon": "",
        "category": "optimization",
        "difficulty": "Advanced",
        "description": "Fix slow queries using indexes, joins, and filters",
        "inspired_by": "Performance tuning games",
        "gameplay": "Query runs slowly. Add indexes. Performance bar increases!",
        "mechanics": {
            "performance_tuning": True,
            "index_management": True,
            "query_analysis": True
        },
        "rewards": {
            "xp_base": 40,
            "xp_perfect": 100,
            "unlocks": "Transaction Manager"
        },
        "file": "query-optimizer"
    },
    "transaction_manager": {
        "id": "transaction_manager",
        "name": "Transaction Manager",
        "icon": "",
        "category": "transactions",
        "difficulty": "Advanced",
        "description": "Handle simultaneous transactions. Ensure ACID properties!",
        "inspired_by": "Strategy management games",
        "gameplay": "Multiple transactions arrive. Fix dirty reads, lost updates",
        "mechanics": {
            "acid_properties": True,
            "concurrency_control": True,
            "conflict_resolution": True
        },
        "rewards": {
            "xp_base": 45,
            "xp_perfect": 110,
            "unlocks": "Index Hunter"
        },
        "file": "transaction-manager"
    },
    "index_hunter": {
        "id": "index_hunter",
        "name": "Index Hunter",
        "icon": "",
        "category": "indexing",
        "difficulty": "Intermediate",
        "description": "Identify where to add indexes. Watch query time improve!",
        "inspired_by": "Puzzle logic games",
        "gameplay": "Analyze queries. Place indexes strategically. Timer improves!",
        "mechanics": {
            "index_placement": True,
            "performance_analysis": True,
            "strategy": True
        },
        "rewards": {
            "xp_base": 30,
            "xp_perfect": 70,
            "unlocks": "Data Cleanup"
        },
        "file": "index-hunter"
    },
    "data_cleanup": {
        "id": "data_cleanup",
        "name": "Data Cleanup",
        "icon": "",
        "category": "normalization",
        "difficulty": "Intermediate",
        "description": "Normalize tables from 1NF -> 2NF -> 3NF",
        "inspired_by": "Match puzzle games",
        "gameplay": "Duplicate data appears. Split tables to normalize!",
        "mechanics": {
            "normalization": True,
            "table_splitting": True,
            "redundancy_removal": True
        },
        "rewards": {
            "xp_base": 35,
            "xp_perfect": 80,
            "unlocks": "Server Crisis Boss"
        },
        "file": "data-cleanup"
    },
    "server_crisis_boss": {
        "id": "server_crisis_boss",
        "name": "Server Crisis",
        "icon": "",
        "category": "boss",
        "difficulty": "Boss",
        "description": "Database server crashes! Redesign schema, optimize everything!",
        "inspired_by": "Crisis management games",
        "gameplay": "Multi-phase: Fix schema -> Optimize queries -> Add indexes",
        "mechanics": {
            "multi_phase": True,
            "system_rescue": True,
            "complete_optimization": True
        },
        "rewards": {
            "xp_base": 200,
            "xp_perfect": 500,
            "unlocks": "Math Dimension World"
        },
        "file": "server-boss"
    }
}

# MATH GAME LIBRARY
MATH_GAMES = {
    "equation_shooter": {
        "id": "equation_shooter",
        "name": "Equation Shooter",
        "icon": "",
        "category": "algebra",
        "difficulty": "Beginner",
        "description": "Equations fall from sky. Shoot the correct answer!",
        "inspired_by": "Arcade shooter games",
        "gameplay": "2x + 3 = 11 falls down. Click X=4 to shoot!",
        "mechanics": {
            "arcade_shooter": True,
            "time_pressure": True,
            "rapid_solving": True
        },
        "rewards": {
            "xp_base": 20,
            "xp_perfect": 50,
            "unlocks": "Graph Matcher"
        },
        "file": "equation-shooter"
    },
    "graph_matcher": {
        "id": "graph_matcher",
        "name": "Graph Matcher",
        "icon": "",
        "category": "functions",
        "difficulty": "Intermediate",
        "description": "Match graphs to their equations",
        "inspired_by": "Matching puzzle games",
        "gameplay": "Graph shown. Choose: y=x^2, y=2x, y=sin(x)",
        "mechanics": {
            "pattern_matching": True,
            "visual_recognition": True,
            "function_understanding": True
        },
        "rewards": {
            "xp_base": 30,
            "xp_perfect": 70,
            "unlocks": "Geometry Builder"
        },
        "file": "graph-matcher"
    },
    "geometry_builder": {
        "id": "geometry_builder",
        "name": "Geometry Builder",
        "icon": "",
        "category": "geometry",
        "difficulty": "Intermediate",
        "description": "Build shapes using geometric formulas",
        "inspired_by": "Construction games",
        "gameplay": "Build triangle with area 24. Adjust base and height!",
        "mechanics": {
            "shape_building": True,
            "formula_application": True,
            "interactive_adjustment": True
        },
        "rewards": {
            "xp_base": 30,
            "xp_perfect": 70,
            "unlocks": "Probability Casino"
        },
        "file": "geometry-builder"
    },
    "probability_casino": {
        "id": "probability_casino",
        "name": "Probability Casino",
        "icon": "",
        "category": "probability",
        "difficulty": "Advanced",
        "description": "Predict outcomes and calculate probabilities to win coins",
        "inspired_by": "Card probability games",
        "gameplay": "What's P(drawing Ace)? Correct guess earns coins!",
        "mechanics": {
            "probability_calculation": True,
            "prediction": True,
            "reward_system": True
        },
        "rewards": {
            "xp_base": 35,
            "xp_perfect": 80,
            "unlocks": "Calculus Runner"
        },
        "file": "probability-casino"
    },
    "calculus_runner": {
        "id": "calculus_runner",
        "name": "Calculus Runner",
        "icon": "",
        "category": "calculus",
        "difficulty": "Advanced",
        "description": "Endless runner through functions. Pick correct derivatives!",
        "inspired_by": "Endless runner games",
        "gameplay": "Function obstacle appears. Choose correct derivative to jump!",
        "mechanics": {
            "endless_runner": True,
            "quick_decisions": True,
            "calculus_application": True
        },
        "rewards": {
            "xp_base": 40,
            "xp_perfect": 100,
            "unlocks": "Number Labyrinth"
        },
        "file": "calculus-runner"
    },
    "number_labyrinth": {
        "id": "number_labyrinth",
        "name": "Number Labyrinth",
        "icon": "",
        "category": "logic",
        "difficulty": "Expert",
        "description": "Navigate maze by solving math puzzles to open gates",
        "inspired_by": "Puzzle maze games",
        "gameplay": "Gate blocks path. Solve puzzle to open. Navigate to exit!",
        "mechanics": {
            "maze_navigation": True,
            "puzzle_solving": True,
            "strategic_thinking": True
        },
        "rewards": {
            "xp_base": 45,
            "xp_perfect": 110,
            "unlocks": "Math Wizard Boss"
        },
        "file": "number-labyrinth"
    },
    "math_wizard_boss": {
        "id": "math_wizard_boss",
        "name": "Math Wizard Challenge",
        "icon": "",
        "category": "boss",
        "difficulty": "Boss",
        "description": "Timed challenge solving multiple puzzles quickly",
        "inspired_by": "Speed challenge games",
        "gameplay": "10 minutes. Solve algebra, geometry, calculus, probability!",
        "mechanics": {
            "time_limit": True,
            "multi_category": True,
            "speed_challenge": True
        },
        "rewards": {
            "xp_base": 200,
            "xp_perfect": 500,
            "unlocks": "Master Achievement"
        },
        "file": "math-wizard-boss"
    }
}

# Combine all games
ALL_GAMES = {
    **DSA_GAMES,
    **DBMS_GAMES,
    **MATH_GAMES
}


def get_games_by_category(subject: str) -> dict:
    """Get all games for a specific subject."""
    if subject.lower() == "dsa":
        return DSA_GAMES
    elif subject.lower() == "dbms":
        return DBMS_GAMES
    elif subject.lower() == "math":
        return MATH_GAMES
    return {}


def get_game_by_id(game_id: str) -> dict:
    """Get specific game by ID."""
    return ALL_GAMES.get(game_id)


def get_unlocked_games(username: str, subject: str) -> list:
    """Get list of unlocked games for user in subject."""
    from gamification import get_game_progress
    
    progress = get_game_progress(subject.lower())
    unlocked_count = progress.get("completed_levels", 0)
    
    games = get_games_by_category(subject)
    game_list = list(games.values())
    
    # First game always unlocked, then unlock based on progress
    return game_list[:min(unlocked_count + 1, len(game_list))]


def calculate_game_xp(game_id: str, performance: dict) -> int:
    """Calculate XP earned from game based on performance."""
    game = get_game_by_id(game_id)
    if not game:
        return 0
    
    base_xp = game["rewards"]["xp_base"]
    perfect_xp = game["rewards"]["xp_perfect"]
    
    # Calculate based on performance
    score = performance.get("score", 0)
    moves = performance.get("moves", 0)
    time = performance.get("time", 0)
    perfect = performance.get("perfect", False)
    
    if perfect:
        return perfect_xp
    
    # Scale XP based on performance
    xp_range = perfect_xp - base_xp
    performance_ratio = min(score / 100, 1.0)  # Assuming score out of 100
    
    return int(base_xp + (xp_range * performance_ratio))
