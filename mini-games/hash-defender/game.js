/**
 * Hash Defender Game
 * Learn hash tables by inserting keys and handling collisions
 * Complexity increases with each level via AI parameters
 */

class HashDefenderGame {
    constructor() {
        // Game parameters from AI or URL
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        // Level-based complexity scaling
        this.level = parseInt(this.params.levelId) || 1;
        this.difficulty = this.params.difficulty || 'beginner';
        
        // Generate level config based on AI complexity
        this.config = this.generateLevelConfig();
        
        // Game state
        this.tableSize = this.config.tableSize;
        this.hashTable = new Array(this.tableSize).fill(null);
        this.keys = [];
        this.currentKeyIndex = 0;
        this.score = 0;
        this.probes = 0;
        this.history = [];
        this.collisionMethod = this.config.collisionMethod;
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'hash-defender',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner'
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
        
        // Base complexity that scales with level
        const complexity = Math.floor(level * difficultyMultiplier);
        
        // Table size increases: 7 -> 11 -> 13 -> 17 -> 19 -> 23...
        const primeSizes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47];
        const sizeIndex = Math.min(Math.floor(complexity / 2), primeSizes.length - 1);
        const tableSize = primeSizes[sizeIndex];
        
        // Number of keys to insert (more keys = harder)
        const keyCount = Math.min(3 + Math.floor(complexity * 0.8), tableSize - 2);
        
        // Collision methods get more complex
        const methods = ['linear', 'linear', 'quadratic', 'quadratic', 'double'];
        const methodIndex = Math.min(Math.floor(complexity / 3), methods.length - 1);
        const collisionMethod = methods[methodIndex];
        
        // Generate keys that will cause collisions at higher levels
        const keys = this.generateKeys(keyCount, tableSize, complexity);
        
        // Time pressure at higher levels (optional future feature)
        const timeLimit = complexity > 5 ? Math.max(120 - complexity * 5, 30) : 0;
        
        return {
            tableSize,
            keyCount,
            keys,
            collisionMethod,
            timeLimit,
            complexity,
            // Bonus objectives for higher levels
            objectives: this.generateObjectives(complexity)
        };
    }
    
    /**
     * Generate keys with intentional collisions for learning
     */
    generateKeys(count, tableSize, complexity) {
        const keys = [];
        const usedHashes = new Set();
        
        // At higher complexity, generate more colliding keys
        const collisionProbability = Math.min(0.3 + complexity * 0.05, 0.7);
        
        for (let i = 0; i < count; i++) {
            let key;
            
            if (i > 0 && Math.random() < collisionProbability && usedHashes.size > 0) {
                // Generate a key that collides with existing
                const existingHash = Array.from(usedHashes)[Math.floor(Math.random() * usedHashes.size)];
                // Find a key that hashes to same slot
                key = existingHash + tableSize * (Math.floor(Math.random() * 3) + 1);
            } else {
                // Generate random key
                key = Math.floor(Math.random() * 100) + 1;
            }
            
            keys.push(key);
            usedHashes.add(key % tableSize);
        }
        
        return keys;
    }
    
    generateObjectives(complexity) {
        const objectives = ['Insert all keys correctly'];
        
        if (complexity >= 2) {
            objectives.push('Handle collisions properly');
        }
        if (complexity >= 4) {
            objectives.push('Minimize probe count');
        }
        if (complexity >= 6) {
            objectives.push('Complete within optimal probes');
        }
        
        return objectives;
    }
    
    init() {
        this.keys = [...this.config.keys];
        this.setupEventListeners();
        this.updateMissionDisplay();
        this.renderHashTable();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('undoBtn').addEventListener('click', () => this.undo());
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetGame());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
    }
    
    updateMissionDisplay() {
        document.getElementById('tableSizeDisplay').textContent = this.tableSize;
        document.getElementById('keysCountDisplay').textContent = this.keys.length;
        document.getElementById('methodDisplay').textContent = this.getMethodName();
        
        // Update objectives
        const objectivesList = document.getElementById('objectivesList');
        objectivesList.innerHTML = this.config.objectives.map(obj => 
            `<li>${obj}</li>`
        ).join('');
        
        // Update mission text based on complexity
        const missionText = document.getElementById('missionText');
        if (this.config.complexity >= 5) {
            missionText.textContent = `Advanced hash table challenge! Use ${this.getMethodName()} probing to handle collisions efficiently.`;
        } else if (this.config.complexity >= 3) {
            missionText.textContent = `Insert keys and handle collisions using ${this.getMethodName()} probing.`;
        }
    }
    
    getMethodName() {
        const names = {
            'linear': 'Linear Probing',
            'quadratic': 'Quadratic Probing',
            'double': 'Double Hashing'
        };
        return names[this.collisionMethod] || 'Linear Probing';
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        document.getElementById('modValue').textContent = this.tableSize;
        this.renderKeysQueue();
        this.renderHashTable();
        this.updateCurrentKey();
        this.updateDisplay();
    }
    
    renderKeysQueue() {
        const container = document.getElementById('keysQueue');
        container.innerHTML = this.keys.map((key, i) => `
            <div class="key-item ${i === this.currentKeyIndex ? 'current' : ''} ${i < this.currentKeyIndex ? 'inserted' : ''}" 
                 data-index="${i}">
                ${key}
            </div>
        `).join('');
    }
    
    renderHashTable() {
        const container = document.getElementById('hashTable');
        container.innerHTML = '';
        
        for (let i = 0; i < this.tableSize; i++) {
            const slot = document.createElement('div');
            slot.className = 'hash-slot';
            slot.dataset.index = i;
            
            if (this.hashTable[i] !== null) {
                slot.classList.add('occupied');
            }
            
            slot.innerHTML = `
                <span class="slot-index">[${i}]</span>
                <span class="slot-value">${this.hashTable[i] !== null ? this.hashTable[i] : '-'}</span>
            `;
            
            slot.addEventListener('click', () => this.onSlotClick(i));
            container.appendChild(slot);
        }
        
        // Highlight target slot for current key
        if (this.currentKeyIndex < this.keys.length) {
            const currentKey = this.keys[this.currentKeyIndex];
            const targetIndex = currentKey % this.tableSize;
            const targetSlot = container.children[targetIndex];
            if (targetSlot && !targetSlot.classList.contains('occupied')) {
                targetSlot.classList.add('target');
            }
        }
    }
    
    updateCurrentKey() {
        if (this.currentKeyIndex < this.keys.length) {
            const key = this.keys[this.currentKeyIndex];
            document.getElementById('currentKey').textContent = key;
            document.getElementById('hashValue').textContent = key % this.tableSize;
        } else {
            document.getElementById('currentKey').textContent = '-';
            document.getElementById('hashValue').textContent = '-';
        }
    }
    
    onSlotClick(slotIndex) {
        if (this.currentKeyIndex >= this.keys.length) return;
        
        const currentKey = this.keys[this.currentKeyIndex];
        const correctSlot = this.findCorrectSlot(currentKey);
        
        if (slotIndex === correctSlot) {
            // Correct placement
            this.saveState();
            this.hashTable[slotIndex] = currentKey;
            this.score += 10;
            
            // Bonus for first try (no probing needed)
            const idealSlot = currentKey % this.tableSize;
            if (slotIndex === idealSlot) {
                this.score += 5;
            }
            
            this.currentKeyIndex++;
            this.hideCollisionInfo();
            
            this.renderKeysQueue();
            this.renderHashTable();
            this.updateCurrentKey();
            this.updateDisplay();
            
            // Check win condition
            if (this.currentKeyIndex >= this.keys.length) {
                this.showResult(true);
            }
        } else if (this.hashTable[slotIndex] !== null) {
            // Clicked occupied slot
            this.showCollisionInfo('This slot is occupied! Find the next available slot using ' + this.getMethodName() + '.');
            this.probes++;
            this.updateDisplay();
        } else {
            // Wrong empty slot
            this.showCollisionInfo(`Wrong slot! The key ${currentKey} should go to slot ${correctSlot} using ${this.getMethodName()}.`);
            this.score = Math.max(0, this.score - 2);
            this.probes++;
            this.updateDisplay();
        }
    }
    
    findCorrectSlot(key) {
        const hash = key % this.tableSize;
        
        if (this.hashTable[hash] === null) {
            return hash;
        }
        
        // Handle collision based on method
        let probe = 1;
        while (probe < this.tableSize) {
            let newIndex;
            
            switch (this.collisionMethod) {
                case 'linear':
                    newIndex = (hash + probe) % this.tableSize;
                    break;
                case 'quadratic':
                    newIndex = (hash + probe * probe) % this.tableSize;
                    break;
                case 'double':
                    const hash2 = 7 - (key % 7); // Second hash function
                    newIndex = (hash + probe * hash2) % this.tableSize;
                    break;
                default:
                    newIndex = (hash + probe) % this.tableSize;
            }
            
            if (this.hashTable[newIndex] === null) {
                return newIndex;
            }
            probe++;
        }
        
        return -1; // Table full
    }
    
    showCollisionInfo(text) {
        const info = document.getElementById('collisionInfo');
        document.getElementById('collisionText').textContent = text;
        info.classList.remove('hidden');
    }
    
    hideCollisionInfo() {
        document.getElementById('collisionInfo').classList.add('hidden');
    }
    
    saveState() {
        this.history.push({
            hashTable: [...this.hashTable],
            currentKeyIndex: this.currentKeyIndex,
            score: this.score,
            probes: this.probes
        });
    }
    
    undo() {
        if (this.history.length === 0) return;
        
        const state = this.history.pop();
        this.hashTable = state.hashTable;
        this.currentKeyIndex = state.currentKeyIndex;
        this.score = state.score;
        this.probes = state.probes;
        
        this.renderKeysQueue();
        this.renderHashTable();
        this.updateCurrentKey();
        this.updateDisplay();
        this.hideCollisionInfo();
    }
    
    showHint() {
        if (this.currentKeyIndex >= this.keys.length) return;
        
        const currentKey = this.keys[this.currentKeyIndex];
        const correctSlot = this.findCorrectSlot(currentKey);
        const idealSlot = currentKey % this.tableSize;
        
        let hint = `Key ${currentKey} → h(${currentKey}) = ${currentKey} mod ${this.tableSize} = ${idealSlot}`;
        
        if (correctSlot !== idealSlot) {
            hint += `\nSlot ${idealSlot} is occupied, so using ${this.getMethodName()}: insert at slot ${correctSlot}`;
        }
        
        alert(`💡 Hint:\n${hint}`);
        this.score = Math.max(0, this.score - 5);
        this.updateDisplay();
    }
    
    resetGame() {
        this.hashTable = new Array(this.tableSize).fill(null);
        this.currentKeyIndex = 0;
        this.score = 0;
        this.probes = 0;
        this.history = [];
        
        this.renderKeysQueue();
        this.renderHashTable();
        this.updateCurrentKey();
        this.updateDisplay();
        this.hideCollisionInfo();
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('scoreDisplay').textContent = this.score;
        document.getElementById('probesDisplay').textContent = this.probes;
    }
    
    showResult(success) {
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        if (success) {
            // Calculate XP based on performance
            const optimalProbes = this.keys.length; // Minimum possible
            const probeBonus = Math.max(0, (optimalProbes * 2 - this.probes) * 5);
            const xpEarned = 50 + this.score + probeBonus;
            
            document.getElementById('resultIcon').textContent = '🎉';
            document.getElementById('resultTitle').textContent = 'Hash Table Complete!';
            document.getElementById('resultText').textContent = 
                `Level ${this.level} conquered! Complexity: ${this.config.complexity}`;
            document.getElementById('resultProbes').textContent = this.probes;
            document.getElementById('resultScore').textContent = this.score;
            document.getElementById('resultXP').textContent = `+${xpEarned}`;
            
            this.reportProgress(xpEarned);
        }
    }
    
    async reportProgress(xpEarned) {
        try {
            if (typeof GameAPI !== 'undefined') {
                const api = new GameAPI();
                await api.updateProgress({
                    username: this.params.username,
                    game_id: 'hash-defender',
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
        this.tableSize = this.config.tableSize;
        this.hashTable = new Array(this.tableSize).fill(null);
        this.keys = [...this.config.keys];
        this.currentKeyIndex = 0;
        this.score = 0;
        this.probes = 0;
        this.history = [];
        this.collisionMethod = this.config.collisionMethod;
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.updateMissionDisplay();
    }
    
    retryLevel() {
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        this.resetGame();
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new HashDefenderGame();
});
