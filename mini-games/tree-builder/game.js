/**
 * Tree Builder Game
 * Build Binary Search Trees interactively
 */

class TreeBuilderGame {
    constructor() {
        // Game parameters
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        // Game state
        this.tree = null;
        this.nodesToInsert = [];
        this.currentNodeIndex = 0;
        this.score = 0;
        this.level = parseInt(this.params.levelId) || 1;
        this.hints = 3;
        
        // Canvas
        this.canvas = document.getElementById('treeCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Tree visual settings
        this.nodeRadius = 25;
        this.levelHeight = 80;
        this.startY = 60;
        
        // Interaction state
        this.selectedPosition = null;
        this.highlightedNode = null;
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'tree-builder',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner',
            nodes: params.get('nodes') ? JSON.parse(params.get('nodes')) : null
        };
    }
    
    init() {
        this.setupEventListeners();
        this.generateLevel();
        this.updateDisplay();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('submitBtn').addEventListener('click', () => this.submitTree());
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('undoBtn').addEventListener('click', () => this.undoLastInsert());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
        
        // Canvas click for inserting nodes
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleCanvasHover(e));
    }
    
    generateLevel() {
        // Generate nodes based on level/difficulty
        const difficulties = {
            beginner: { count: 5, max: 20 },
            intermediate: { count: 7, max: 50 },
            advanced: { count: 9, max: 100 },
            expert: { count: 12, max: 200 }
        };
        
        const config = difficulties[this.params.difficulty] || difficulties.beginner;
        
        // Use provided nodes or generate random ones
        if (this.params.nodes) {
            this.nodesToInsert = this.params.nodes;
        } else {
            this.nodesToInsert = this.generateRandomNodes(config.count, config.max);
        }
        
        // Display nodes in mission panel
        const nodesContainer = document.getElementById('nodesToInsert');
        nodesContainer.innerHTML = this.nodesToInsert.map(n => 
            `<div class="mission-node">${n}</div>`
        ).join('');
        
        document.getElementById('missionText').textContent = 
            `Insert ${this.nodesToInsert.length} nodes to build a valid Binary Search Tree`;
    }
    
    generateRandomNodes(count, maxValue) {
        const nodes = new Set();
        while (nodes.size < count) {
            nodes.add(Math.floor(Math.random() * maxValue) + 1);
        }
        return Array.from(nodes);
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        // Initialize empty tree
        this.tree = null;
        this.currentNodeIndex = 0;
        this.insertHistory = [];
        
        this.updateCurrentNode();
        this.drawTree();
    }
    
    updateCurrentNode() {
        const nodeDisplay = document.getElementById('currentNode');
        if (this.currentNodeIndex < this.nodesToInsert.length) {
            nodeDisplay.textContent = this.nodesToInsert[this.currentNodeIndex];
            nodeDisplay.style.animation = 'none';
            nodeDisplay.offsetHeight; // Trigger reflow
            nodeDisplay.style.animation = 'pulse 1.5s ease-in-out infinite';
        } else {
            nodeDisplay.textContent = '✓';
            nodeDisplay.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
        }
    }
    
    handleCanvasClick(e) {
        if (this.currentNodeIndex >= this.nodesToInsert.length) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const currentValue = this.nodesToInsert[this.currentNodeIndex];
        
        // If tree is empty, create root
        if (!this.tree) {
            this.tree = this.createNode(currentValue);
            this.insertHistory.push({ action: 'root', value: currentValue });
            this.currentNodeIndex++;
            this.updateCurrentNode();
            this.drawTree();
            this.updateTraversals();
            return;
        }
        
        // Find clicked position and validate BST property
        const clickedSlot = this.findClickedSlot(x, y, this.tree, this.canvas.width / 2, this.startY, this.canvas.width / 4);
        
        if (clickedSlot) {
            if (this.isValidInsertion(clickedSlot.parent, clickedSlot.direction, currentValue)) {
                // Insert node
                const newNode = this.createNode(currentValue);
                if (clickedSlot.direction === 'left') {
                    clickedSlot.parent.left = newNode;
                } else {
                    clickedSlot.parent.right = newNode;
                }
                
                this.insertHistory.push({
                    action: 'insert',
                    value: currentValue,
                    parent: clickedSlot.parent.value,
                    direction: clickedSlot.direction
                });
                
                this.currentNodeIndex++;
                this.updateCurrentNode();
                this.drawTree();
                this.updateTraversals();
                this.score += 10;
                this.updateDisplay();
            } else {
                this.showError('Invalid BST position! Remember: Left < Parent < Right');
            }
        }
    }
    
    handleCanvasHover(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Highlight potential insertion points
        this.drawTree();
        
        if (this.tree && this.currentNodeIndex < this.nodesToInsert.length) {
            const slot = this.findClickedSlot(x, y, this.tree, this.canvas.width / 2, this.startY, this.canvas.width / 4);
            if (slot) {
                this.highlightSlot(slot.x, slot.y);
            }
        }
    }
    
    findClickedSlot(x, y, node, nodeX, nodeY, offset, parent = null, direction = null) {
        if (!node) return null;
        
        const nextY = nodeY + this.levelHeight;
        const leftX = nodeX - offset;
        const rightX = nodeX + offset;
        
        // Check left slot
        if (!node.left) {
            const dist = Math.sqrt((x - leftX) ** 2 + (y - nextY) ** 2);
            if (dist < this.nodeRadius * 1.5) {
                return { parent: node, direction: 'left', x: leftX, y: nextY };
            }
        } else {
            const leftResult = this.findClickedSlot(x, y, node.left, leftX, nextY, offset / 2, node, 'left');
            if (leftResult) return leftResult;
        }
        
        // Check right slot
        if (!node.right) {
            const dist = Math.sqrt((x - rightX) ** 2 + (y - nextY) ** 2);
            if (dist < this.nodeRadius * 1.5) {
                return { parent: node, direction: 'right', x: rightX, y: nextY };
            }
        } else {
            const rightResult = this.findClickedSlot(x, y, node.right, rightX, nextY, offset / 2, node, 'right');
            if (rightResult) return rightResult;
        }
        
        return null;
    }
    
    isValidInsertion(parent, direction, value) {
        if (direction === 'left') {
            return value < parent.value;
        } else {
            return value > parent.value;
        }
    }
    
    createNode(value) {
        return { value, left: null, right: null };
    }
    
    drawTree() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (!this.tree) {
            // Draw empty slot for root
            this.drawEmptySlot(this.canvas.width / 2, this.startY);
            return;
        }
        
        this.drawNode(this.tree, this.canvas.width / 2, this.startY, this.canvas.width / 4);
    }
    
    drawNode(node, x, y, offset) {
        if (!node) return;
        
        const nextY = y + this.levelHeight;
        
        // Draw edges first
        this.ctx.strokeStyle = '#2ecc71';
        this.ctx.lineWidth = 3;
        
        if (node.left) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, y + this.nodeRadius);
            this.ctx.lineTo(x - offset, nextY - this.nodeRadius);
            this.ctx.stroke();
        } else if (this.currentNodeIndex < this.nodesToInsert.length) {
            // Draw empty slot
            this.drawEmptySlot(x - offset, nextY);
        }
        
        if (node.right) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, y + this.nodeRadius);
            this.ctx.lineTo(x + offset, nextY - this.nodeRadius);
            this.ctx.stroke();
        } else if (this.currentNodeIndex < this.nodesToInsert.length) {
            // Draw empty slot
            this.drawEmptySlot(x + offset, nextY);
        }
        
        // Draw node circle
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, this.nodeRadius);
        gradient.addColorStop(0, '#2ecc71');
        gradient.addColorStop(1, '#27ae60');
        
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.nodeRadius, 0, Math.PI * 2);
        this.ctx.fillStyle = gradient;
        this.ctx.fill();
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
        
        // Draw value
        this.ctx.fillStyle = '#fff';
        this.ctx.font = 'bold 18px Orbitron';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(node.value, x, y);
        
        // Recursively draw children
        if (node.left) this.drawNode(node.left, x - offset, nextY, offset / 2);
        if (node.right) this.drawNode(node.right, x + offset, nextY, offset / 2);
    }
    
    drawEmptySlot(x, y) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.nodeRadius, 0, Math.PI * 2);
        this.ctx.strokeStyle = '#555';
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);
        this.ctx.stroke();
        this.ctx.setLineDash([]);
        
        this.ctx.fillStyle = '#444';
        this.ctx.font = '14px Rajdhani';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('?', x, y);
    }
    
    highlightSlot(x, y) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.nodeRadius + 5, 0, Math.PI * 2);
        this.ctx.strokeStyle = '#f39c12';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
    }
    
    updateTraversals() {
        const inorder = this.inorderTraversal(this.tree);
        const preorder = this.preorderTraversal(this.tree);
        
        document.getElementById('inorderDisplay').textContent = inorder.join(' → ') || '-';
        document.getElementById('preorderDisplay').textContent = preorder.join(' → ') || '-';
    }
    
    inorderTraversal(node, result = []) {
        if (node) {
            this.inorderTraversal(node.left, result);
            result.push(node.value);
            this.inorderTraversal(node.right, result);
        }
        return result;
    }
    
    preorderTraversal(node, result = []) {
        if (node) {
            result.push(node.value);
            this.preorderTraversal(node.left, result);
            this.preorderTraversal(node.right, result);
        }
        return result;
    }
    
    undoLastInsert() {
        if (this.insertHistory.length === 0) return;
        
        const lastAction = this.insertHistory.pop();
        
        if (lastAction.action === 'root') {
            this.tree = null;
        } else {
            // Find parent and remove child
            const parent = this.findNode(this.tree, lastAction.parent);
            if (parent) {
                if (lastAction.direction === 'left') {
                    parent.left = null;
                } else {
                    parent.right = null;
                }
            }
        }
        
        this.currentNodeIndex--;
        this.score = Math.max(0, this.score - 5);
        this.updateCurrentNode();
        this.drawTree();
        this.updateTraversals();
        this.updateDisplay();
    }
    
    findNode(root, value) {
        if (!root) return null;
        if (root.value === value) return root;
        return this.findNode(root.left, value) || this.findNode(root.right, value);
    }
    
    showHint() {
        if (this.hints <= 0) {
            this.showError('No hints remaining!');
            return;
        }
        
        this.hints--;
        const currentValue = this.nodesToInsert[this.currentNodeIndex];
        
        // Find correct position
        if (!this.tree) {
            alert(`💡 Hint: Insert ${currentValue} as the root node (click in the center)`);
        } else {
            const position = this.findCorrectPosition(this.tree, currentValue);
            alert(`💡 Hint: ${currentValue} should go to the ${position.direction} of ${position.parent}`);
        }
        
        this.updateDisplay();
    }
    
    findCorrectPosition(node, value) {
        if (value < node.value) {
            if (!node.left) {
                return { parent: node.value, direction: 'LEFT' };
            }
            return this.findCorrectPosition(node.left, value);
        } else {
            if (!node.right) {
                return { parent: node.value, direction: 'RIGHT' };
            }
            return this.findCorrectPosition(node.right, value);
        }
    }
    
    showError(message) {
        // Simple error display
        const btn = document.getElementById('submitBtn');
        btn.textContent = message;
        btn.style.background = 'linear-gradient(135deg, #e74c3c, #c0392b)';
        
        setTimeout(() => {
            btn.textContent = '✅ Submit Tree';
            btn.style.background = '';
        }, 2000);
    }
    
    submitTree() {
        if (this.currentNodeIndex < this.nodesToInsert.length) {
            this.showError('Insert all nodes first!');
            return;
        }
        
        // Verify it's a valid BST
        if (this.isValidBST(this.tree)) {
            this.showResult(true);
        } else {
            this.showResult(false);
        }
    }
    
    isValidBST(node, min = -Infinity, max = Infinity) {
        if (!node) return true;
        if (node.value <= min || node.value >= max) return false;
        return this.isValidBST(node.left, min, node.value) && 
               this.isValidBST(node.right, node.value, max);
    }
    
    showResult(success) {
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        if (success) {
            const xpEarned = 50 + (this.hints * 10) + this.score;
            
            document.getElementById('resultIcon').textContent = '🎉';
            document.getElementById('resultTitle').textContent = 'Perfect Tree!';
            document.getElementById('resultText').textContent = 'You built a valid Binary Search Tree!';
            document.getElementById('resultScore').textContent = this.score;
            document.getElementById('resultXP').textContent = `+${xpEarned}`;
            
            // Report progress
            this.reportProgress(xpEarned);
        } else {
            document.getElementById('resultIcon').textContent = '❌';
            document.getElementById('resultTitle').textContent = 'Invalid BST';
            document.getElementById('resultText').textContent = 'The tree violates BST properties. Try again!';
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
                    game_id: 'tree-builder',
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
        this.hints = 3;
        this.tree = null;
        this.currentNodeIndex = 0;
        this.insertHistory = [];
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.generateLevel();
        this.updateDisplay();
    }
    
    retryLevel() {
        this.score = 0;
        this.tree = null;
        this.currentNodeIndex = 0;
        this.insertHistory = [];
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('scoreDisplay').textContent = this.score;
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new TreeBuilderGame();
});
