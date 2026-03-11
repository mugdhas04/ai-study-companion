/**
 * Equation Shooter - Math Practice Game
 * Solve equations by shooting the correct answers
 */

class EquationShooter {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.lives = 3;
        this.timer = 30;
        this.problemsSolved = 0;
        this.currentAnswer = 0;
        this.timerInterval = null;
        this.isGameOver = false;
        
        this.initElements();
        this.bindEvents();
        this.startGame();
    }
    
    initElements() {
        this.scoreEl = document.getElementById('score');
        this.levelEl = document.getElementById('level');
        this.livesEl = document.getElementById('lives');
        this.timerEl = document.getElementById('timer');
        this.equationEl = document.getElementById('equation');
        this.targetsContainer = document.getElementById('targets-container');
        this.answerInput = document.getElementById('answer-input');
        this.feedbackEl = document.getElementById('feedback');
        this.modal = document.getElementById('game-over-modal');
        this.modalTitle = document.getElementById('modal-title');
        this.modalMessage = document.getElementById('modal-message');
        this.finalScoreEl = document.getElementById('final-score');
        this.problemsSolvedEl = document.getElementById('problems-solved');
    }
    
    bindEvents() {
        document.getElementById('shoot-btn').addEventListener('click', () => this.shoot());
        document.getElementById('restart-btn').addEventListener('click', () => this.restart());
        
        this.answerInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.shoot();
            }
        });
    }
    
    startGame() {
        this.generateProblem();
        this.startTimer();
        this.answerInput.focus();
    }
    
    startTimer() {
        this.timerInterval = setInterval(() => {
            this.timer--;
            this.timerEl.textContent = this.timer;
            
            if (this.timer <= 10) {
                this.timerEl.style.color = '#ff6b6b';
            }
            
            if (this.timer <= 0) {
                this.loseLife();
                this.resetTimer();
            }
        }, 1000);
    }
    
    resetTimer() {
        this.timer = Math.max(15, 30 - (this.level - 1) * 3); // Gets harder each level
        this.timerEl.textContent = this.timer;
        this.timerEl.style.color = '#00ff88';
    }
    
    generateProblem() {
        const operators = ['+', '-', '*'];
        let a, b, operator, answer;
        
        // Difficulty scaling based on level
        const maxNum = Math.min(10 + this.level * 5, 50);
        
        if (this.level <= 2) {
            // Easy: addition and subtraction only
            operator = operators[Math.floor(Math.random() * 2)];
            a = Math.floor(Math.random() * maxNum) + 1;
            b = Math.floor(Math.random() * maxNum) + 1;
        } else if (this.level <= 4) {
            // Medium: include multiplication with smaller numbers
            operator = operators[Math.floor(Math.random() * 3)];
            if (operator === '*') {
                a = Math.floor(Math.random() * 12) + 1;
                b = Math.floor(Math.random() * 12) + 1;
            } else {
                a = Math.floor(Math.random() * maxNum) + 1;
                b = Math.floor(Math.random() * maxNum) + 1;
            }
        } else {
            // Hard: all operations with larger numbers
            operator = operators[Math.floor(Math.random() * 3)];
            a = Math.floor(Math.random() * maxNum) + 1;
            b = Math.floor(Math.random() * maxNum) + 1;
        }
        
        // Ensure subtraction doesn't go negative
        if (operator === '-' && b > a) {
            [a, b] = [b, a];
        }
        
        switch (operator) {
            case '+': answer = a + b; break;
            case '-': answer = a - b; break;
            case '*': answer = a * b; break;
        }
        
        this.currentAnswer = answer;
        this.equationEl.textContent = `${a} ${operator} ${b} = ?`;
        
        this.generateTargets(answer);
    }
    
    generateTargets(correctAnswer) {
        this.targetsContainer.innerHTML = '';
        
        // Generate wrong answers
        const answers = [correctAnswer];
        while (answers.length < 5) {
            let wrong;
            const variation = Math.floor(Math.random() * 20) - 10;
            wrong = correctAnswer + variation;
            
            // Ensure unique and reasonable answers
            if (wrong !== correctAnswer && wrong >= 0 && !answers.includes(wrong)) {
                answers.push(wrong);
            }
        }
        
        // Shuffle answers
        answers.sort(() => Math.random() - 0.5);
        
        // Create target elements
        const containerRect = this.targetsContainer.getBoundingClientRect();
        
        answers.forEach((answer, index) => {
            const target = document.createElement('div');
            target.className = 'target';
            target.textContent = answer;
            target.dataset.answer = answer;
            
            // Random position
            const maxX = containerRect.width - 80;
            const maxY = containerRect.height - 60;
            const x = Math.random() * maxX;
            const y = Math.random() * maxY;
            
            target.style.left = `${x}px`;
            target.style.top = `${y}px`;
            target.style.animationDelay = `${index * 0.2}s`;
            
            target.addEventListener('click', () => this.clickTarget(target, answer));
            
            this.targetsContainer.appendChild(target);
        });
    }
    
    clickTarget(target, answer) {
        if (this.isGameOver) return;
        
        if (answer === this.currentAnswer) {
            this.handleCorrect(target);
        } else {
            this.handleWrong(target);
        }
    }
    
    shoot() {
        if (this.isGameOver) return;
        
        const answer = parseInt(this.answerInput.value);
        
        if (isNaN(answer)) {
            this.showFeedback('Enter a number!', 'wrong');
            return;
        }
        
        // Find the target with this answer
        const targets = this.targetsContainer.querySelectorAll('.target');
        let targetFound = null;
        
        targets.forEach(target => {
            if (parseInt(target.dataset.answer) === answer) {
                targetFound = target;
            }
        });
        
        if (answer === this.currentAnswer) {
            this.handleCorrect(targetFound);
        } else {
            this.handleWrong(targetFound);
        }
        
        this.answerInput.value = '';
        this.answerInput.focus();
    }
    
    handleCorrect(target) {
        this.score += 10 * this.level;
        this.problemsSolved++;
        
        // Level up every 5 problems
        if (this.problemsSolved % 5 === 0) {
            this.level++;
            this.showFeedback(`Level ${this.level}! +${10 * this.level} pts per answer`, 'correct');
        } else {
            this.showFeedback(`Correct! +${10 * this.level}`, 'correct');
        }
        
        if (target) {
            target.classList.add('correct', 'explode');
        }
        
        this.updateStats();
        this.resetTimer();
        
        setTimeout(() => {
            this.generateProblem();
        }, 500);
    }
    
    handleWrong(target) {
        this.showFeedback(`Wrong! The answer was ${this.currentAnswer}`, 'wrong');
        
        if (target) {
            target.classList.add('wrong');
        }
        
        this.loseLife();
    }
    
    loseLife() {
        this.lives--;
        this.updateStats();
        
        if (this.lives <= 0) {
            this.gameOver();
        } else {
            this.resetTimer();
            setTimeout(() => {
                this.generateProblem();
            }, 1000);
        }
    }
    
    showFeedback(message, type) {
        this.feedbackEl.textContent = message;
        this.feedbackEl.className = `feedback ${type}`;
        
        setTimeout(() => {
            this.feedbackEl.textContent = '';
            this.feedbackEl.className = 'feedback';
        }, 2000);
    }
    
    updateStats() {
        this.scoreEl.textContent = this.score;
        this.levelEl.textContent = this.level;
        this.livesEl.textContent = '❤️'.repeat(this.lives);
    }
    
    gameOver() {
        this.isGameOver = true;
        clearInterval(this.timerInterval);
        
        if (this.problemsSolved >= 10) {
            this.modalTitle.textContent = '🎉 Great Job!';
            this.modalTitle.className = 'win';
            this.modalMessage.textContent = 'You\'re a math champion!';
        } else {
            this.modalTitle.textContent = '💥 Game Over';
            this.modalTitle.className = 'lose';
            this.modalMessage.textContent = 'Keep practicing to improve!';
        }
        
        this.finalScoreEl.textContent = this.score;
        this.problemsSolvedEl.textContent = this.problemsSolved;
        this.modal.classList.add('active');
        
        this.reportScore();
    }
    
    restart() {
        this.score = 0;
        this.level = 1;
        this.lives = 3;
        this.timer = 30;
        this.problemsSolved = 0;
        this.isGameOver = false;
        
        this.modal.classList.remove('active');
        this.updateStats();
        this.startGame();
    }
    
    reportScore() {
        if (window.parent !== window) {
            window.parent.postMessage({
                type: 'GAME_SCORE',
                game: 'equation-shooter',
                score: this.score,
                level: this.level,
                problemsSolved: this.problemsSolved
            }, '*');
        }
    }
}

// Initialize game
document.addEventListener('DOMContentLoaded', () => {
    new EquationShooter();
});
