/**
 * Algorithm Arena Boss Battle
 * Epic 3-phase algorithm challenge boss fight
 */

class AlgorithmBoss {
    constructor() {
        this.level = 1;
        this.difficulty = 'normal';
        this.phase = 1;
        this.maxPhase = 3;
        
        // Boss stats
        this.bossMaxHP = 1000;
        this.bossHP = 1000;
        this.bossName = "The Algorithm Oracle";
        
        // Player stats
        this.playerMaxHP = 100;
        this.playerHP = 100;
        this.combo = 0;
        this.maxCombo = 0;
        
        // Scoring
        this.score = 0;
        this.questionsAnswered = 0;
        this.correctAnswers = 0;
        this.totalQuestions = 0;
        
        // Phase tracking
        this.phaseQuestions = 0;
        this.questionsPerPhase = 5;
        
        // Combat
        this.baseDamage = 80;
        this.criticalMultiplier = 2;
        this.bossDamage = 15;
        
        // Time
        this.timeLimit = 300; // 5 minutes
        this.timer = null;
        this.timeRemaining = this.timeLimit;
        
        // Questions for each phase
        this.questionBank = {
            theory: [],
            design: [],
            optimize: []
        };
        
        this.currentQuestion = null;
        this.gameActive = false;
        
        this.initURLParams();
        this.loadQuestionBank();
    }
    
    initURLParams() {
        const params = new URLSearchParams(window.location.search);
        this.level = parseInt(params.get('level')) || 1;
        this.difficulty = params.get('difficulty') || 'normal';
        
        // Scale based on level
        const levelScale = 1 + (this.level - 1) * 0.15;
        this.bossMaxHP = Math.floor(1000 * levelScale);
        this.bossHP = this.bossMaxHP;
        this.timeLimit = Math.max(180, 300 - (this.level * 10)); // Less time at higher levels
        this.timeRemaining = this.timeLimit;
        
        // Increase boss damage at higher levels
        this.bossDamage = Math.floor(15 + (this.level * 2));
        
        // Update boss name based on level
        const bossNames = [
            "The Algorithm Apprentice",
            "The Complexity Guardian",
            "The Data Structure Keeper",
            "The Algorithm Oracle",
            "The Efficiency Overlord",
            "The Big O Titan",
            "The Ultimate Algorithm Dragon"
        ];
        this.bossName = bossNames[Math.min(this.level - 1, bossNames.length - 1)];
        
        // Update displays
        document.querySelector('.boss-name').textContent = `🐉 ${this.bossName}`;
        document.getElementById('bossHPText').textContent = `${this.bossMaxHP}/${this.bossMaxHP}`;
    }
    
    loadQuestionBank() {
        // Phase 1: Theory - Time complexity questions
        this.questionBank.theory = [
            {
                question: "What is the time complexity of accessing an element in an array by index?",
                options: ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                correct: 0,
                damage: 80
            },
            {
                question: "What is the time complexity of binary search?",
                options: ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                correct: 1,
                damage: 80
            },
            {
                question: "What is the worst-case time complexity of quicksort?",
                options: ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
                correct: 1,
                damage: 100
            },
            {
                question: "What is the space complexity of merge sort?",
                options: ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                correct: 2,
                damage: 80
            },
            {
                question: "Which sorting algorithm has the best worst-case time complexity?",
                options: ["Quick Sort", "Bubble Sort", "Merge Sort", "Selection Sort"],
                correct: 2,
                damage: 100
            },
            {
                question: "What is the time complexity of inserting at the beginning of a linked list?",
                options: ["O(n)", "O(1)", "O(log n)", "O(n²)"],
                correct: 1,
                damage: 80
            },
            {
                question: "What is the amortized time complexity of push operation in dynamic arrays?",
                options: ["O(n)", "O(1)", "O(log n)", "O(n²)"],
                correct: 1,
                damage: 100
            },
            {
                question: "What is the time complexity of searching in a hash table (average case)?",
                options: ["O(n)", "O(log n)", "O(1)", "O(n²)"],
                correct: 2,
                damage: 80
            },
            {
                question: "What is the time complexity of DFS traversal in a graph with V vertices and E edges?",
                options: ["O(V)", "O(E)", "O(V + E)", "O(V * E)"],
                correct: 2,
                damage: 100
            },
            {
                question: "What is the time complexity of finding minimum in a min-heap?",
                options: ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                correct: 0,
                damage: 80
            }
        ];
        
        // Phase 2: Design - Data structure choice questions
        this.questionBank.design = [
            {
                question: "Which data structure is best for implementing an undo feature?",
                options: ["Queue", "Stack", "Array", "Graph"],
                correct: 1,
                damage: 100
            },
            {
                question: "Which data structure would you use for a job scheduler (first come, first served)?",
                options: ["Stack", "Tree", "Queue", "Hash Table"],
                correct: 2,
                damage: 100
            },
            {
                question: "Which data structure is best for implementing autocomplete?",
                options: ["Array", "Linked List", "Trie", "Stack"],
                correct: 2,
                damage: 120
            },
            {
                question: "Which data structure would you use to find the shortest path in an unweighted graph?",
                options: ["DFS", "BFS", "Heap", "Stack"],
                correct: 1,
                damage: 100
            },
            {
                question: "Which data structure is best for maintaining a leaderboard with top K scores?",
                options: ["Array", "Heap", "Stack", "Queue"],
                correct: 1,
                damage: 120
            },
            {
                question: "Which data structure is ideal for implementing a spell checker?",
                options: ["Array", "Linked List", "Hash Set", "Stack"],
                correct: 2,
                damage: 100
            },
            {
                question: "Which algorithm is best for detecting a cycle in a linked list?",
                options: ["DFS", "BFS", "Floyd's Cycle Detection", "Binary Search"],
                correct: 2,
                damage: 120
            },
            {
                question: "Which data structure is best for implementing browser history (forward/back)?",
                options: ["Queue", "Two Stacks", "Array", "Heap"],
                correct: 1,
                damage: 100
            },
            {
                question: "Which algorithm is best for finding the shortest path in a weighted graph?",
                options: ["BFS", "DFS", "Dijkstra's Algorithm", "Linear Search"],
                correct: 2,
                damage: 120
            },
            {
                question: "Which data structure is best for implementing a priority queue?",
                options: ["Array", "Linked List", "Binary Heap", "Hash Table"],
                correct: 2,
                damage: 100
            }
        ];
        
        // Phase 3: Optimization - Performance challenges
        this.questionBank.optimize = [
            {
                question: "How can you optimize this: Linear search for sorted array?",
                options: ["Use hash table", "Use binary search", "Use bubble sort first", "No optimization possible"],
                correct: 1,
                damage: 150
            },
            {
                question: "What technique reduces repeated calculations in recursive Fibonacci?",
                options: ["Iteration", "Memoization", "Bubble Sort", "Linear Search"],
                correct: 1,
                damage: 150
            },
            {
                question: "How to optimize checking if two strings are anagrams?",
                options: ["Sort both O(n log n)", "Character count array O(n)", "Brute force O(n!)", "Binary search O(log n)"],
                correct: 1,
                damage: 150
            },
            {
                question: "Which technique is used to optimize the 0/1 Knapsack problem?",
                options: ["Greedy", "Dynamic Programming", "Brute Force", "Linear Search"],
                correct: 1,
                damage: 180
            },
            {
                question: "How to find duplicates in an array in O(n) time?",
                options: ["Nested loops", "Sort first", "Use a Hash Set", "Binary search"],
                correct: 2,
                damage: 150
            },
            {
                question: "What's the optimal way to merge K sorted arrays?",
                options: ["Merge one by one O(NK)", "Use min-heap O(N log K)", "Bubble sort all O(N²)", "Random merge O(N)"],
                correct: 1,
                damage: 180
            },
            {
                question: "How to optimize finding the longest common subsequence?",
                options: ["Recursion", "Dynamic Programming with 2D table", "Brute Force", "Greedy"],
                correct: 1,
                damage: 180
            },
            {
                question: "What technique optimizes range sum queries after preprocessing?",
                options: ["Linear scan each time", "Prefix sum array", "Binary search", "Recursion"],
                correct: 1,
                damage: 150
            },
            {
                question: "How to optimize finding median in a data stream?",
                options: ["Sort each time", "Two heaps (max + min)", "Single array", "Binary search tree only"],
                correct: 1,
                damage: 180
            },
            {
                question: "Which technique solves the sliding window maximum problem efficiently?",
                options: ["Nested loops O(nk)", "Monotonic deque O(n)", "Sorting O(n log n)", "Recursion O(2^n)"],
                correct: 1,
                damage: 180
            }
        ];
        
        // Shuffle questions based on level
        this.shuffleQuestions();
    }
    
    shuffleQuestions() {
        // Shuffle each category
        Object.keys(this.questionBank).forEach(key => {
            this.questionBank[key] = this.shuffleArray([...this.questionBank[key]]);
        });
    }
    
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        this.gameActive = true;
        this.phase = 1;
        this.updatePhaseDisplay();
        this.updateBossHP();
        this.updatePlayerHP();
        this.startTimer();
        this.nextQuestion();
        
        this.addCombatLog("⚔️ The battle begins!", "critical");
        this.addCombatLog(`Phase 1: Theory Challenge - Prove your algorithm knowledge!`, "");
    }
    
    startTimer() {
        this.timer = setInterval(() => {
            this.timeRemaining--;
            document.getElementById('timerDisplay').textContent = this.formatTime(this.timeRemaining);
            
            if (this.timeRemaining <= 0) {
                this.endGame(false);
            }
            
            if (this.timeRemaining <= 30) {
                document.getElementById('timerDisplay').style.color = '#e74c3c';
            }
        }, 1000);
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    updatePhaseDisplay() {
        document.getElementById('phaseDisplay').textContent = `${this.phase}/3`;
        
        // Update boss dialog based on phase
        const dialogs = {
            1: "Let's test your theoretical knowledge, warrior!",
            2: "Can you design the right solution?",
            3: "Time for the ultimate optimization challenge!"
        };
        document.getElementById('bossDialog').textContent = dialogs[this.phase];
    }
    
    updateBossHP() {
        const percent = (this.bossHP / this.bossMaxHP) * 100;
        document.getElementById('bossHPFill').style.width = `${percent}%`;
        document.getElementById('bossHP').textContent = `${this.bossHP}/${this.bossMaxHP}`;
    }
    
    updatePlayerHP() {
        const percent = (this.playerHP / this.playerMaxHP) * 100;
        document.getElementById('playerHPFill').style.width = `${percent}%`;
        document.getElementById('playerHP').textContent = `${this.playerHP}/${this.playerMaxHP}`;
    }
    
    getPhaseType() {
        const types = ['theory', 'design', 'optimize'];
        return types[this.phase - 1];
    }
    
    nextQuestion() {
        if (!this.gameActive) return;
        
        const phaseType = this.getPhaseType();
        const questions = this.questionBank[phaseType];
        
        if (questions.length === 0) {
            // Reload and shuffle questions if exhausted
            this.loadQuestionBank();
        }
        
        this.currentQuestion = questions.pop();
        this.totalQuestions++;
        this.displayQuestion();
    }
    
    displayQuestion() {
        const card = document.querySelector('.question-card');
        const q = this.currentQuestion;
        const phaseType = this.getPhaseType();
        
        // Set question type badge
        const typeElement = card.querySelector('.question-type');
        typeElement.textContent = phaseType.toUpperCase();
        typeElement.className = `question-type ${phaseType}`;
        
        // Set damage points
        card.querySelector('.question-points').textContent = `💥 ${q.damage} DMG`;
        
        // Set question text
        card.querySelector('.question-text').textContent = q.question;
        
        // Set answer options
        const optionsContainer = card.querySelector('.answer-options');
        optionsContainer.innerHTML = '';
        
        q.options.forEach((option, index) => {
            const btn = document.createElement('button');
            btn.className = 'answer-btn';
            btn.textContent = option;
            btn.onclick = () => this.checkAnswer(index, btn);
            optionsContainer.appendChild(btn);
        });
    }
    
    checkAnswer(selectedIndex, button) {
        if (!this.gameActive) return;
        
        const q = this.currentQuestion;
        const buttons = document.querySelectorAll('.answer-btn');
        const isCorrect = selectedIndex === q.correct;
        
        // Disable all buttons
        buttons.forEach(btn => btn.disabled = true);
        
        // Show correct/incorrect
        if (isCorrect) {
            button.classList.add('correct');
            this.handleCorrectAnswer(q);
        } else {
            button.classList.add('incorrect');
            buttons[q.correct].classList.add('correct');
            this.handleWrongAnswer();
        }
        
        this.questionsAnswered++;
        this.phaseQuestions++;
        
        // Check phase transition or victory
        setTimeout(() => {
            if (this.bossHP <= 0) {
                this.endGame(true);
                return;
            }
            
            if (this.playerHP <= 0) {
                this.endGame(false);
                return;
            }
            
            // Check for phase transition
            if (this.phaseQuestions >= this.questionsPerPhase && this.phase < this.maxPhase) {
                this.nextPhase();
            } else {
                this.nextQuestion();
            }
        }, 1200);
    }
    
    handleCorrectAnswer(question) {
        this.correctAnswers++;
        this.combo++;
        this.maxCombo = Math.max(this.maxCombo, this.combo);
        
        // Calculate damage
        let damage = question.damage;
        let isCritical = false;
        
        // Combo bonus
        if (this.combo >= 3) {
            damage *= (1 + (this.combo - 2) * 0.2);
        }
        
        // Critical hit chance increases with combo
        if (Math.random() < 0.1 + (this.combo * 0.05)) {
            damage *= this.criticalMultiplier;
            isCritical = true;
        }
        
        damage = Math.floor(damage);
        this.bossHP = Math.max(0, this.bossHP - damage);
        this.score += damage;
        
        this.updateBossHP();
        document.getElementById('damageDisplay').textContent = this.score;
        document.getElementById('comboDisplay').textContent = `x${this.combo}`;
        
        // Animate boss
        document.querySelector('.boss-avatar').style.animation = 'none';
        setTimeout(() => {
            document.querySelector('.boss-avatar').style.animation = 'bossIdle 2s ease-in-out infinite';
        }, 100);
        
        // Combat log
        if (isCritical) {
            this.addCombatLog(`💥 CRITICAL HIT! You deal ${damage} damage! Combo x${this.combo}!`, 'critical');
        } else {
            this.addCombatLog(`⚔️ You deal ${damage} damage to ${this.bossName}!`, 'damage');
        }
    }
    
    handleWrongAnswer() {
        this.combo = 0;
        
        // Boss attacks player
        this.playerHP = Math.max(0, this.playerHP - this.bossDamage);
        this.updatePlayerHP();
        
        document.getElementById('comboDisplay').textContent = `x0`;
        
        this.addCombatLog(`🔥 Wrong answer! ${this.bossName} strikes for ${this.bossDamage} damage!`, 'damage');
    }
    
    nextPhase() {
        this.phase++;
        this.phaseQuestions = 0;
        
        // Heal player slightly between phases
        const healAmount = 20;
        this.playerHP = Math.min(this.playerMaxHP, this.playerHP + healAmount);
        this.updatePlayerHP();
        
        this.updatePhaseDisplay();
        
        const phaseNames = ['', 'Theory', 'Design', 'Optimization'];
        this.addCombatLog(`🎯 PHASE ${this.phase}: ${phaseNames[this.phase]} Challenge begins!`, 'critical');
        this.addCombatLog(`💚 You recovered ${healAmount} HP!`, 'heal');
        
        this.nextQuestion();
    }
    
    addCombatLog(message, type) {
        const log = document.getElementById('combatLog');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = message;
        log.insertBefore(entry, log.firstChild);
        
        // Keep log manageable
        while (log.children.length > 20) {
            log.removeChild(log.lastChild);
        }
    }
    
    endGame(victory) {
        this.gameActive = false;
        clearInterval(this.timer);
        
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        const resultPanel = document.getElementById('resultPanel');
        const icon = document.getElementById('resultIcon');
        const title = document.getElementById('resultTitle');
        const message = document.getElementById('resultText');
        
        if (victory) {
            resultPanel.classList.remove('defeat');
            icon.textContent = '🏆';
            title.textContent = 'BOSS DEFEATED!';
            message.textContent = `You have conquered ${this.bossName}!`;
            
            // Show loot
            document.querySelector('.loot-section').classList.remove('hidden');
        } else {
            resultPanel.classList.add('defeat');
            icon.textContent = '💀';
            title.textContent = 'DEFEATED';
            message.textContent = `${this.bossName} has proven too powerful... for now.`;
            document.querySelector('.loot-section').classList.add('hidden');
        }
        
        // Update stats
        document.getElementById('resultDamage').textContent = this.score;
        document.getElementById('resultCombo').textContent = 'x' + this.maxCombo;
        document.getElementById('resultXP').textContent = '+' + (this.score * 2);
        
        // Report to parent
        this.reportCompletion(victory);
    }
    
    reportCompletion(victory) {
        const result = {
            type: 'gameComplete',
            success: victory,
            score: this.score,
            accuracy: this.questionsAnswered > 0 
                ? Math.round((this.correctAnswers / this.questionsAnswered) * 100) 
                : 0,
            maxCombo: this.maxCombo,
            phasesCompleted: this.phase,
            timeUsed: this.timeLimit - this.timeRemaining,
            bossDefeated: this.bossHP <= 0
        };
        
        try {
            window.parent.postMessage(result, '*');
        } catch (e) {
            console.log('Could not communicate with parent:', e);
        }
    }
    
    claimLoot() {
        // Report loot claimed
        const lootResult = {
            type: 'lootClaimed',
            xp: this.score * 2,
            badge: 'Boss Slayer'
        };
        
        try {
            window.parent.postMessage(lootResult, '*');
        } catch (e) {
            console.log('Could not report loot:', e);
        }
        
        // Close or return
        this.returnToHub();
    }
    
    retry() {
        // Reset game state
        this.bossHP = this.bossMaxHP;
        this.playerHP = this.playerMaxHP;
        this.score = 0;
        this.combo = 0;
        this.maxCombo = 0;
        this.questionsAnswered = 0;
        this.correctAnswers = 0;
        this.totalQuestions = 0;
        this.phase = 1;
        this.phaseQuestions = 0;
        this.timeRemaining = this.timeLimit;
        
        // Reset UI
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('timerDisplay').style.color = '#e74c3c';
        document.getElementById('combatLog').innerHTML = '';
        
        // Reload questions
        this.loadQuestionBank();
        
        // Start fresh
        this.startGame();
    }
    
    returnToHub() {
        try {
            window.parent.postMessage({ type: 'returnToHub' }, '*');
        } catch (e) {
            window.close();
        }
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new AlgorithmBoss();
    
    // Attach button handlers
    document.getElementById('startBtn').addEventListener('click', () => {
        window.game.startGame();
    });
    
    document.getElementById('continueBtn').addEventListener('click', () => {
        window.game.claimLoot();
    });
    
    document.getElementById('retryBtn').addEventListener('click', () => {
        window.game.retry();
    });
});
