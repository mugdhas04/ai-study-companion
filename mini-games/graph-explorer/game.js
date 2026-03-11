/**
 * Graph Explorer Game
 * Navigate graphs using BFS, DFS, or Dijkstra algorithms
 */

class GraphExplorerGame {
    constructor() {
        // Game parameters
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        // Game state
        this.nodes = [];
        this.edges = [];
        this.adjacencyList = {};
        this.startNode = null;
        this.endNode = null;
        this.currentPath = [];
        this.visitedNodes = new Set();
        this.algorithm = 'bfs';
        this.score = 0;
        this.level = parseInt(this.params.levelId) || 1;
        this.hints = 3;
        
        // Canvas
        this.canvas = document.getElementById('graphCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Node visual settings
        this.nodeRadius = 30;
        this.nodePositions = {};
        
        // Optimal path for comparison
        this.optimalPath = [];
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'graph-explorer',
            levelId: params.get('levelId') || '1',
            difficulty: params.get('difficulty') || 'beginner',
            nodes: params.get('nodes') ? JSON.parse(params.get('nodes')) : null,
            edges: params.get('edges') ? JSON.parse(params.get('edges')) : null
        };
    }
    
    init() {
        this.setupEventListeners();
        this.generateLevel();
        this.updateDisplay();
    }
    
    setupEventListeners() {
        // Algorithm selection
        document.querySelectorAll('.algo-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.algo-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.algorithm = btn.dataset.algo;
                this.updateAlgoInfo();
            });
        });
        
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('submitBtn').addEventListener('click', () => this.submitPath());
        document.getElementById('hintBtn').addEventListener('click', () => this.showHint());
        document.getElementById('undoBtn').addEventListener('click', () => this.undoLastMove());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetPath());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
        
        // Canvas click for node selection
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleCanvasHover(e));
        
        // Select default algorithm
        document.querySelector('.algo-btn[data-algo="bfs"]').classList.add('selected');
    }
    
    generateLevel() {
        // Generate graph based on level/difficulty
        const difficulties = {
            beginner: { nodeCount: 6, edgeCount: 8, weighted: false },
            intermediate: { nodeCount: 8, edgeCount: 12, weighted: true },
            advanced: { nodeCount: 10, edgeCount: 15, weighted: true },
            expert: { nodeCount: 12, edgeCount: 20, weighted: true }
        };
        
        const config = difficulties[this.params.difficulty] || difficulties.beginner;
        
        // Use provided nodes/edges or generate
        if (this.params.nodes && this.params.edges) {
            this.nodes = this.params.nodes;
            this.edges = this.params.edges;
        } else {
            this.generateRandomGraph(config.nodeCount, config.edgeCount, config.weighted);
        }
        
        // Set start and end
        this.startNode = this.nodes[0];
        this.endNode = this.nodes[this.nodes.length - 1];
        
        // Build adjacency list
        this.buildAdjacencyList();
        
        // Calculate node positions for visualization
        this.calculateNodePositions();
        
        // Calculate optimal path
        this.optimalPath = this.calculateOptimalPath();
        
        // Update mission text
        document.getElementById('missionText').textContent = 
            `Find a path from ${this.startNode} to ${this.endNode}`;
    }
    
    generateRandomGraph(nodeCount, edgeCount, weighted) {
        // Generate node labels
        this.nodes = [];
        for (let i = 0; i < nodeCount; i++) {
            this.nodes.push(String.fromCharCode(65 + i)); // A, B, C, ...
        }
        
        // Generate edges ensuring connectivity
        this.edges = [];
        const addedEdges = new Set();
        
        // First, ensure basic connectivity (linear chain)
        for (let i = 0; i < nodeCount - 1; i++) {
            const weight = weighted ? Math.floor(Math.random() * 9) + 1 : 1;
            this.edges.push([this.nodes[i], this.nodes[i + 1], weight]);
            addedEdges.add(`${this.nodes[i]}-${this.nodes[i + 1]}`);
            addedEdges.add(`${this.nodes[i + 1]}-${this.nodes[i]}`);
        }
        
        // Add additional random edges
        while (this.edges.length < edgeCount) {
            const a = this.nodes[Math.floor(Math.random() * nodeCount)];
            const b = this.nodes[Math.floor(Math.random() * nodeCount)];
            
            if (a !== b && !addedEdges.has(`${a}-${b}`)) {
                const weight = weighted ? Math.floor(Math.random() * 9) + 1 : 1;
                this.edges.push([a, b, weight]);
                addedEdges.add(`${a}-${b}`);
                addedEdges.add(`${b}-${a}`);
            }
        }
    }
    
    buildAdjacencyList() {
        this.adjacencyList = {};
        
        this.nodes.forEach(node => {
            this.adjacencyList[node] = [];
        });
        
        this.edges.forEach(([from, to, weight]) => {
            this.adjacencyList[from].push({ node: to, weight });
            this.adjacencyList[to].push({ node: from, weight }); // Undirected
        });
    }
    
    calculateNodePositions() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 60;
        
        // Arrange nodes in a circle
        this.nodes.forEach((node, i) => {
            const angle = (2 * Math.PI * i / this.nodes.length) - Math.PI / 2;
            this.nodePositions[node] = {
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle)
            };
        });
    }
    
    calculateOptimalPath() {
        // Use BFS for unweighted, Dijkstra for weighted
        const hasWeights = this.edges.some(e => e[2] > 1);
        
        if (hasWeights) {
            return this.dijkstra(this.startNode, this.endNode);
        } else {
            return this.bfs(this.startNode, this.endNode);
        }
    }
    
    bfs(start, end) {
        const queue = [[start]];
        const visited = new Set([start]);
        
        while (queue.length > 0) {
            const path = queue.shift();
            const node = path[path.length - 1];
            
            if (node === end) return path;
            
            for (const neighbor of this.adjacencyList[node]) {
                if (!visited.has(neighbor.node)) {
                    visited.add(neighbor.node);
                    queue.push([...path, neighbor.node]);
                }
            }
        }
        
        return [];
    }
    
    dijkstra(start, end) {
        const distances = {};
        const previous = {};
        const pq = [];
        
        this.nodes.forEach(node => {
            distances[node] = Infinity;
            previous[node] = null;
        });
        distances[start] = 0;
        pq.push({ node: start, dist: 0 });
        
        while (pq.length > 0) {
            pq.sort((a, b) => a.dist - b.dist);
            const { node } = pq.shift();
            
            if (node === end) break;
            
            for (const neighbor of this.adjacencyList[node]) {
                const alt = distances[node] + neighbor.weight;
                if (alt < distances[neighbor.node]) {
                    distances[neighbor.node] = alt;
                    previous[neighbor.node] = node;
                    pq.push({ node: neighbor.node, dist: alt });
                }
            }
        }
        
        // Reconstruct path
        const path = [];
        let current = end;
        while (current) {
            path.unshift(current);
            current = previous[current];
        }
        
        return path[0] === start ? path : [];
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        // Initialize path with start node
        this.currentPath = [this.startNode];
        this.visitedNodes = new Set([this.startNode]);
        
        this.drawGraph();
        this.updatePathDisplay();
        this.updateAlgoInfo();
    }
    
    handleCanvasClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Find clicked node
        const clickedNode = this.findClickedNode(x, y);
        
        if (clickedNode && this.isValidMove(clickedNode)) {
            this.moveToNode(clickedNode);
        }
    }
    
    handleCanvasHover(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const hoveredNode = this.findClickedNode(x, y);
        
        // Redraw with hover effect
        this.drawGraph(hoveredNode);
    }
    
    findClickedNode(x, y) {
        for (const node of this.nodes) {
            const pos = this.nodePositions[node];
            const dist = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2);
            if (dist <= this.nodeRadius) {
                return node;
            }
        }
        return null;
    }
    
    isValidMove(node) {
        if (this.currentPath.includes(node)) return false;
        
        const currentNode = this.currentPath[this.currentPath.length - 1];
        const neighbors = this.adjacencyList[currentNode].map(n => n.node);
        
        return neighbors.includes(node);
    }
    
    moveToNode(node) {
        this.currentPath.push(node);
        this.visitedNodes.add(node);
        this.score += 5;
        
        this.drawGraph();
        this.updatePathDisplay();
        this.updateDisplay();
        
        // Check if reached end
        if (node === this.endNode) {
            this.submitPath();
        }
    }
    
    drawGraph(hoveredNode = null) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw edges
        this.edges.forEach(([from, to, weight]) => {
            const fromPos = this.nodePositions[from];
            const toPos = this.nodePositions[to];
            
            // Check if edge is in current path
            const inPath = this.isEdgeInPath(from, to);
            
            this.ctx.beginPath();
            this.ctx.moveTo(fromPos.x, fromPos.y);
            this.ctx.lineTo(toPos.x, toPos.y);
            this.ctx.strokeStyle = inPath ? '#3498db' : '#444';
            this.ctx.lineWidth = inPath ? 4 : 2;
            this.ctx.stroke();
            
            // Draw weight
            if (weight > 1) {
                const midX = (fromPos.x + toPos.x) / 2;
                const midY = (fromPos.y + toPos.y) / 2;
                
                this.ctx.fillStyle = '#1a1a2e';
                this.ctx.beginPath();
                this.ctx.arc(midX, midY, 15, 0, Math.PI * 2);
                this.ctx.fill();
                
                this.ctx.fillStyle = '#fff';
                this.ctx.font = 'bold 12px Orbitron';
                this.ctx.textAlign = 'center';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(weight, midX, midY);
            }
        });
        
        // Draw nodes
        this.nodes.forEach(node => {
            const pos = this.nodePositions[node];
            const isStart = node === this.startNode;
            const isEnd = node === this.endNode;
            const isInPath = this.currentPath.includes(node);
            const isCurrent = node === this.currentPath[this.currentPath.length - 1];
            const isHovered = node === hoveredNode;
            const isValidNext = this.isValidMove(node);
            
            // Node style
            let gradient;
            if (isStart) {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#2ecc71');
                gradient.addColorStop(1, '#27ae60');
            } else if (isEnd) {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#e74c3c');
                gradient.addColorStop(1, '#c0392b');
            } else if (isCurrent) {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#f39c12');
                gradient.addColorStop(1, '#e67e22');
            } else if (isInPath) {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#3498db');
                gradient.addColorStop(1, '#2980b9');
            } else if (isHovered && isValidNext) {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#9b59b6');
                gradient.addColorStop(1, '#8e44ad');
            } else {
                gradient = this.ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, this.nodeRadius);
                gradient.addColorStop(0, '#444');
                gradient.addColorStop(1, '#333');
            }
            
            // Draw node
            this.ctx.beginPath();
            this.ctx.arc(pos.x, pos.y, this.nodeRadius, 0, Math.PI * 2);
            this.ctx.fillStyle = gradient;
            this.ctx.fill();
            
            // Border
            this.ctx.strokeStyle = isCurrent ? '#fff' : (isValidNext && isHovered ? '#9b59b6' : '#666');
            this.ctx.lineWidth = isCurrent ? 3 : 2;
            this.ctx.stroke();
            
            // Label
            this.ctx.fillStyle = '#fff';
            this.ctx.font = 'bold 18px Orbitron';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(node, pos.x, pos.y);
        });
    }
    
    isEdgeInPath(from, to) {
        for (let i = 0; i < this.currentPath.length - 1; i++) {
            if ((this.currentPath[i] === from && this.currentPath[i + 1] === to) ||
                (this.currentPath[i] === to && this.currentPath[i + 1] === from)) {
                return true;
            }
        }
        return false;
    }
    
    updatePathDisplay() {
        const container = document.getElementById('pathDisplay');
        container.innerHTML = this.currentPath.map((node, i) => {
            let className = 'path-node';
            if (node === this.startNode) className += ' start';
            if (node === this.endNode) className += ' end';
            
            const arrow = i < this.currentPath.length - 1 ? '<span class="path-arrow">→</span>' : '';
            return `<span class="${className}">${node}</span>${arrow}`;
        }).join('');
    }
    
    updateAlgoInfo() {
        const info = {
            bfs: { icon: '🌊', text: 'BFS Mode: Explore level by level. Best for unweighted shortest path.' },
            dfs: { icon: '🕳️', text: 'DFS Mode: Go deep first, then backtrack. Explores all paths.' },
            dijkstra: { icon: '⚡', text: 'Dijkstra Mode: Find shortest weighted path. Consider edge weights!' }
        };
        
        const current = info[this.algorithm];
        document.querySelector('.algo-info-icon').textContent = current.icon;
        document.querySelector('.algo-info-text').innerHTML = `<strong>${this.algorithm.toUpperCase()} Mode:</strong> ${current.text}`;
    }
    
    undoLastMove() {
        if (this.currentPath.length <= 1) return;
        
        const removed = this.currentPath.pop();
        this.visitedNodes.delete(removed);
        this.score = Math.max(0, this.score - 5);
        
        this.drawGraph();
        this.updatePathDisplay();
        this.updateDisplay();
    }
    
    resetPath() {
        this.currentPath = [this.startNode];
        this.visitedNodes = new Set([this.startNode]);
        this.score = 0;
        
        this.drawGraph();
        this.updatePathDisplay();
        this.updateDisplay();
    }
    
    showHint() {
        if (this.hints <= 0) {
            alert('No hints remaining!');
            return;
        }
        
        this.hints--;
        
        // Show the next node in optimal path
        const currentNode = this.currentPath[this.currentPath.length - 1];
        const currentInOptimal = this.optimalPath.indexOf(currentNode);
        
        if (currentInOptimal >= 0 && currentInOptimal < this.optimalPath.length - 1) {
            const nextNode = this.optimalPath[currentInOptimal + 1];
            alert(`💡 Hint: Try moving to node ${nextNode}`);
        } else {
            // If off the optimal path, suggest backtracking
            alert(`💡 Hint: The optimal path is ${this.optimalPath.join(' → ')}`);
        }
        
        this.updateDisplay();
    }
    
    submitPath() {
        const reachedEnd = this.currentPath[this.currentPath.length - 1] === this.endNode;
        
        if (!reachedEnd) {
            alert('Find a path to the end node first!');
            return;
        }
        
        // Calculate score based on path efficiency
        const efficiency = this.optimalPath.length / this.currentPath.length;
        const bonusScore = Math.floor(efficiency * 100);
        this.score += bonusScore;
        
        this.showResult(true);
    }
    
    showResult(success) {
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        const xpEarned = success ? (50 + this.score) : 0;
        
        document.getElementById('resultIcon').textContent = success ? '🎉' : '❌';
        document.getElementById('resultTitle').textContent = success ? 'Path Found!' : 'Path Not Found';
        document.getElementById('resultText').textContent = success 
            ? `You navigated from ${this.startNode} to ${this.endNode}!`
            : 'Try again to find a valid path.';
        document.getElementById('resultSteps').textContent = this.currentPath.length - 1;
        document.getElementById('resultOptimal').textContent = this.optimalPath.length - 1;
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
                    game_id: 'graph-explorer',
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
        this.currentPath = [];
        this.visitedNodes = new Set();
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.generateLevel();
        this.updateDisplay();
    }
    
    retryLevel() {
        this.score = 0;
        this.currentPath = [];
        this.visitedNodes = new Set();
        
        document.getElementById('resultPanel').classList.add('hidden');
        document.getElementById('missionPanel').classList.remove('hidden');
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('stepsDisplay').textContent = Math.max(0, this.currentPath.length - 1);
        document.getElementById('scoreDisplay').textContent = this.score;
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new GraphExplorerGame();
});
