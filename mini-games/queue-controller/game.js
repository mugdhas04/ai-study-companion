/**
 * Queue Traffic Controller Game
 * Learn FIFO queue operations by managing car traffic
 * Complexity increases with each level via AI parameters
 */

class QueueTrafficController {
    constructor() {
        this.params = window.GAME_PARAMS || this.getURLParams();
        
        this.level = parseInt(this.params.levelId) || 1;
        this.difficulty = this.params.difficulty || 'beginner';
        
        // Generate level config with AI complexity
        this.config = this.generateLevelConfig();
        
        // Game state
        this.queue = [];
        this.maxQueueSize = this.config.maxQueueSize;
        this.incomingCars = [];
        this.processedCars = [];
        this.currentCarId = 1;
        this.score = 0;
        this.lives = 3;
        this.carsToProcess = this.config.carsToProcess;
        this.gameActive = false;
        this.spawnInterval = null;
        this.timeLeft = this.config.timeLimit;
        this.timerInterval = null;
        
        this.init();
    }
    
    getURLParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            username: params.get('username') || 'Guest',
            gameId: params.get('gameId') || 'queue-controller',
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
        
        const complexity = Math.floor(level * difficultyMultiplier);
        
        // Queue size decreases at higher levels (more challenging)
        const maxQueueSize = Math.max(3, 7 - Math.floor(complexity / 3));
        
        // More cars to process at higher levels
        const carsToProcess = Math.min(8 + complexity * 2, 25);
        
        // Faster spawn rate at higher levels
        const spawnRate = Math.max(800, 2500 - complexity * 150);
        
        // Time limit at higher levels
        const timeLimit = complexity >= 4 ? Math.max(30, 90 - complexity * 5) : 0;
        
        // Special mechanics at higher levels
        const hasVIPCars = complexity >= 3;
        const hasUrgentCars = complexity >= 5;
        const hasPriorityCars = complexity >= 7;
        
        return {
            maxQueueSize,
            carsToProcess,
            spawnRate,
            timeLimit,
            hasVIPCars,
            hasUrgentCars,
            hasPriorityCars,
            complexity,
            objectives: this.generateObjectives(complexity)
        };
    }
    
    generateObjectives(complexity) {
        const objectives = ['Release cars in FIFO order'];
        
        if (complexity >= 2) {
            objectives.push("Don't let the queue overflow");
        }
        if (complexity >= 4) {
            objectives.push('Complete within time limit');
        }
        if (complexity >= 6) {
            objectives.push('Handle priority cars correctly');
        }
        
        return objectives;
    }
    
    init() {
        this.setupEventListeners();
        this.updateMissionDisplay();
        this.renderQueue();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.startGame());
        document.getElementById('enqueueBtn').addEventListener('click', () => this.enqueueNextCar());
        document.getElementById('dequeueBtn').addEventListener('click', () => this.dequeue());
        document.getElementById('peekBtn').addEventListener('click', () => this.peek());
        document.getElementById('releaseBtn').addEventListener('click', () => this.releaseCar());
        document.getElementById('continueBtn').addEventListener('click', () => this.nextLevel());
        document.getElementById('retryBtn').addEventListener('click', () => this.retryLevel());
    }
    
    updateMissionDisplay() {
        document.getElementById('queueSizeDisplay').textContent = this.config.maxQueueSize;
        document.getElementById('carsCountDisplay').textContent = this.config.carsToProcess;
        
        const speeds = ['Slow', 'Normal', 'Fast', 'Insane'];
        const speedIndex = Math.min(Math.floor(this.config.complexity / 2), speeds.length - 1);
        document.getElementById('speedDisplay').textContent = speeds[speedIndex];
        
        const objectivesList = document.getElementById('objectivesList');
        objectivesList.innerHTML = this.config.objectives.map(obj => 
            `<li>${obj}</li>`
        ).join('');
        
        if (this.config.complexity >= 4) {
            document.getElementById('missionText').textContent = 
                `Advanced traffic control! Process ${this.config.carsToProcess} cars within ${this.config.timeLimit} seconds!`;
        }
    }
    
    startGame() {
        document.getElementById('missionPanel').classList.add('hidden');
        document.getElementById('gameArea').classList.remove('hidden');
        
        document.getElementById('maxSize').textContent = this.maxQueueSize;
        
        this.gameActive = true;
        this.generateIncomingCars();
        this.renderIncomingCars();
        this.renderQueue();
        this.updateDisplay();
        
        // Start car spawning
        this.startCarSpawning();
        
        // Start timer if applicable
        if (this.config.timeLimit > 0) {
            this.startTimer();
        }
    }
    
    generateIncomingCars() {
        this.incomingCars = [];
        const colors = ['🚗', '🚙', '🚕', '🚐', '🚎'];
        
        for (let i = 0; i < Math.min(5, this.carsToProcess); i++) {
            const carType = this.getCarType();
            this.incomingCars.push({
                id: this.currentCarId++,
                emoji: colors[Math.floor(Math.random() * colors.length)],
                type: carType,
                priority: carType === 'vip' ? 2 : carType === 'urgent' ? 3 : 1
            });
        }
    }
    
    getCarType() {
        const rand = Math.random();
        if (this.config.hasUrgentCars && rand < 0.1) return 'urgent';
        if (this.config.hasVIPCars && rand < 0.25) return 'vip';
        return 'normal';
    }
    
    startCarSpawning() {
        this.spawnInterval = setInterval(() => {
            if (!this.gameActive) return;
            
            if (this.incomingCars.length < 6 && this.processedCars.length + this.queue.length < this.carsToProcess) {
                const carType = this.getCarType();
                const colors = ['🚗', '🚙', '🚕', '🚐', '🚎'];
                
                this.incomingCars.push({
                    id: this.currentCarId++,
                    emoji: colors[Math.floor(Math.random() * colors.length)],
                    type: carType,
                    priority: carType === 'vip' ? 2 : carType === 'urgent' ? 3 : 1
                });
                
                this.renderIncomingCars();
            }
        }, this.config.spawnRate);
    }
    
    startTimer() {
        document.getElementById('timerDisplay').textContent = this.timeLeft;
        
        this.timerInterval = setInterval(() => {
            this.timeLeft--;
            document.getElementById('timerDisplay').textContent = this.timeLeft;
            
            if (this.timeLeft <= 0) {
                this.endGame(false, 'Time ran out!');
            }
        }, 1000);
    }
    
    renderIncomingCars() {
        const container = document.getElementById('incomingLane');
        container.innerHTML = this.incomingCars.map(car => {
            let carClass = 'car';
            let style = '';
            
            if (car.type === 'vip') {
                style = 'background: linear-gradient(135deg, #f1c40f, #f39c12);';
            } else if (car.type === 'urgent') {
                style = 'background: linear-gradient(135deg, #e74c3c, #c0392b); animation: urgentPulse 0.3s infinite;';
            }
            
            return `<div class="${carClass}" data-id="${car.id}" style="${style}" onclick="game.selectCar(${car.id})">${car.emoji}</div>`;
        }).join('');
    }
    
    renderQueue() {
        const container = document.getElementById('queueSlots');
        container.innerHTML = '';
        
        for (let i = 0; i < this.maxQueueSize; i++) {
            const slot = document.createElement('div');
            slot.className = 'queue-slot';
            
            if (i < this.queue.length) {
                slot.classList.add('filled');
                if (i === 0) slot.classList.add('front');
                
                const car = this.queue[i];
                slot.innerHTML = car.emoji;
                slot.title = `Car #${car.id}`;
            } else {
                slot.innerHTML = '-';
            }
            
            container.appendChild(slot);
        }
        
        document.getElementById('currentSize').textContent = this.queue.length;
        document.getElementById('releaseBtn').disabled = this.queue.length === 0;
    }
    
    selectCar(carId) {
        // Find and enqueue the selected car
        const carIndex = this.incomingCars.findIndex(c => c.id === carId);
        if (carIndex === -1) return;
        
        this.enqueue(this.incomingCars[carIndex]);
        this.incomingCars.splice(carIndex, 1);
        this.renderIncomingCars();
    }
    
    enqueueNextCar() {
        if (this.incomingCars.length === 0) {
            this.showStatus('No cars to enqueue!', 'error');
            return;
        }
        
        this.selectCar(this.incomingCars[0].id);
    }
    
    enqueue(car) {
        if (this.queue.length >= this.maxQueueSize) {
            this.showStatus('Queue Overflow! Lost a life!', 'error');
            this.lives--;
            this.updateDisplay();
            
            // Animate overflow
            document.querySelectorAll('.queue-slot').forEach(slot => {
                slot.classList.add('overflow');
                setTimeout(() => slot.classList.remove('overflow'), 500);
            });
            
            if (this.lives <= 0) {
                this.endGame(false, 'No lives remaining!');
            }
            return;
        }
        
        this.queue.push(car);
        this.score += 5;
        this.showStatus(`Car #${car.id} enqueued!`, 'success');
        this.renderQueue();
        this.updateDisplay();
    }
    
    dequeue() {
        if (this.queue.length === 0) {
            this.showStatus('Queue is empty!', 'error');
            return;
        }
        
        this.releaseCar();
    }
    
    releaseCar() {
        if (this.queue.length === 0) return;
        
        const car = this.queue.shift();
        this.processedCars.push(car);
        this.score += 10;
        
        // Bonus for quick processing
        if (this.config.timeLimit > 0 && this.timeLeft > this.config.timeLimit / 2) {
            this.score += 5;
        }
        
        this.showStatus(`Car #${car.id} released! +10 points`, 'success');
        
        // Show exit animation
        const exitCar = document.getElementById('exitCar');
        exitCar.innerHTML = car.emoji;
        exitCar.classList.remove('hidden');
        setTimeout(() => exitCar.classList.add('hidden'), 500);
        
        this.renderQueue();
        this.updateDisplay();
        
        // Check win condition
        if (this.processedCars.length >= this.carsToProcess) {
            this.endGame(true, 'All cars processed!');
        }
    }
    
    peek() {
        if (this.queue.length === 0) {
            this.showStatus('Queue is empty! Nothing to peek.', 'info');
            return;
        }
        
        const frontCar = this.queue[0];
        this.showStatus(`Front car: #${frontCar.id} ${frontCar.emoji}`, 'info');
    }
    
    showStatus(message, type) {
        const statusEl = document.getElementById('statusMessage');
        statusEl.textContent = message;
        statusEl.className = `status-message ${type}`;
        statusEl.classList.remove('hidden');
        
        setTimeout(() => {
            statusEl.classList.add('hidden');
        }, 2000);
    }
    
    updateDisplay() {
        document.getElementById('levelDisplay').textContent = this.level;
        document.getElementById('scoreDisplay').textContent = this.score;
        document.getElementById('livesDisplay').textContent = '❤️'.repeat(Math.max(0, this.lives));
    }
    
    endGame(success, message) {
        this.gameActive = false;
        clearInterval(this.spawnInterval);
        clearInterval(this.timerInterval);
        
        document.getElementById('gameArea').classList.add('hidden');
        document.getElementById('resultPanel').classList.remove('hidden');
        
        if (success) {
            const xpEarned = 50 + this.score + this.lives * 20;
            
            document.getElementById('resultIcon').textContent = '🎉';
            document.getElementById('resultTitle').textContent = 'Traffic Controlled!';
            document.getElementById('resultText').textContent = message;
            document.getElementById('resultCars').textContent = this.processedCars.length;
            document.getElementById('resultScore').textContent = this.score;
            document.getElementById('resultXP').textContent = `+${xpEarned}`;
            
            this.reportProgress(xpEarned);
        } else {
            document.getElementById('resultIcon').textContent = '💥';
            document.getElementById('resultTitle').textContent = 'System Crash!';
            document.getElementById('resultText').textContent = message;
            document.getElementById('resultCars').textContent = this.processedCars.length;
            document.getElementById('resultScore').textContent = this.score;
            document.getElementById('resultXP').textContent = '+0';
        }
    }
    
    async reportProgress(xpEarned) {
        try {
            if (typeof GameAPI !== 'undefined') {
                const api = new GameAPI();
                await api.updateProgress({
                    username: this.params.username,
                    game_id: 'queue-controller',
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
        this.queue = [];
        this.incomingCars = [];
        this.processedCars = [];
        this.currentCarId = 1;
        this.score = 0;
        this.lives = 3;
        this.maxQueueSize = this.config.maxQueueSize;
        this.carsToProcess = this.config.carsToProcess;
        this.timeLeft = this.config.timeLimit;
        this.gameActive = false;
        
        clearInterval(this.spawnInterval);
        clearInterval(this.timerInterval);
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new QueueTrafficController();
});
