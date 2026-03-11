// Stack Tower Game Logic
class StackTowerGame {
    constructor() {
        this.stack = [];
        this.availableBlocks = [];
        this.selectedBlock = null;
        this.score = 0;
        this.level = 1;
        this.operations = 0;
        this.targetSequence = [];
        this.currentSequenceIndex = 0;
        
        // Get parameters from window.GAME_PARAMS (injected by Streamlit) or URL
        const params = window.GAME_PARAMS || this.getURLParams();
        this.username = params.username || 'guest';
        this.gameId = params.gameId || 'dsa';
        this.levelId = parseInt(params.levelId) || 1;
        
        this.initializeGame();
    }
    
    getURLParams() {
        const urlParams = new URLSearchParams(window.location.search);
        return {
            username: urlParams.get('username'),
            gameId: urlParams.get('gameId'),
            levelId: urlParams.get('levelId')
        };
    }
    
    initializeGame() {
        // Generate level challenge
        this.generateLevelChallenge();
        
        // Setup event listeners
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('pushBtn').addEventListener('click', () => this.pushToStack());
        document.getElementById('popBtn').addEventListener('click', () => this.popFromStack());
        document.getElementById('peekBtn').addEventListener('click', () => this.peekStack());
        document.getElementById('continueBtn').addEventListener('click', () => this.continueToNextLevel());
    }
    
    generateLevelChallenge() {
        // Level 1-3: Basic PUSH operations
        // Level 4-6: PUSH and POP combinations
        // Level 7+: Complex sequences
        
        const operations = [];
        const blocks = [];
        
        if (this.level <= 3) {
            // Simple PUSH sequence
            const blockCount = 3 + this.level;
            for (let i = 1; i <= blockCount; i++) {
                blocks.push(i);
                operations.push({ type: 'PUSH', value: i });
            }
        } else if (this.level <= 6) {
            // PUSH and POP mix
            const blockCount = 5;
            for (let i = 1; i <= blockCount; i++) {
                blocks.push(i);
                operations.push({ type: 'PUSH', value: i });
            }
            // Add some POP operations
            for (let i = 0; i < 2; i++) {
                operations.push({ type: 'POP', value: null });
            }
        } else {
            // Complex sequences
            const blockCount = 6;
            for (let i = 1; i <= blockCount; i++) {
                blocks.push(i);
                operations.push({ type: 'PUSH', value: i });
            }
            for (let i = 0; i < 3; i++) {
                operations.push({ type: 'POP', value: null });
            }
        }
        
        this.availableBlocks = blocks;
        this.targetSequence = operations;
        
        // Display operations
        const sequenceDiv = document.getElementById('operationSequence');
        sequenceDiv.innerHTML = '';
        operations.forEach(op => {
            const chip = document.createElement('div');
            chip.className = 'operation-chip';
            chip.textContent = op.type === 'PUSH' ? `PUSH ${op.value}` : 'POP';
            sequenceDiv.appendChild(chip);
        });
        
        document.getElementById('missionText').textContent = 
            `Complete ${operations.length} operations in the correct order!`;
    }
    
    startGame() {
        document.getElementById('missionPanel').style.display = 'none';
        document.getElementById('gameArea').style.display = 'grid';
        
        this.renderBlocks();
        this.updateUI();
        this.addLog('Game started! Complete the operation sequence.', 'info');
    }
    
    renderBlocks() {
        const grid = document.getElementById('blocksGrid');
        grid.innerHTML = '';
        
        this.availableBlocks.forEach(block => {
            const blockDiv = document.createElement('div');
            blockDiv.className = 'block-item';
            blockDiv.textContent = block;
            blockDiv.dataset.value = block;
            
            blockDiv.addEventListener('click', () => {
                if (!blockDiv.classList.contains('used')) {
                    this.selectBlock(block, blockDiv);
                }
            });
            
            grid.appendChild(blockDiv);
        });
    }
    
    selectBlock(value, element) {
        // Remove previous selection
        document.querySelectorAll('.block-item').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Select new block
        element.classList.add('selected');
        this.selectedBlock = value;
        
        // Enable PUSH button
        document.getElementById('pushBtn').disabled = false;
        
        this.addLog(`Selected block: ${value}`, 'info');
    }
    
    pushToStack() {
        if (this.selectedBlock === null) {
            this.addLog('Please select a block first!', 'error');
            return;
        }
        
        // Check if this matches the expected operation
        const expectedOp = this.targetSequence[this.currentSequenceIndex];
        
        if (expectedOp.type !== 'PUSH' || expectedOp.value !== this.selectedBlock) {
            this.addLog(`Wrong operation! Expected: ${this.getExpectedOperationText()}`, 'error');
            return;
        }
        
        // Add to stack
        this.stack.push(this.selectedBlock);
        this.operations++;
        this.score += 10;
        this.currentSequenceIndex++;
        
        // Mark block as used
        document.querySelectorAll('.block-item').forEach(el => {
            if (parseInt(el.dataset.value) === this.selectedBlock) {
                el.classList.add('used');
                el.classList.remove('selected');
            }
        });
        
        this.selectedBlock = null;
        document.getElementById('pushBtn').disabled = true;
        
        this.addLog(`Pushed ${this.stack[this.stack.length - 1]} to stack`, 'success');
        this.updateStackVisual();
        this.updateUI();
        this.checkCompletion();
    }
    
    popFromStack() {
        if (this.stack.length === 0) {
            this.addLog('Stack is empty! Cannot POP.', 'error');
            return;
        }
        
        // Check if this matches the expected operation
        const expectedOp = this.targetSequence[this.currentSequenceIndex];
        
        if (expectedOp.type !== 'POP') {
            this.addLog(`Wrong operation! Expected: ${this.getExpectedOperationText()}`, 'error');
            return;
        }
        
        const popped = this.stack.pop();
        this.operations++;
        this.score += 15;
        this.currentSequenceIndex++;
        
        this.addLog(`Popped ${popped} from stack`, 'success');
        this.updateStackVisual();
        this.updateUI();
        this.checkCompletion();
    }
    
    peekStack() {
        if (this.stack.length === 0) {
            this.addLog('Stack is empty!', 'info');
        } else {
            this.addLog(`Top of stack: ${this.stack[this.stack.length - 1]}`, 'info');
        }
    }
    
    getExpectedOperationText() {
        const op = this.targetSequence[this.currentSequenceIndex];
        return op.type === 'PUSH' ? `PUSH ${op.value}` : 'POP';
    }
    
    updateStackVisual() {
        const stackDiv = document.getElementById('stack');
        stackDiv.innerHTML = '';
        
        if (this.stack.length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'stack-empty-message';
            emptyMsg.textContent = 'Empty Stack';
            stackDiv.appendChild(emptyMsg);
        } else {
            this.stack.forEach(value => {
                const block = document.createElement('div');
                block.className = 'stack-block';
                block.textContent = value;
                stackDiv.appendChild(block);
            });
        }
        
        // Enable/disable buttons based on stack state
        document.getElementById('popBtn').disabled = this.stack.length === 0;
        document.getElementById('peekBtn').disabled = this.stack.length === 0;
    }
    
    updateUI() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('level').textContent = this.level;
    }
    
    addLog(message, type = 'info') {
        const logContent = document.getElementById('logContent');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logContent.insertBefore(entry, logContent.firstChild);
    }
    
    async checkCompletion() {
        if (this.currentSequenceIndex >= this.targetSequence.length) {
            // Level complete!
            const xp = 20 + (this.level * 5);
            
            // Send progress to API
            try {
                const result = await window.GameAPI.updateProgress(
                    this.username,
                    this.gameId,
                    this.levelId,
                    xp,
                    this.score,
                    true
                );
                
                this.showResultPanel(xp, result);
            } catch (error) {
                console.error('Failed to sync progress:', error);
                this.showResultPanel(xp, null);
            }
        }
    }
    
    showResultPanel(xp, apiResult) {
        document.getElementById('resultTitle').textContent = '🎉 LEVEL COMPLETE!';
        document.getElementById('resultMessage').textContent = 
            'Perfect! You\'ve mastered LIFO Stack operations.';
        document.getElementById('resultOps').textContent = this.operations;
        document.getElementById('resultXP').textContent = `+${xp}`;
        
        document.getElementById('resultPanel').style.display = 'flex';
    }
    
    continueToNextLevel() {
        // In production, this would navigate back to Streamlit or load next level
        window.parent.postMessage({ 
            type: 'LEVEL_COMPLETE',
            gameId: this.gameId,
            levelId: this.levelId,
            score: this.score
        }, '*');
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new StackTowerGame();
});
