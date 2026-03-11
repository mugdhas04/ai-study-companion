/**
 * Algorithm Race Game
 * Watch algorithms compete and learn time complexity
 * Complexity increases with each level via AI parameters
 */

class AlgorithmRace {
    constructor() {
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        this.level = parseInt(this.params.levelId) || 1;
        this.difficulty = this.params.difficulty || 'beginner';
        
        // Generate level config with AI complexity
        this.config = this.generateLevelConfig();
        
        // Game state
        this.score = 0;
        this.streak = 0;
        this.correctPredictions = 0;
        this.totalRaces = 0;
        this.currentRace = 0;
        this.selectedPrediction = null;
        this.raceInProgress = false;
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'algorithm-race',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner'
        };
    }
    
    /**
     * Algorithm definitions with realistic time complexities
     */
    getAlgorithms() {
        return {
            // Sorting Algorithms
            bubble_sort: {
                name: "Bubble Sort",
                emoji: "🫧",
                category: "sorting",
                best: "O(n)",
                average: "O(n²)",
                worst: "O(n²)",
                space: "O(1)",
                speed: (n) => n * n * 0.5,  // Slow quadratic
                description: "Repeatedly swaps adjacent elements"
            },
            selection_sort: {
                name: "Selection Sort",
                emoji: "👆",
                category: "sorting",
                best: "O(n²)",
                average: "O(n²)",
                worst: "O(n²)",
                space: "O(1)",
                speed: (n) => n * n * 0.6,
                description: "Finds minimum and places at beginning"
            },
            insertion_sort: {
                name: "Insertion Sort",
                emoji: "📥",
                category: "sorting",
                best: "O(n)",
                average: "O(n²)",
                worst: "O(n²)",
                space: "O(1)",
                speed: (n) => n * n * 0.4,
                description: "Builds sorted array one element at a time"
            },
            merge_sort: {
                name: "Merge Sort",
                emoji: "🔀",
                category: "sorting",
                best: "O(n log n)",
                average: "O(n log n)",
                worst: "O(n log n)",
                space: "O(n)",
                speed: (n) => n * Math.log2(n) * 0.1,
                description: "Divides array and merges sorted halves"
            },
            quick_sort: {
                name: "Quick Sort",
                emoji: "⚡",
                category: "sorting",
                best: "O(n log n)",
                average: "O(n log n)",
                worst: "O(n²)",
                space: "O(log n)",
                speed: (n) => n * Math.log2(n) * 0.08,
                description: "Partitions around a pivot element"
            },
            heap_sort: {
                name: "Heap Sort",
                emoji: "🏔️",
                category: "sorting",
                best: "O(n log n)",
                average: "O(n log n)",
                worst: "O(n log n)",
                space: "O(1)",
                speed: (n) => n * Math.log2(n) * 0.12,
                description: "Uses heap data structure to sort"
            },
            // Search Algorithms
            linear_search: {
                name: "Linear Search",
                emoji: "➡️",
                category: "search",
                best: "O(1)",
                average: "O(n)",
                worst: "O(n)",
                space: "O(1)",
                speed: (n) => n * 0.5,
                description: "Checks elements one by one"
            },
            binary_search: {
                name: "Binary Search",
                emoji: "✂️",
                category: "search",
                best: "O(1)",
                average: "O(log n)",
                worst: "O(log n)",
                space: "O(1)",
                speed: (n) => Math.log2(n) * 2,
                description: "Divides search space in half"
            },
            // Graph Algorithms
            bfs: {
                name: "BFS",
                emoji: "🌊",
                category: "graph",
                best: "O(V+E)",
                average: "O(V+E)",
                worst: "O(V+E)",
                space: "O(V)",
                speed: (n) => n * 1.5,
                description: "Explores level by level"
            },
            dfs: {
                name: "DFS",
                emoji: "🔍",
                category: "graph",
                best: "O(V+E)",
                average: "O(V+E)",
                worst: "O(V+E)",
                space: "O(V)",
                speed: (n) => n * 1.4,
                description: "Explores as deep as possible first"
            },
            dijkstra: {
                name: "Dijkstra",
                emoji: "🗺️",
                category: "graph",
                best: "O(E log V)",
                average: "O(E log V)",
                worst: "O(E log V)",
                space: "O(V)",
                speed: (n) => n * Math.log2(n) * 0.3,
                description: "Finds shortest path with weights"
            }
        };
    }
    
    /**
     * AI-driven level configuration
     * Complexity increases with each level
     */
    generateLevelConfig() {
        const level = this.level;
        const difficultyMultiplier = {
            'beginner': 1,
            'intermediate': 1.5,
            'advanced': 2,
            'expert': 2.5
        }[this.difficulty] || 1;
        
        const complexity = Math.floor(level * difficultyMultiplier);
        
        // Number of algorithms racing
        const algoCount = Math.min(2 + Math.floor(complexity / 2), 5);
        
        // Data size increases
        const dataSize = 50 + complexity * 25;
        
        // Number of races per level
        const racesPerLevel = Math.min(3 + Math.floor(complexity / 3), 7);
        
        // Categories available based on complexity
        let categories = ['sorting'];
        if (complexity >= 3) categories.push('search');
        if (complexity >= 5) categories.push('graph');
        
        // Mixed categories at higher levels
        const mixCategories = complexity >= 4;
        
        return {
            algoCount,
            dataSize,
            racesPerLevel,
            categories,
            mixCategories,
            complexity,
            showComplexity: complexity >= 2,
            showExplanation: true,
            objectives: this.generateObjectives(complexity)
        };
    }
    
    generateObjectives(complexity) {
        const objectives = ['Predict the fastest algorithm'];
        
        if (complexity >= 2) {
            objectives.push('Understand time complexity');
        }
        if (complexity >= 4) {
            objectives.push('Compare different categories');
        }
        if (complexity >= 6) {
            objectives.push('Achieve 80% accuracy');
        }
        
        return objectives;
    }
    
    init() {
        this.totalRaces = this.config.racesPerLevel;
        this.setupEventListeners();
        this.updateMissionDisplay();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('nextRaceBtn').addEventListener('click', () => this.setupNextRace());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
    }
    
    updateMissionDisplay() {
        document.getElementById('algoCountDisplay').textContent = this.config.algoCount;
        document.getElementById('dataSizeDisplay').textContent = this.config.dataSize;
        document.getElementById('categoryDisplay').textContent = 
            this.config.categories.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(', ');
        
        const objectivesList = document.getElementById('objectivesList');
        objectivesList.innerHTML = this.config.objectives.map(obj => 
            `<li>${obj}</li>`
        ).join('');
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        this.setupNextRace();
    }
    
    setupNextRace() {
        this.currentRace++;
        this.selectedPrediction = null;
        this.raceInProgress = false;
        
        if (this.currentRace > this.totalRaces) {
            this.showFinalResult();
            return;
        }
        
        // Select algorithms for this race
        this.raceAlgorithms = this.selectAlgorithms();
        
        // Reset UI
        document.getElementById('predictionSection').classList.remove('hidden');
        document.getElementById('raceProgress').classList.add('hidden');
        document.getElementById('raceResult').classList.add('hidden');
        document.getElementById('algoInfoSection').classList.add('hidden');
        
        document.getElementById('arraySize').textContent = this.config.dataSize;
        
        this.renderRaceTrack();
        this.renderPredictionButtons();
        
        if (this.config.showComplexity) {
            this.renderAlgoInfo();
        }
        
        this.updateDisplay();
    }
    
    selectAlgorithms() {
        const allAlgos = this.getAlgorithms();
        const available = [];
        
        // Filter by available categories
        for (const [id, algo] of Object.entries(allAlgos)) {
            if (this.config.categories.includes(algo.category)) {
                available.push({ id, ...algo });
            }
        }
        
        // Shuffle and select
        const shuffled = available.sort(() => Math.random() - 0.5);
        return shuffled.slice(0, this.config.algoCount);
    }
    
    renderRaceTrack() {
        const track = document.getElementById('raceTrack');
        track.innerHTML = this.raceAlgorithms.map((algo, index) => {
            const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6'];
            const color = colors[index % colors.length];
            
            return `
                <div class="race-lane" data-algo="${algo.id}">
                    <div class="lane-info">
                        <span class="algo-name">${algo.emoji} ${algo.name}</span>
                        <span class="algo-complexity">${algo.average}</span>
                    </div>
                    <div class="lane-track">
                        <div class="racer" id="racer-${algo.id}" style="left: 0%;">${algo.emoji}</div>
                        <div class="finish-line"></div>
                        <span class="finish-flag">🏁</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    renderPredictionButtons() {
        const container = document.getElementById('predictionButtons');
        container.innerHTML = this.raceAlgorithms.map(algo => `
            <button class="prediction-btn" data-algo="${algo.id}" onclick="game.selectPrediction('${algo.id}')">
                ${algo.emoji} ${algo.name}
            </button>
        `).join('');
    }
    
    renderAlgoInfo() {
        document.getElementById('algoInfoSection').classList.remove('hidden');
        
        const container = document.getElementById('algoCards');
        container.innerHTML = this.raceAlgorithms.map(algo => `
            <div class="algo-card">
                <h4>${algo.emoji} ${algo.name}</h4>
                <div class="complexity">
                    <span class="label">Best:</span>
                    <span class="value">${algo.best}</span>
                </div>
                <div class="complexity">
                    <span class="label">Average:</span>
                    <span class="value">${algo.average}</span>
                </div>
                <div class="complexity">
                    <span class="label">Worst:</span>
                    <span class="value">${algo.worst}</span>
                </div>
            </div>
        `).join('');
    }
    
    selectPrediction(algoId) {
        this.selectedPrediction = algoId;
        
        // Update button styles
        document.querySelectorAll('.prediction-btn').forEach(btn => {
            btn.classList.remove('selected');
            if (btn.dataset.algo === algoId) {
                btn.classList.add('selected');
            }
        });
        
        // Start race after selection
        setTimeout(() => this.startRace(), 500);
    }
    
    startRace() {
        if (this.raceInProgress) return;
        this.raceInProgress = true;
        
        document.getElementById('predictionSection').classList.add('hidden');
        document.getElementById('algoInfoSection').classList.add('hidden');
        document.getElementById('raceProgress').classList.remove('hidden');
        
        const n = this.config.dataSize;
        const raceData = this.raceAlgorithms.map(algo => ({
            id: algo.id,
            name: algo.name,
            emoji: algo.emoji,
            totalTime: algo.speed(n),
            currentProgress: 0,
            finished: false,
            finishTime: 0
        }));
        
        // Normalize times so race takes about 3-4 seconds
        const maxTime = Math.max(...raceData.map(r => r.totalTime));
        const scaleFactor = 3000 / maxTime;
        
        raceData.forEach(r => {
            r.totalTime *= scaleFactor;
            // Add some randomness
            r.totalTime *= (0.9 + Math.random() * 0.2);
        });
        
        this.renderProgressBars(raceData);
        this.animateRace(raceData);
    }
    
    renderProgressBars(raceData) {
        const container = document.getElementById('progressBars');
        const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6'];
        
        container.innerHTML = raceData.map((r, i) => `
            <div class="progress-bar">
                <span class="name">${r.emoji} ${r.name}</span>
                <div class="bar">
                    <div class="fill" id="fill-${r.id}" style="width: 0%; background: ${colors[i % colors.length]};"></div>
                </div>
                <span class="time" id="time-${r.id}">0ms</span>
            </div>
        `).join('');
    }
    
    animateRace(raceData) {
        const startTime = Date.now();
        let finishedCount = 0;
        const finishOrder = [];
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            
            raceData.forEach(racer => {
                if (racer.finished) return;
                
                const progress = Math.min(100, (elapsed / racer.totalTime) * 100);
                racer.currentProgress = progress;
                
                // Update progress bar
                const fill = document.getElementById(`fill-${racer.id}`);
                if (fill) fill.style.width = `${progress}%`;
                
                // Update time display
                const timeEl = document.getElementById(`time-${racer.id}`);
                if (timeEl) timeEl.textContent = `${Math.floor(elapsed)}ms`;
                
                // Update race track
                const racerEl = document.getElementById(`racer-${racer.id}`);
                if (racerEl) racerEl.style.left = `${progress * 0.9}%`;
                
                // Check finish
                if (progress >= 100) {
                    racer.finished = true;
                    racer.finishTime = elapsed;
                    finishedCount++;
                    finishOrder.push(racer);
                }
            });
            
            if (finishedCount < raceData.length) {
                requestAnimationFrame(animate);
            } else {
                this.showRaceResult(finishOrder);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    showRaceResult(finishOrder) {
        document.getElementById('raceProgress').classList.add('hidden');
        document.getElementById('raceResult').classList.remove('hidden');
        
        const winner = finishOrder[0];
        const winnerAlgo = this.raceAlgorithms.find(a => a.id === winner.id);
        
        const correct = this.selectedPrediction === winner.id;
        
        if (correct) {
            this.correctPredictions++;
            this.streak++;
            this.score += 10 + this.streak * 5;
        } else {
            this.streak = 0;
        }
        
        const resultsHTML = finishOrder.map((r, i) => {
            const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}`;
            return `${medal} ${r.emoji} ${r.name} - ${Math.floor(r.finishTime)}ms`;
        }).join('<br>');
        
        const predictionResult = correct
            ? `<div class="your-pick correct">✅ Correct! You predicted ${winner.emoji} ${winner.name}</div>`
            : `<div class="your-pick incorrect">❌ Wrong! You picked ${this.raceAlgorithms.find(a => a.id === this.selectedPrediction)?.name || 'nothing'}</div>`;
        
        const explanation = `
            <p class="explanation">
                <strong>Why ${winner.name} won:</strong><br>
                ${winnerAlgo.description}.<br>
                With ${this.config.dataSize} elements, its ${winnerAlgo.average} complexity made it fastest.
            </p>
        `;
        
        document.getElementById('resultDetails').innerHTML = `
            <div class="winner">🏆 ${winner.emoji} ${winner.name} wins!</div>
            ${resultsHTML}
            ${predictionResult}
            ${this.config.showExplanation ? explanation : ''}
        `;
        
        document.getElementById('nextRaceBtn').textContent = 
            this.currentRace >= this.totalRaces ? 'See Results' : 'Next Race →';
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('scoreDisplay').textContent = this.score;
        document.getElementById('streakDisplay').textContent = this.streak;
    }
    
    showFinalResult() {
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        const accuracy = Math.round((this.correctPredictions / this.totalRaces) * 100);
        const xpEarned = 50 + this.score + (accuracy >= 80 ? 50 : 0);
        
        const success = accuracy >= 50;
        
        document.getElementById('resultIcon').textContent = success ? '🏆' : '🏁';
        document.getElementById('resultTitle').textContent = success ? 'Race Champion!' : 'Keep Practicing!';
        document.getElementById('resultText').textContent = 
            `${accuracy}% accuracy - ${this.correctPredictions}/${this.totalRaces} predictions correct`;
        document.getElementById('resultCorrect').textContent = `${this.correctPredictions}/${this.totalRaces}`;
        document.getElementById('resultScore').textContent = this.score;
        document.getElementById('resultXP').textContent = `+${xpEarned}`;
        
        if (success) {
            this.reportProgress(xpEarned);
        }
    }
    
    async reportProgress(xpEarned) {
        try {
            if (typeof GameAPI !== 'undefined') {
                const api = new GameAPI();
                await api.updateProgress({
                    username: this.params.username,
                    game_id: 'algorithm-race',
                    level_id: this.level,
                    xp_earned: xpEarned,
                    score: this.score,
                    completed: true
                });
            }
        } catch (e) {
            console.log('Progress sync failed:', e);
        }
    }
    
    nextLevel() {
        this.level++;
        this.config = this.generateLevelConfig();
        this.resetState();
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.updateMissionDisplay();
    }
    
    retryLevel() {
        this.resetState();
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
    }
    
    resetState() {
        this.score = 0;
        this.streak = 0;
        this.correctPredictions = 0;
        this.totalRaces = this.config.racesPerLevel;
        this.currentRace = 0;
        this.selectedPrediction = null;
        this.raceInProgress = false;
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new AlgorithmRace();
});
