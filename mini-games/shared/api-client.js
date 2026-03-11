// Shared API Client for Mini-Games
// Handles communication with the FastAPI backend

class GameAPI {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000';
    }

    /**
     * Update game progress after level completion
     */
    async updateProgress(username, gameId, levelId, xpEarned, score, completed) {
        try {
            const response = await fetch(`${this.API_BASE_URL}/api/progress/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    game_id: gameId,
                    level_id: levelId,
                    xp_earned: xpEarned,
                    score: score,
                    completed: completed
                })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to update progress:', error);
            // Return mock data for offline mode
            return {
                success: true,
                message: 'Progress saved (offline mode)',
                new_xp: xpEarned,
                new_level: 1
            };
        }
    }

    /**
     * Submit quiz results
     */
    async submitQuiz(username, gameId, levelId, correctAnswers, totalQuestions, xpEarned) {
        try {
            const response = await fetch(`${this.API_BASE_URL}/api/quiz/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    game_id: gameId,
                    level_id: levelId,
                    correct_answers: correctAnswers,
                    total_questions: totalQuestions,
                    xp_earned: xpEarned
                })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to submit quiz:', error);
            return {
                success: true,
                message: 'Quiz submitted (offline mode)',
                new_xp: xpEarned,
                new_level: 1
            };
        }
    }

    /**
     * Get user progress
     */
    async getProgress(username) {
        try {
            const response = await fetch(`${this.API_BASE_URL}/api/progress/${username}`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            return data.progress;
        } catch (error) {
            console.error('Failed to fetch progress:', error);
            return null;
        }
    }

    /**
     * Get leaderboard
     */
    async getLeaderboard() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/api/leaderboard`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();
            return data.leaderboard;
        } catch (error) {
            console.error('Failed to fetch leaderboard:', error);
            return [];
        }
    }
}

// Create global instance
window.GameAPI = new GameAPI();

// Helper function to parse URL parameters
window.getGameParams = function() {
    const params = new URLSearchParams(window.location.search);
    return {
        username: params.get('username') || 'guest',
        gameId: params.get('gameId') || 'unknown',
        levelId: parseInt(params.get('levelId')) || 1,
        difficulty: params.get('difficulty') || 'intermediate'
    };
};

// Post message to parent (Streamlit)
window.notifyParent = function(type, data) {
    window.parent.postMessage({
        type: type,
        ...data
    }, '*');
};

console.log('GameAPI initialized');
