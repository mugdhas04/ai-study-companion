class SortingArena {
    constructor() {
        // Get game parameters
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        // Game state
        this.currentMode = null;
        this.arraySize = 8;
        this.originalArray = [];
        this.currentArray = [];
        this.swaps = 0;
        this.selectedIndices = [];
        this.optimalSwaps = 0;
        this.score = 0;
        
        // Mode descriptions
        this.modeInfo = {
            bubble: {
                name: "Bubble Sort",
                icon: "🫧",
                hint: "Compare adjacent elements and swap if they're in wrong order. Repeat until sorted.",
                complexity: "O(n²)"
            },
            insertion: {
                name: "Insertion Sort",
                icon: "➡️",
                hint: "Take each element and insert it into its correct position in the sorted portion.",
                complexity: "O(n²)"
            },
            selection: {
                name: "Selection Sort",
                icon: "🎯",
                hint: "Find the minimum element and place it at the beginning. Repeat for remaining array.",
                complexity: "O(n²)"
            },
            quick: {
                name: "Quick Sort",
                icon: "⚡",
                hint: "Choose a pivot, partition array around it, then recursively sort subarrays.",
                complexity: "O(n log n)"
            }
        };
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'sorting-arena',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner'
        };
    }
    
    init() {
        this.setupEventListeners();
        this.showModeSelection();
    }
    
    setupEventListeners() {
        // Mode selection
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const mode = btn.dataset.mode;
                this.selectMode(mode);
            });
        });
        
        // Control buttons
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('compareBtn').addEventListener('click', () => this.showComparison());
        document.getElementById('submitBtn').addEventListener('click', () => this.submitSolution());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetArray());
        document.getElementById('changeModeBtn').addEventListener('click', () => this.showModeSelection());
        
        // Result buttons
        document.getElementById('nextLevelBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('changeModeResultBtn').addEventListener('click', () => this.showModeSelection());
        
        // Race button
        document.getElementById('startRaceBtn').addEventListener('click', () => this.startRace());
    }
    
    showModeSelection() {
        // Hide all panels
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('arrayContainer').classList.add('hidden');
        document.getElementById('controlsPanel').classList.add('hidden');
        document.getElementById('comparisonPanel').classList.add('hidden');
        document.getElementById('resultPanel').classList.add('hidden');
        
        // Show mode panel
        document.getElementById('modePanel').classList.remove('hidden');
        
        // Reset state
        this.currentMode = null;
        this.swaps = 0;
        this.selectedIndices = [];
    }
    
    selectMode(mode) {
        this.currentMode = mode;
        const modeData = this.modeInfo[mode];
        
        // Update display
        document.getElementById('modeDisplay').textContent = modeData.name;
        document.getElementById('swapsDisplay').textContent = '0';
        document.getElementById('scoreDisplay').textContent = '0';
        
        // Hide mode panel
        document.getElementById('modePanel').classList.add('hidden');
        
        // Show mission panel
        const missionPanel = document.getElementById('missionPanel');
        missionPanel.classList.remove('hidden');
        document.getElementById('missionText').textContent = 
            `Sort the array using ${modeData.name}!`;
        document.getElementById('algorithmHint').innerHTML = 
            `<strong>${modeData.icon} ${modeData.name}</strong><br>${modeData.hint}<br><em>Time Complexity: ${modeData.complexity}</em>`;
        
        // Generate and display array
        this.generateArray();
        this.calculateOptimalSwaps();
        this.displayArray();
        this.updateStats();
        
        // Show array and controls
        document.getElementById('arrayContainer').classList.remove('hidden');
        document.getElementById('controlsPanel').classList.remove('hidden');
    }
    
    generateArray() {
        // Generate random unsorted array
        this.arraySize = 6 + Math.floor(Math.random() * 5); // 6-10 elements
        const numbers = Array.from({length: this.arraySize}, (_, i) => i + 1);
        
        // Fisher-Yates shuffle
        for (let i = numbers.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [numbers[i], numbers[j]] = [numbers[j], numbers[i]];
        }
        
        this.originalArray = [...numbers];
        this.currentArray = [...numbers];
        this.swaps = 0;
        this.selectedIndices = [];
    }
    
    calculateOptimalSwaps() {
        // Calculate minimum swaps needed (using bubble sort as baseline)
        let tempArray = [...this.originalArray];
        let swapCount = 0;
        
        for (let i = 0; i < tempArray.length - 1; i++) {
            for (let j = 0; j < tempArray.length - i - 1; j++) {
                if (tempArray[j] > tempArray[j + 1]) {
                    [tempArray[j], tempArray[j + 1]] = [tempArray[j + 1], tempArray[j]];
                    swapCount++;
                }
            }
        }
        
        this.optimalSwaps = swapCount;
        document.getElementById('optimalSwaps').textContent = swapCount;
    }
    
    displayArray() {
        const container = document.getElementById('arrayContainer');
        container.innerHTML = '';
        
        const maxValue = Math.max(...this.currentArray);
        const minHeight = 60;
        const maxHeight = 200;
        
        this.currentArray.forEach((value, index) => {
            const element = document.createElement('div');
            element.className = 'array-element';
            element.dataset.index = index;
            
            // Calculate bar height
            const height = minHeight + (value / maxValue) * (maxHeight - minHeight);
            
            const bar = document.createElement('div');
            bar.className = 'array-bar';
            bar.style.height = `${height}px`;
            bar.textContent = value;
            
            const indexLabel = document.createElement('div');
            indexLabel.className = 'array-index';
            indexLabel.textContent = `[${index}]`;
            
            element.appendChild(bar);
            element.appendChild(indexLabel);
            
            // Add click handler
            element.addEventListener('click', () => this.selectElement(index));
            
            container.appendChild(element);
        });
    }
    
    selectElement(index) {
        // Toggle selection
        if (this.selectedIndices.includes(index)) {
            this.selectedIndices = this.selectedIndices.filter(i => i !== index);
        } else {
            this.selectedIndices.push(index);
        }
        
        // Limit to 2 selections for swap
        if (this.selectedIndices.length > 2) {
            this.selectedIndices.shift();
        }
        
        // Update visual selection
        document.querySelectorAll('.array-element').forEach((el, i) => {
            if (this.selectedIndices.includes(i)) {
                el.classList.add('selected');
            } else {
                el.classList.remove('selected');
            }
        });
        
        // Auto-swap when 2 elements selected
        if (this.selectedIndices.length === 2) {
            setTimeout(() => this.swapElements(), 300);
        }
    }
    
    swapElements() {
        if (this.selectedIndices.length !== 2) return;
        
        const [i, j] = this.selectedIndices;
        
        // Swap in array
        [this.currentArray[i], this.currentArray[j]] = 
            [this.currentArray[j], this.currentArray[i]];
        
        // Increment swap count
        this.swaps++;
        
        // Clear selection
        this.selectedIndices = [];
        
        // Update display
        this.displayArray();
        this.updateStats();
    }
    
    updateStats() {
        document.getElementById('swapsDisplay').textContent = this.swaps;
        document.getElementById('currentSwaps').textContent = this.swaps;
        
        // Calculate efficiency
        const efficiency = this.optimalSwaps === 0 ? 100 : 
            Math.max(0, Math.min(100, Math.round((this.optimalSwaps / Math.max(this.swaps, 1)) * 100)));
        document.getElementById('efficiency').textContent = `${efficiency}%`;
        
        // Calculate score
        this.score = Math.max(0, 100 - (this.swaps - this.optimalSwaps) * 5);
        document.getElementById('scoreDisplay').textContent = this.score;
    }
    
    showHint() {
        // Find first pair that needs swapping
        for (let i = 0; i < this.currentArray.length - 1; i++) {
            if (this.currentArray[i] > this.currentArray[i + 1]) {
                // Highlight these elements
                this.selectedIndices = [i, i + 1];
                document.querySelectorAll('.array-element').forEach((el, idx) => {
                    if (this.selectedIndices.includes(idx)) {
                        el.classList.add('selected');
                    } else {
                        el.classList.remove('selected');
                    }
                });
                
                // Show hint message
                const hint = document.createElement('div');
                hint.textContent = `💡 Swap elements at positions ${i} and ${i + 1}`;
                hint.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(243, 156, 18, 0.95);
                    color: white;
                    padding: 20px 40px;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    z-index: 999;
                    animation: fadeIn 0.3s ease-out;
                `;
                document.body.appendChild(hint);
                setTimeout(() => hint.remove(), 2000);
                
                return;
            }
        }
        
        // If array is sorted
        alert('Array is already sorted! Click SUBMIT to complete the level.');
    }
    
    showComparison() {
        // Hide game elements
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('arrayContainer').classList.add('hidden');
        document.getElementById('controlsPanel').classList.add('hidden');
        
        // Show comparison panel
        document.getElementById('comparisonPanel').classList.remove('hidden');
        
        // Reset race bars
        document.querySelectorAll('.race-bar').forEach(bar => {
            bar.classList.remove('racing');
        });
        document.querySelectorAll('.race-time').forEach(time => {
            time.textContent = '-';
        });
    }
    
    startRace() {
        const arraySize = this.currentArray.length;
        
        // Simulate algorithm times based on complexity
        const bubbleTime = arraySize * arraySize * 2; // O(n²)
        const quickTime = arraySize * Math.log2(arraySize) * 15; // O(n log n)
        const mergeTime = arraySize * Math.log2(arraySize) * 18; // O(n log n)
        
        // Normalize times
        const maxTime = Math.max(bubbleTime, quickTime, mergeTime);
        
        // Animate bars
        setTimeout(() => {
            const quickBar = document.getElementById('quickBar');
            quickBar.classList.add('racing');
            quickBar.style.animationDuration = `${(quickTime / maxTime) * 3}s`;
            document.getElementById('quickTime').textContent = `${quickTime.toFixed(0)}ms`;
        }, 100);
        
        setTimeout(() => {
            const mergeBar = document.getElementById('mergeBar');
            mergeBar.classList.add('racing');
            mergeBar.style.animationDuration = `${(mergeTime / maxTime) * 3}s`;
            document.getElementById('mergeTime').textContent = `${mergeTime.toFixed(0)}ms`;
        }, 300);
        
        setTimeout(() => {
            const bubbleBar = document.getElementById('bubbleBar');
            bubbleBar.classList.add('racing');
            bubbleBar.style.animationDuration = `${(bubbleTime / maxTime) * 3}s`;
            document.getElementById('bubbleTime').textContent = `${bubbleTime.toFixed(0)}ms`;
        }, 500);
        
        // Show return option after race
        setTimeout(() => {
            const returnBtn = document.createElement('button');
            returnBtn.className = 'control-btn secondary';
            returnBtn.textContent = '← RETURN TO SORTING';
            returnBtn.onclick = () => this.returnToGame();
            document.getElementById('comparisonPanel').appendChild(returnBtn);
        }, 4000);
    }
    
    returnToGame() {
        document.getElementById('comparisonPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        document.getElementById('arrayContainer').classList.remove('hidden');
        document.getElementById('controlsPanel').classList.remove('hidden');
    }
    
    resetArray() {
        this.currentArray = [...this.originalArray];
        this.swaps = 0;
        this.selectedIndices = [];
        this.displayArray();
        this.updateStats();
    }
    
    isSorted() {
        for (let i = 0; i < this.currentArray.length - 1; i++) {
            if (this.currentArray[i] > this.currentArray[i + 1]) {
                return false;
            }
        }
        return true;
    }
    
    submitSolution() {
        if (!this.isSorted()) {
            // Show error
            const error = document.createElement('div');
            error.textContent = '❌ Array is not sorted yet!';
            error.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(231, 76, 60, 0.95);
                color: white;
                padding: 20px 40px;
                border-radius: 10px;
                font-size: 1.2rem;
                z-index: 999;
                animation: fadeIn 0.3s ease-out;
            `;
            document.body.appendChild(error);
            setTimeout(() => error.remove(), 2000);
            return;
        }
        
        // Calculate results
        const efficiency = this.optimalSwaps === 0 ? 100 : 
            Math.max(0, Math.min(100, Math.round((this.optimalSwaps / Math.max(this.swaps, 1)) * 100)));
        
        let xp = 30; // Base XP
        if (efficiency >= 100) {
            xp = 50; // Perfect
        } else if (efficiency >= 80) {
            xp = 40; // Great
        }
        
        // Show results
        this.showResults(efficiency, xp);
        
        // Save progress
        this.saveProgress(xp);
    }
    
    showResults(efficiency, xp) {
        const resultPanel = document.getElementById('resultPanel');
        
        // Set icon and title based on efficiency
        let icon = '⭐';
        let title = 'SORTED!';
        let message = 'You sorted the array!';
        
        if (efficiency >= 100) {
            icon = '🏆';
            title = 'PERFECT SORT!';
            message = 'You used the optimal number of swaps!';
        } else if (efficiency >= 80) {
            icon = '⭐';
            title = 'GREAT SORT!';
            message = 'Very efficient sorting!';
        } else if (efficiency >= 60) {
            icon = '👍';
            title = 'GOOD SORT!';
            message = 'You sorted the array successfully!';
        }
        
        document.getElementById('resultIcon').textContent = icon;
        document.getElementById('resultTitle').textContent = title;
        document.getElementById('resultMessage').textContent = message;
        document.getElementById('resultSwaps').textContent = this.swaps;
        document.getElementById('resultEfficiency').textContent = `${efficiency}%`;
        document.getElementById('resultXP').textContent = `+${xp}`;
        
        resultPanel.classList.remove('hidden');
    }
    
    nextLevel() {
        // Hide result panel
        document.getElementById('resultPanel').classList.add('hidden');
        
        // Generate new array for same mode
        this.generateArray();
        this.calculateOptimalSwaps();
        this.displayArray();
        this.updateStats();
        
        // Show game elements
        document.getElementById('missionPanel').classList.remove('hidden');
        document.getElementById('arrayContainer').classList.remove('hidden');
        document.getElementById('controlsPanel').classList.remove('hidden');
    }
    
    async saveProgress(xp) {
        try {
            const response = await fetch('http://localhost:8000/api/save-progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.params.username,
                    gameId: this.params.gameId,
                    levelId: this.params.levelId,
                    score: this.score,
                    xp: xp,
                    metadata: {
                        mode: this.currentMode,
                        swaps: this.swaps,
                        optimalSwaps: this.optimalSwaps,
                        arraySize: this.arraySize
                    }
                })
            });
            
            if (!response.ok) {
                console.error('Failed to save progress');
            }
        } catch (error) {
            console.error('Error saving progress:', error);
        }
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SortingArena();
});
