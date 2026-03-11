// Array Sorter Game Logic
class ArraySorterGame {
    constructor() {
        this.currentArray = [];
        this.originalArray = [];
        this.selectedIndex = null;
        this.moves = 0;
        this.score = 0;
        this.level = 1;
        
        // Get parameters from window.GAME_PARAMS (injected by Streamlit) or URL
        const params = window.GAME_PARAMS || this.getURLParams();
        this.username = params.username || 'guest';
        this.gameId = params.gameId || 'dsa';
        this.levelId = parseInt(params.levelId) || 1;
        this.difficulty = params.difficulty || 'intermediate';
        
        this.apiClient = typeof GameAPI !== 'undefined' ? new GameAPI() : null;
        
        this.initializeGame();
    }
    
    getURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        return {
            username: urlParams.get('username'),
            gameId: urlParams.get('gameId'),
            levelId: urlParams.get('levelId'),
            difficulty: urlParams.get('difficulty')
        };
    }
    
    initializeGame() {
        // Generate array based on level
        this.generateArray();
        
        // Setup event listeners
        document.getElementById('submitBtn').addEventListener('click', () => this.checkSolution());
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetArray());
        document.getElementById('continueBtn').addEventListener('click', () => this.continueToNext());
        
        // Update UI
        this.updateDisplay();
        this.renderArray();
    }
    
    generateArray() {
        // Generate array based on level difficulty
        const sizes = {
            beginner: 5,
            intermediate: 7,
            advanced: 9,
            expert: 12
        };
        
        const size = sizes[this.difficulty.toLowerCase()] || 7;
        
        // Create sorted array
        this.currentArray = [];
        for (let i = 1; i <= size; i++) {
            this.currentArray.push(i);
        }
        
        // Shuffle array (Fisher-Yates shuffle)
        for (let i = this.currentArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.currentArray[i], this.currentArray[j]] = [this.currentArray[j], this.currentArray[i]];
        }
        
        // Store original for reset
        this.originalArray = [...this.currentArray];
        
        // Ensure it's not already sorted
        while (this.isSorted()) {
            for (let i = this.currentArray.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [this.currentArray[i], this.currentArray[j]] = [this.currentArray[j], this.currentArray[i]];
            }
        }
        
        this.moves = 0;
        this.selectedIndex = null;
    }
    
    renderArray() {
        const container = document.getElementById('arrayContainer');
        container.innerHTML = '';
        
        this.currentArray.forEach((value, index) => {
            const element = document.createElement('div');
            element.className = 'array-element';
            element.textContent = value;
            element.dataset.index = index;
            
            element.addEventListener('click', () => this.selectElement(index));
            
            container.appendChild(element);
        });
    }
    
    selectElement(index) {
        if (this.selectedIndex === null) {
            // First selection
            this.selectedIndex = index;
            this.highlightSelected(index);
        } else if (this.selectedIndex === index) {
            // Deselect same element
            this.selectedIndex = null;
            this.clearHighlights();
        } else {
            // Second selection - swap
            this.swapElements(this.selectedIndex, index);
            this.selectedIndex = null;
            this.clearHighlights();
            this.moves++;
            this.updateDisplay();
        }
    }
    
    highlightSelected(index) {
        const elements = document.querySelectorAll('.array-element');
        elements.forEach((el, i) => {
            if (i === index) {
                el.classList.add('selected');
            } else {
                el.classList.remove('selected');
            }
        });
    }
    
    clearHighlights() {
        const elements = document.querySelectorAll('.array-element');
        elements.forEach(el => el.classList.remove('selected'));
    }
    
    swapElements(i, j) {
        [this.currentArray[i], this.currentArray[j]] = [this.currentArray[j], this.currentArray[i]];
        this.renderArray();
    }
    
    isSorted() {
        for (let i = 0; i < this.currentArray.length - 1; i++) {
            if (this.currentArray[i] > this.currentArray[i + 1]) {
                return false;
            }
        }
        return true;
    }
    
    checkSolution() {
        if (this.isSorted()) {
            this.levelComplete();
        } else {
            this.showMessage('❌ Not quite right! Keep sorting...', 'error');
        }
    }
    
    showHint() {
        // Find first out-of-place element
        for (let i = 0; i < this.currentArray.length - 1; i++) {
            if (this.currentArray[i] > this.currentArray[i + 1]) {
                this.showMessage(`💡 Try swapping ${this.currentArray[i]} with a smaller number`, 'hint');
                
                // Highlight the problem element
                const elements = document.querySelectorAll('.array-element');
                elements[i].style.border = '3px solid #ffd700';
                setTimeout(() => {
                    elements[i].style.border = '';
                }, 2000);
                
                return;
            }
        }
    }
    
    resetArray() {
        this.currentArray = [...this.originalArray];
        this.moves = 0;
        this.selectedIndex = null;
        this.clearHighlights();
        this.renderArray();
        this.updateDisplay();
        this.showMessage('↻ Array reset!', 'info');
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('movesDisplay').textContent = this.moves;
        document.getElementById('scoreDisplay').textContent = this.score;
        document.getElementById('difficultyBadge').textContent = this.difficulty.toUpperCase();
    }
    
    showMessage(message, type) {
        const missionText = document.getElementById('missionText');
        const originalText = missionText.textContent;
        
        missionText.textContent = message;
        missionText.style.color = type === 'error' ? '#e74c3c' : type === 'hint' ? '#ffd700' : '#9b59b6';
        
        setTimeout(() => {
            missionText.textContent = originalText;
            missionText.style.color = '';
        }, 3000);
    }
    
    levelComplete() {
        // Calculate score (fewer moves = higher score)
        const baseXP = 100;
        const movesPenalty = Math.max(0, this.moves - this.currentArray.length);
        const earnedXP = Math.max(50, baseXP - (movesPenalty * 5));
        
        this.score += earnedXP;
        
        // Show all elements as correct
        const elements = document.querySelectorAll('.array-element');
        elements.forEach(el => el.classList.add('correct'));
        
        // Show result panel
        setTimeout(() => {
            this.showResultPanel(earnedXP);
            this.saveProgress(earnedXP);
        }, 1000);
    }
    
    showResultPanel(xp) {
        document.getElementById('resultIcon').textContent = '✓';
        document.getElementById('resultTitle').textContent = 'LEVEL COMPLETE!';
        document.getElementById('resultMoves').textContent = this.moves;
        document.getElementById('resultXP').textContent = `+${xp}`;
        document.getElementById('resultPanel').classList.remove('hidden');
    }
    
    async saveProgress(xp) {
        if (!this.apiClient) {
            console.log('API client not available');
            return;
        }
        
        try {
            await this.apiClient.updateProgress(this.username, {
                gameId: this.gameId,
                levelId: this.levelId,
                score: this.score,
                xpEarned: xp,
                completed: true,
                metadata: {
                    moves: this.moves,
                    difficulty: this.difficulty
                }
            });
            console.log('Progress saved successfully');
        } catch (error) {
            console.error('Failed to save progress:', error);
        }
    }
    
    continueToNext() {
        this.level++;
        this.generateArray();
        this.renderArray();
        this.updateDisplay();
        document.getElementById('resultPanel').classList.add('hidden');
        
        // Clear correct highlighting
        const elements = document.querySelectorAll('.array-element');
        elements.forEach(el => el.classList.remove('correct'));
    }
}

// Initialize game when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.game = new ArraySorterGame();
    });
} else {
    window.game = new ArraySorterGame();
}
