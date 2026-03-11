/**
 * Link Builder Game
 * Build and manipulate linked lists
 */

class LinkBuilderGame {
    constructor() {
        // Game parameters
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        // Game state
        this.currentList = [];
        this.initialList = [];
        this.targetList = [];
        this.operations = 0;
        this.score = 0;
        this.level = parseInt(this.params.levelId) || 1;
        this.hints = 3;
        this.history = [];
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'link-builder',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner',
            initialList: params.get('initialList') ? JSON.parse(params.get('initialList')) : null,
            targetList: params.get('targetList') ? JSON.parse(params.get('targetList')) : null
        };
    }
    
    init() {
        this.setupEventListeners();
        this.generateLevel();
        this.updateDisplay();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('insertFrontBtn').addEventListener('click', () => this.insertFront());
        document.getElementById('insertEndBtn').addEventListener('click', () => this.insertEnd());
        document.getElementById('insertAtBtn').addEventListener('click', () => this.insertAt());
        document.getElementById('deleteAtBtn').addEventListener('click', () => this.deleteAt());
        document.getElementById('reverseBtn').addEventListener('click', () => this.reverseList());
        document.getElementById('undoBtn').addEventListener('click', () => this.undo());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetList());
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('submitBtn').addEventListener('click', () => this.checkSolution());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
    }
    
    generateLevel() {
        const difficulties = {
            beginner: { listSize: 3, targetOps: 2, maxVal: 20 },
            intermediate: { listSize: 4, targetOps: 4, maxVal: 50 },
            advanced: { listSize: 5, targetOps: 6, maxVal: 100 },
            expert: { listSize: 6, targetOps: 8, maxVal: 200 }
        };
        
        const config = difficulties[this.params.difficulty] || difficulties.beginner;
        
        // Use provided lists or generate
        if (this.params.initialList && this.params.targetList) {
            this.initialList = [...this.params.initialList];
            this.targetList = [...this.params.targetList];
        } else {
            // Generate initial list
            this.initialList = [];
            for (let i = 0; i < config.listSize; i++) {
                this.initialList.push(Math.floor(Math.random() * config.maxVal) + 1);
            }
            
            // Generate target by applying random operations
            this.targetList = [...this.initialList];
            for (let i = 0; i < config.targetOps; i++) {
                this.applyRandomOperation(this.targetList, config.maxVal);
            }
        }
        
        // Display initial and target in mission panel
        this.renderListVisual('initialListVisual', this.initialList);
        this.renderListVisual('targetListVisual', this.targetList);
        
        document.getElementById('missionText').textContent = 
            `Transform the starting list into the target list using linked list operations.`;
    }
    
    applyRandomOperation(list, maxVal) {
        const ops = ['insertFront', 'insertEnd', 'insertAt', 'deleteAt', 'reverse'];
        const op = ops[Math.floor(Math.random() * ops.length)];
        
        switch (op) {
            case 'insertFront':
                list.unshift(Math.floor(Math.random() * maxVal) + 1);
                break;
            case 'insertEnd':
                list.push(Math.floor(Math.random() * maxVal) + 1);
                break;
            case 'insertAt':
                if (list.length > 0) {
                    const pos = Math.floor(Math.random() * list.length);
                    list.splice(pos, 0, Math.floor(Math.random() * maxVal) + 1);
                }
                break;
            case 'deleteAt':
                if (list.length > 1) {
                    const pos = Math.floor(Math.random() * list.length);
                    list.splice(pos, 1);
                }
                break;
            case 'reverse':
                list.reverse();
                break;
        }
    }
    
    renderListVisual(containerId, list) {
        const container = document.getElementById(containerId);
        
        if (list.length === 0) {
            container.innerHTML = '<span class="null">NULL</span>';
            return;
        }
        
        container.innerHTML = list.map((val, i) => {
            const arrow = i < list.length - 1 ? '<span class="arrow">→</span>' : '';
            return `<span class="node">${val}</span>${arrow}`;
        }).join('') + '<span class="arrow">→</span><span class="null">NULL</span>';
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        // Initialize current list from initial
        this.currentList = [...this.initialList];
        this.operations = 0;
        this.history = [];
        
        this.renderCurrentList();
        this.renderTargetList();
    }
    
    renderCurrentList() {
        const container = document.getElementById('listNodes');
        
        if (this.currentList.length === 0) {
            container.innerHTML = '<span style="color: #666;">Empty List</span>';
            return;
        }
        
        container.innerHTML = this.currentList.map((val, i) => `
            <div class="list-node" data-index="${i}">
                <div class="node-box">
                    <span class="data">${val}</span>
                    <span class="next">•</span>
                </div>
                <span class="arrow">→</span>
            </div>
        `).join('');
    }
    
    renderTargetList() {
        const container = document.getElementById('targetNodes');
        
        if (this.targetList.length === 0) {
            container.innerHTML = '<span style="color: #666;">Empty List</span>';
            return;
        }
        
        container.innerHTML = this.targetList.map((val, i) => `
            <div class="list-node">
                <div class="node-box">
                    <span class="data">${val}</span>
                    <span class="next">•</span>
                </div>
                <span class="arrow">→</span>
            </div>
        `).join('');
    }
    
    saveState() {
        this.history.push([...this.currentList]);
    }
    
    insertFront() {
        const value = parseInt(document.getElementById('valueInput').value);
        
        if (isNaN(value)) {
            this.showError('Enter a value first!');
            return;
        }
        
        this.saveState();
        this.currentList.unshift(value);
        this.operations++;
        this.score += 5;
        
        this.renderCurrentList();
        this.highlightNode(0);
        this.updateDisplay();
        this.clearInputs();
    }
    
    insertEnd() {
        const value = parseInt(document.getElementById('valueInput').value);
        
        if (isNaN(value)) {
            this.showError('Enter a value first!');
            return;
        }
        
        this.saveState();
        this.currentList.push(value);
        this.operations++;
        this.score += 5;
        
        this.renderCurrentList();
        this.highlightNode(this.currentList.length - 1);
        this.updateDisplay();
        this.clearInputs();
    }
    
    insertAt() {
        const value = parseInt(document.getElementById('valueInput').value);
        const position = parseInt(document.getElementById('positionInput').value);
        
        if (isNaN(value)) {
            this.showError('Enter a value first!');
            return;
        }
        
        if (isNaN(position) || position < 0 || position > this.currentList.length) {
            this.showError(`Enter a valid position (0-${this.currentList.length})`);
            return;
        }
        
        this.saveState();
        this.currentList.splice(position, 0, value);
        this.operations++;
        this.score += 5;
        
        this.renderCurrentList();
        this.highlightNode(position);
        this.updateDisplay();
        this.clearInputs();
    }
    
    deleteAt() {
        const position = parseInt(document.getElementById('positionInput').value);
        
        if (this.currentList.length === 0) {
            this.showError('List is empty!');
            return;
        }
        
        if (isNaN(position) || position < 0 || position >= this.currentList.length) {
            this.showError(`Enter a valid position (0-${this.currentList.length - 1})`);
            return;
        }
        
        this.saveState();
        this.currentList.splice(position, 1);
        this.operations++;
        this.score += 5;
        
        this.renderCurrentList();
        this.updateDisplay();
        this.clearInputs();
    }
    
    reverseList() {
        if (this.currentList.length <= 1) {
            this.showError('Need at least 2 elements to reverse!');
            return;
        }
        
        this.saveState();
        this.currentList.reverse();
        this.operations++;
        this.score += 10;
        
        this.renderCurrentList();
        this.updateDisplay();
    }
    
    highlightNode(index) {
        const nodes = document.querySelectorAll('.list-node');
        if (nodes[index]) {
            nodes[index].classList.add('highlight');
            setTimeout(() => nodes[index].classList.remove('highlight'), 1000);
        }
    }
    
    clearInputs() {
        document.getElementById('valueInput').value = '';
        document.getElementById('positionInput').value = '';
    }
    
    undo() {
        if (this.history.length === 0) {
            this.showError('Nothing to undo!');
            return;
        }
        
        this.currentList = this.history.pop();
        this.operations = Math.max(0, this.operations - 1);
        this.score = Math.max(0, this.score - 5);
        
        this.renderCurrentList();
        this.updateDisplay();
    }
    
    resetList() {
        this.currentList = [...this.initialList];
        this.operations = 0;
        this.score = 0;
        this.history = [];
        
        this.renderCurrentList();
        this.updateDisplay();
    }
    
    showHint() {
        if (this.hints <= 0) {
            this.showError('No hints remaining!');
            return;
        }
        
        this.hints--;
        
        // Analyze differences and suggest an operation
        let hint = this.analyzeForHint();
        alert(`💡 Hint: ${hint}`);
        
        this.updateDisplay();
    }
    
    analyzeForHint() {
        // Simple hint generation
        if (this.currentList.length < this.targetList.length) {
            // Need to add elements
            const missingFirst = this.targetList[0];
            const missingLast = this.targetList[this.targetList.length - 1];
            
            if (this.currentList[0] !== missingFirst) {
                return `Try inserting ${missingFirst} at the front`;
            }
            return `Try inserting ${missingLast} at the end`;
        } else if (this.currentList.length > this.targetList.length) {
            // Need to remove elements
            for (let i = 0; i < this.currentList.length; i++) {
                if (this.currentList[i] !== this.targetList[i]) {
                    return `Try deleting element at position ${i}`;
                }
            }
            return `Try deleting the last element`;
        } else {
            // Same length, might need reverse or specific changes
            const currentReversed = [...this.currentList].reverse();
            if (this.arraysEqual(currentReversed, this.targetList)) {
                return 'Try reversing the list!';
            }
            return 'Compare each position and modify accordingly';
        }
    }
    
    arraysEqual(a, b) {
        if (a.length !== b.length) return false;
        for (let i = 0; i < a.length; i++) {
            if (a[i] !== b[i]) return false;
        }
        return true;
    }
    
    showError(message) {
        const btn = document.getElementById('submitBtn');
        const originalText = btn.textContent;
        btn.textContent = message;
        btn.style.background = 'linear-gradient(135deg, #e74c3c, #c0392b)';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    }
    
    checkSolution() {
        if (this.arraysEqual(this.currentList, this.targetList)) {
            this.showResult(true);
        } else {
            this.showError('Not quite right! Keep trying.');
        }
    }
    
    showResult(success) {
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        if (success) {
            // Bonus for fewer operations
            const optimalOps = Math.abs(this.initialList.length - this.targetList.length) + 2;
            const bonus = Math.max(0, (optimalOps - this.operations) * 10);
            this.score += bonus + 50;
            
            const xpEarned = 50 + this.score;
            
            document.getElementById('resultIcon').textContent = '🎉';
            document.getElementById('resultTitle').textContent = 'List Complete!';
            document.getElementById('resultText').textContent = 'You built the target linked list!';
            document.getElementById('resultOps').textContent = this.operations;
            document.getElementById('resultScore').textContent = this.score;
            document.getElementById('resultXP').textContent = `+${xpEarned}`;
            
            this.reportProgress(xpEarned);
        } else {
            document.getElementById('resultIcon').textContent = '❌';
            document.getElementById('resultTitle').textContent = 'Not Quite';
            document.getElementById('resultText').textContent = 'Try again!';
            document.getElementById('resultOps').textContent = this.operations;
            document.getElementById('resultScore').textContent = 0;
            document.getElementById('resultXP').textContent = '+0';
        }
    }
    
    async reportProgress(xpEarned) {
        try {
            if (typeof GameAPI !== 'undefined') {
                const api = new GameAPI();
                await api.updateProgress({
                    username: this.params.username,
                    game_id: 'link-builder',
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
        this.score = 0;
        this.operations = 0;
        this.hints = 3;
        this.history = [];
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.generateLevel();
        this.updateDisplay();
    }
    
    retryLevel() {
        this.score = 0;
        this.operations = 0;
        this.history = [];
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('opsDisplay').textContent = this.operations;
        document.getElementById('scoreDisplay').textContent = this.score;
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new LinkBuilderGame();
});
