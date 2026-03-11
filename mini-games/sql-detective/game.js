/**
 * SQL Detective - Database Query Puzzle Game
 * Solve cases by writing correct SQL queries
 */

class SQLDetective {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.streak = 0;
        this.currentCase = null;
        this.cases = this.generateCases();
        this.caseIndex = 0;
        
        this.initElements();
        this.bindEvents();
        this.loadCase();
    }
    
    initElements() {
        this.scoreEl = document.getElementById('score');
        this.levelEl = document.getElementById('level');
        this.streakEl = document.getElementById('streak');
        this.caseTitleEl = document.getElementById('case-title');
        this.caseDescEl = document.getElementById('case-description');
        this.tablesContainer = document.getElementById('tables-container');
        this.queryInput = document.getElementById('query-input');
        this.resultsContainer = document.getElementById('results-container');
        this.feedbackArea = document.getElementById('feedback-area');
        this.modal = document.getElementById('success-modal');
        this.xpEarnedEl = document.getElementById('xp-earned');
    }
    
    bindEvents() {
        document.getElementById('run-query').addEventListener('click', () => this.runQuery());
        document.getElementById('hint-btn').addEventListener('click', () => this.showHint());
        document.getElementById('clear-btn').addEventListener('click', () => this.clearQuery());
        document.getElementById('next-case').addEventListener('click', () => this.nextCase());
        
        // Ctrl+Enter to run query
        this.queryInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.runQuery();
            }
        });
    }
    
    generateCases() {
        return [
            {
                id: 1,
                title: "Case #001: Customer List",
                description: "Welcome, Detective! Your first case is simple. The manager needs a list of all customers in the database. Write a query to SELECT all columns FROM the 'customers' table.",
                tables: {
                    customers: {
                        columns: ['id', 'name', 'email', 'city'],
                        data: [
                            [1, 'Alice Smith', 'alice@email.com', 'New York'],
                            [2, 'Bob Johnson', 'bob@email.com', 'Los Angeles'],
                            [3, 'Carol White', 'carol@email.com', 'Chicago'],
                            [4, 'David Brown', 'david@email.com', 'Houston']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+\*\s+FROM\s+customers\s*;?\s*$/i,
                hint: "Use SELECT * FROM tablename to get all columns from a table.",
                xp: 50
            },
            {
                id: 2,
                title: "Case #002: Find the New Yorkers",
                description: "We need to find all customers who live in 'New York'. Use the WHERE clause to filter the results.",
                tables: {
                    customers: {
                        columns: ['id', 'name', 'email', 'city'],
                        data: [
                            [1, 'Alice Smith', 'alice@email.com', 'New York'],
                            [2, 'Bob Johnson', 'bob@email.com', 'Los Angeles'],
                            [3, 'Carol White', 'carol@email.com', 'New York'],
                            [4, 'David Brown', 'david@email.com', 'Houston'],
                            [5, 'Eve Davis', 'eve@email.com', 'New York']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+\*\s+FROM\s+customers\s+WHERE\s+city\s*=\s*['"]New York['"]\s*;?\s*$/i,
                expectedData: [
                    [1, 'Alice Smith', 'alice@email.com', 'New York'],
                    [3, 'Carol White', 'carol@email.com', 'New York'],
                    [5, 'Eve Davis', 'eve@email.com', 'New York']
                ],
                hint: "Use WHERE column = 'value' to filter rows. Don't forget quotes around text values!",
                xp: 75
            },
            {
                id: 3,
                title: "Case #003: Count the Products",
                description: "The inventory manager needs to know how many products are in the database. Use COUNT() to find the total number of products.",
                tables: {
                    products: {
                        columns: ['id', 'name', 'price', 'category'],
                        data: [
                            [1, 'Laptop', 999.99, 'Electronics'],
                            [2, 'Mouse', 29.99, 'Electronics'],
                            [3, 'Desk', 149.99, 'Furniture'],
                            [4, 'Chair', 199.99, 'Furniture'],
                            [5, 'Monitor', 299.99, 'Electronics'],
                            [6, 'Keyboard', 79.99, 'Electronics']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+COUNT\s*\(\s*\*\s*\)\s+FROM\s+products\s*;?\s*$/i,
                hint: "Use COUNT(*) to count all rows in a table.",
                xp: 100
            },
            {
                id: 4,
                title: "Case #004: Expensive Items",
                description: "Find all products that cost more than $100. We need to identify our premium items.",
                tables: {
                    products: {
                        columns: ['id', 'name', 'price', 'category'],
                        data: [
                            [1, 'Laptop', 999.99, 'Electronics'],
                            [2, 'Mouse', 29.99, 'Electronics'],
                            [3, 'Desk', 149.99, 'Furniture'],
                            [4, 'Chair', 199.99, 'Furniture'],
                            [5, 'Monitor', 299.99, 'Electronics'],
                            [6, 'Keyboard', 79.99, 'Electronics']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+\*\s+FROM\s+products\s+WHERE\s+price\s*>\s*100\s*;?\s*$/i,
                expectedData: [
                    [1, 'Laptop', 999.99, 'Electronics'],
                    [3, 'Desk', 149.99, 'Furniture'],
                    [4, 'Chair', 199.99, 'Furniture'],
                    [5, 'Monitor', 299.99, 'Electronics']
                ],
                hint: "Use comparison operators like > (greater than) with numbers. No quotes needed for numbers!",
                xp: 100
            },
            {
                id: 5,
                title: "Case #005: Order by Price",
                description: "The sales team wants to see all products sorted by price from lowest to highest. Use ORDER BY to sort the results.",
                tables: {
                    products: {
                        columns: ['id', 'name', 'price', 'category'],
                        data: [
                            [1, 'Laptop', 999.99, 'Electronics'],
                            [2, 'Mouse', 29.99, 'Electronics'],
                            [3, 'Desk', 149.99, 'Furniture'],
                            [4, 'Chair', 199.99, 'Furniture'],
                            [5, 'Monitor', 299.99, 'Electronics']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+\*\s+FROM\s+products\s+ORDER\s+BY\s+price(\s+ASC)?\s*;?\s*$/i,
                hint: "Use ORDER BY column to sort results. ASC for ascending (default), DESC for descending.",
                xp: 100
            },
            {
                id: 6,
                title: "Case #006: Specific Columns",
                description: "The marketing team only needs customer names and emails. Select just the 'name' and 'email' columns from customers.",
                tables: {
                    customers: {
                        columns: ['id', 'name', 'email', 'city', 'phone'],
                        data: [
                            [1, 'Alice Smith', 'alice@email.com', 'New York', '555-0101'],
                            [2, 'Bob Johnson', 'bob@email.com', 'LA', '555-0102'],
                            [3, 'Carol White', 'carol@email.com', 'Chicago', '555-0103']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+name\s*,\s*email\s+FROM\s+customers\s*;?\s*$/i,
                hint: "Instead of *, list the specific column names separated by commas.",
                xp: 75
            },
            {
                id: 7,
                title: "Case #007: Electronics Only",
                description: "Count how many products are in the 'Electronics' category.",
                tables: {
                    products: {
                        columns: ['id', 'name', 'price', 'category'],
                        data: [
                            [1, 'Laptop', 999.99, 'Electronics'],
                            [2, 'Mouse', 29.99, 'Electronics'],
                            [3, 'Desk', 149.99, 'Furniture'],
                            [4, 'Chair', 199.99, 'Furniture'],
                            [5, 'Monitor', 299.99, 'Electronics'],
                            [6, 'Keyboard', 79.99, 'Electronics'],
                            [7, 'Lamp', 49.99, 'Furniture']
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+COUNT\s*\(\s*\*\s*\)\s+FROM\s+products\s+WHERE\s+category\s*=\s*['"]Electronics['"]\s*;?\s*$/i,
                hint: "Combine COUNT(*) with WHERE to count specific rows.",
                xp: 125
            },
            {
                id: 8,
                title: "Case #008: Top 3 Expensive",
                description: "Find the top 3 most expensive products. Use ORDER BY and LIMIT.",
                tables: {
                    products: {
                        columns: ['id', 'name', 'price'],
                        data: [
                            [1, 'Laptop', 999.99],
                            [2, 'Mouse', 29.99],
                            [3, 'Desk', 149.99],
                            [4, 'Chair', 199.99],
                            [5, 'Monitor', 299.99],
                            [6, 'Keyboard', 79.99]
                        ]
                    }
                },
                expectedQuery: /^\s*SELECT\s+\*\s+FROM\s+products\s+ORDER\s+BY\s+price\s+DESC\s+LIMIT\s+3\s*;?\s*$/i,
                hint: "Use ORDER BY column DESC for descending order, then LIMIT n to get only n rows.",
                xp: 150
            }
        ];
    }
    
    loadCase() {
        if (this.caseIndex >= this.cases.length) {
            this.caseIndex = 0; // Loop back
            this.level++;
            this.updateStats();
        }
        
        this.currentCase = this.cases[this.caseIndex];
        this.caseTitleEl.textContent = this.currentCase.title;
        this.caseDescEl.textContent = this.currentCase.description;
        this.renderTables();
        this.clearResults();
        this.hideFeedback();
        this.queryInput.value = '';
    }
    
    renderTables() {
        this.tablesContainer.innerHTML = '';
        
        for (const [tableName, tableData] of Object.entries(this.currentCase.tables)) {
            const tableDiv = document.createElement('div');
            tableDiv.className = 'db-table';
            
            const headerHtml = `<div class="table-header">📁 ${tableName}</div>`;
            
            let tableHtml = '<div class="table-content"><table>';
            tableHtml += '<tr>' + tableData.columns.map(col => `<th>${col}</th>`).join('') + '</tr>';
            
            for (const row of tableData.data) {
                tableHtml += '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>';
            }
            
            tableHtml += '</table></div>';
            
            tableDiv.innerHTML = headerHtml + tableHtml;
            this.tablesContainer.appendChild(tableDiv);
        }
    }
    
    runQuery() {
        const query = this.queryInput.value.trim();
        
        if (!query) {
            this.showFeedback('Please enter a SQL query!', 'error');
            return;
        }
        
        // Check if query matches expected pattern
        if (this.currentCase.expectedQuery.test(query)) {
            this.handleCorrectQuery();
        } else {
            // Simulate running the query (basic parsing)
            const result = this.simulateQuery(query);
            if (result.error) {
                this.showFeedback(result.error, 'error');
            } else {
                this.displayResults(result);
                this.showFeedback('Query executed, but this doesn\'t solve the case. Try again!', 'error');
            }
            this.streak = 0;
            this.updateStats();
        }
    }
    
    simulateQuery(query) {
        // Very basic SQL simulation for display purposes
        const upperQuery = query.toUpperCase();
        
        if (!upperQuery.includes('SELECT')) {
            return { error: 'Query must start with SELECT' };
        }
        
        if (!upperQuery.includes('FROM')) {
            return { error: 'Query must include FROM clause' };
        }
        
        // Find the table name
        const fromMatch = query.match(/FROM\s+(\w+)/i);
        if (!fromMatch) {
            return { error: 'Could not parse table name' };
        }
        
        const tableName = fromMatch[1].toLowerCase();
        const tableData = this.currentCase.tables[tableName];
        
        if (!tableData) {
            return { error: `Table '${tableName}' does not exist` };
        }
        
        // Return simulated results
        return {
            columns: tableData.columns,
            data: tableData.data.slice(0, 5) // Show first 5 rows
        };
    }
    
    displayResults(result) {
        if (!result.columns || !result.data) {
            this.resultsContainer.innerHTML = '<p class="placeholder-text">No results</p>';
            return;
        }
        
        let html = '<table>';
        html += '<tr>' + result.columns.map(col => `<th>${col}</th>`).join('') + '</tr>';
        
        for (const row of result.data) {
            html += '<tr>' + row.map(cell => `<td>${cell}</td>`).join('') + '</tr>';
        }
        
        html += '</table>';
        this.resultsContainer.innerHTML = html;
    }
    
    handleCorrectQuery() {
        this.score += this.currentCase.xp;
        this.streak++;
        
        // Bonus for streak
        const streakBonus = this.streak > 1 ? (this.streak - 1) * 10 : 0;
        const totalXp = this.currentCase.xp + streakBonus;
        
        this.updateStats();
        
        // Show expected results
        if (this.currentCase.expectedData) {
            const tableName = Object.keys(this.currentCase.tables)[0];
            this.displayResults({
                columns: this.currentCase.tables[tableName].columns,
                data: this.currentCase.expectedData
            });
        }
        
        // Show success modal
        this.xpEarnedEl.textContent = `+${totalXp} XP`;
        this.modal.classList.add('active');
        
        // Report score to parent app
        this.reportScore();
    }
    
    nextCase() {
        this.modal.classList.remove('active');
        this.caseIndex++;
        this.loadCase();
    }
    
    showHint() {
        this.showFeedback(`💡 Hint: ${this.currentCase.hint}`, 'hint');
    }
    
    clearQuery() {
        this.queryInput.value = '';
        this.clearResults();
        this.hideFeedback();
    }
    
    clearResults() {
        this.resultsContainer.innerHTML = '<p class="placeholder-text">Run a query to see results...</p>';
    }
    
    showFeedback(message, type) {
        this.feedbackArea.textContent = message;
        this.feedbackArea.className = `feedback-area ${type}`;
    }
    
    hideFeedback() {
        this.feedbackArea.className = 'feedback-area';
    }
    
    updateStats() {
        this.scoreEl.textContent = this.score;
        this.levelEl.textContent = this.level;
        this.streakEl.textContent = this.streak;
    }
    
    reportScore() {
        // Report to parent iframe if available
        if (window.parent !== window) {
            window.parent.postMessage({
                type: 'GAME_SCORE',
                game: 'sql-detective',
                score: this.score,
                level: this.level,
                casesCompleted: this.caseIndex + 1
            }, '*');
        }
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new SQLDetective();
});
