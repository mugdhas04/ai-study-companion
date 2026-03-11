/**
 * Schema Builder - ER Diagram Design Game
 * Build database schemas by creating entities, attributes, and relationships
 */

class SchemaBuilder {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.schemasBuilt = 0;
        this.currentChallenge = null;
        this.elements = [];
        this.selectedElement = null;
        this.selectedTool = null;
        this.connections = [];
        this.elementId = 0;
        
        this.challenges = this.generateChallenges();
        this.challengeIndex = 0;
        
        this.initElements();
        this.bindEvents();
        this.loadChallenge();
    }
    
    initElements() {
        this.scoreEl = document.getElementById('score');
        this.levelEl = document.getElementById('level');
        this.schemasBuiltEl = document.getElementById('schemas-built');
        this.challengeTitle = document.getElementById('challenge-title');
        this.challengeDesc = document.getElementById('challenge-description');
        this.canvas = document.getElementById('canvas');
        this.connectionsEl = document.getElementById('connections');
        this.propertiesPanel = document.getElementById('properties-content');
        this.feedbackEl = document.getElementById('feedback');
        this.modal = document.getElementById('success-modal');
    }
    
    bindEvents() {
        document.querySelectorAll('.tool-btn').forEach(btn => {
            btn.addEventListener('click', () => this.selectTool(btn.dataset.type));
        });
        
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        document.getElementById('check-btn').addEventListener('click', () => this.checkSchema());
        document.getElementById('hint-btn').addEventListener('click', () => this.showHint());
        document.getElementById('clear-btn').addEventListener('click', () => this.clearCanvas());
        document.getElementById('next-btn').addEventListener('click', () => this.nextChallenge());
    }
    
    generateChallenges() {
        return [
            {
                id: 1,
                title: "Simple Student Database",
                description: "Create a STUDENT entity with attributes: StudentID (PK), Name, and Email",
                requirements: {
                    entities: [{ name: "STUDENT", attributes: ["StudentID", "Name", "Email"], pk: "StudentID" }],
                    relationships: []
                },
                hint: "Start by creating a STUDENT entity, then add three attributes. Make StudentID the primary key.",
                xp: 100
            },
            {
                id: 2,
                title: "Student-Course Relationship",
                description: "Create STUDENT and COURSE entities with an 'Enrolls' relationship between them",
                requirements: {
                    entities: [
                        { name: "STUDENT", attributes: ["StudentID", "Name"], pk: "StudentID" },
                        { name: "COURSE", attributes: ["CourseID", "Title"], pk: "CourseID" }
                    ],
                    relationships: [{ name: "Enrolls", between: ["STUDENT", "COURSE"] }]
                },
                hint: "Create both entities with their primary keys, then add an 'Enrolls' relationship to connect them.",
                xp: 150
            },
            {
                id: 3,
                title: "Library Management",
                description: "Design: BOOK (BookID, Title, Author), MEMBER (MemberID, Name), with 'Borrows' relationship",
                requirements: {
                    entities: [
                        { name: "BOOK", attributes: ["BookID", "Title", "Author"], pk: "BookID" },
                        { name: "MEMBER", attributes: ["MemberID", "Name"], pk: "MemberID" }
                    ],
                    relationships: [{ name: "Borrows", between: ["BOOK", "MEMBER"] }]
                },
                hint: "Two entities connected by a Borrows relationship. Don't forget primary keys!",
                xp: 200
            },
            {
                id: 4,
                title: "E-Commerce Order System",
                description: "CUSTOMER, PRODUCT, ORDER entities with relationships: Places (Customer-Order), Contains (Order-Product)",
                requirements: {
                    entities: [
                        { name: "CUSTOMER", attributes: ["CustomerID", "Name"], pk: "CustomerID" },
                        { name: "ORDER", attributes: ["OrderID", "Date"], pk: "OrderID" },
                        { name: "PRODUCT", attributes: ["ProductID", "Name", "Price"], pk: "ProductID" }
                    ],
                    relationships: [
                        { name: "Places", between: ["CUSTOMER", "ORDER"] },
                        { name: "Contains", between: ["ORDER", "PRODUCT"] }
                    ]
                },
                hint: "Three entities, two relationships. Customer places Order, Order contains Product.",
                xp: 250
            }
        ];
    }
    
    loadChallenge() {
        if (this.challengeIndex >= this.challenges.length) {
            this.challengeIndex = 0;
            this.level++;
            this.updateStats();
        }
        
        this.currentChallenge = this.challenges[this.challengeIndex];
        this.challengeTitle.textContent = this.currentChallenge.title;
        this.challengeDesc.textContent = this.currentChallenge.description;
        this.clearCanvas();
        this.hideFeedback();
    }
    
    selectTool(type) {
        document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-type="${type}"]`).classList.add('active');
        this.selectedTool = type;
    }
    
    handleCanvasClick(e) {
        if (e.target !== this.canvas && !e.target.classList.contains('connections')) return;
        if (!this.selectedTool) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left - 60;
        const y = e.clientY - rect.top - 25;
        
        this.createElement(this.selectedTool, x, y);
    }
    
    createElement(type, x, y) {
        const element = document.createElement('div');
        element.className = type === 'primary-key' || type === 'foreign-key' ? `attribute ${type}` : type;
        element.style.left = `${x}px`;
        element.style.top = `${y}px`;
        element.dataset.id = this.elementId++;
        element.dataset.type = type;
        
        switch (type) {
            case 'entity':
                element.textContent = 'ENTITY';
                element.dataset.name = 'ENTITY';
                break;
            case 'attribute':
                element.textContent = 'attr';
                element.dataset.name = 'attr';
                break;
            case 'primary-key':
                element.textContent = '🔑 PK';
                element.dataset.name = 'id';
                break;
            case 'foreign-key':
                element.textContent = '🔗 FK';
                element.dataset.name = 'fk_id';
                break;
            case 'relationship':
                element.innerHTML = '<span>relates</span>';
                element.dataset.name = 'relates';
                break;
        }
        
        this.makeDraggable(element);
        element.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectElement(element);
        });
        element.addEventListener('dblclick', () => this.editElement(element));
        
        this.canvas.appendChild(element);
        this.elements.push(element);
        this.selectElement(element);
    }
    
    makeDraggable(element) {
        let isDragging = false;
        let startX, startY, initialX, initialY;
        
        element.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            initialX = element.offsetLeft;
            initialY = element.offsetTop;
            element.style.zIndex = 1000;
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            element.style.left = `${initialX + dx}px`;
            element.style.top = `${initialY + dy}px`;
            
            this.updateConnections();
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
            element.style.zIndex = '';
        });
    }
    
    selectElement(element) {
        document.querySelectorAll('.entity, .attribute, .relationship').forEach(el => {
            el.classList.remove('selected');
        });
        element.classList.add('selected');
        this.selectedElement = element;
        this.showProperties(element);
    }
    
    showProperties(element) {
        const type = element.dataset.type;
        const name = element.dataset.name;
        
        this.propertiesPanel.innerHTML = `
            <label>Name:</label>
            <input type="text" id="prop-name" value="${name}" placeholder="Enter name">
            <button class="btn btn-primary" style="width:100%; margin-top:10px;" onclick="game.updateElementName()">Update</button>
            <button class="btn btn-danger" style="width:100%; margin-top:10px;" onclick="game.deleteElement()">Delete</button>
        `;
    }
    
    updateElementName() {
        if (!this.selectedElement) return;
        
        const newName = document.getElementById('prop-name').value.toUpperCase();
        this.selectedElement.dataset.name = newName;
        
        if (this.selectedElement.dataset.type === 'relationship') {
            this.selectedElement.innerHTML = `<span>${newName}</span>`;
        } else if (this.selectedElement.dataset.type === 'primary-key') {
            this.selectedElement.textContent = `🔑 ${newName}`;
        } else if (this.selectedElement.dataset.type === 'foreign-key') {
            this.selectedElement.textContent = `🔗 ${newName}`;
        } else {
            this.selectedElement.textContent = newName;
        }
    }
    
    editElement(element) {
        const newName = prompt('Enter name:', element.dataset.name);
        if (newName) {
            element.dataset.name = newName.toUpperCase();
            if (element.dataset.type === 'relationship') {
                element.innerHTML = `<span>${newName.toUpperCase()}</span>`;
            } else if (element.dataset.type === 'primary-key') {
                element.textContent = `🔑 ${newName.toUpperCase()}`;
            } else {
                element.textContent = newName.toUpperCase();
            }
        }
    }
    
    deleteElement() {
        if (!this.selectedElement) return;
        
        this.elements = this.elements.filter(el => el !== this.selectedElement);
        this.selectedElement.remove();
        this.selectedElement = null;
        this.propertiesPanel.innerHTML = '<p class="placeholder">Select an element to edit</p>';
    }
    
    updateConnections() {
        // Simple visual connections would go here
    }
    
    checkSchema() {
        const entities = this.elements.filter(el => el.dataset.type === 'entity');
        const attributes = this.elements.filter(el => 
            el.dataset.type === 'attribute' || 
            el.dataset.type === 'primary-key' || 
            el.dataset.type === 'foreign-key'
        );
        const relationships = this.elements.filter(el => el.dataset.type === 'relationship');
        const primaryKeys = this.elements.filter(el => el.dataset.type === 'primary-key');
        
        const req = this.currentChallenge.requirements;
        
        // Check entities
        const entityNames = entities.map(e => e.dataset.name.toUpperCase());
        const requiredEntities = req.entities.map(e => e.name.toUpperCase());
        
        const hasAllEntities = requiredEntities.every(name => entityNames.includes(name));
        
        // Check primary keys exist
        const hasPrimaryKeys = primaryKeys.length >= req.entities.length;
        
        // Check relationships
        const relationshipNames = relationships.map(r => r.dataset.name.toUpperCase());
        const requiredRelationships = req.relationships.map(r => r.name.toUpperCase());
        const hasAllRelationships = requiredRelationships.every(name => relationshipNames.includes(name));
        
        if (hasAllEntities && hasPrimaryKeys && hasAllRelationships) {
            this.handleSuccess();
        } else {
            let feedback = "Not quite right. ";
            if (!hasAllEntities) feedback += "Check your entities. ";
            if (!hasPrimaryKeys) feedback += "Add primary keys. ";
            if (!hasAllRelationships) feedback += "Add the required relationships. ";
            this.showFeedback(feedback, 'error');
        }
    }
    
    handleSuccess() {
        this.score += this.currentChallenge.xp;
        this.schemasBuilt++;
        this.updateStats();
        
        document.getElementById('xp-earned').textContent = `+${this.currentChallenge.xp} XP`;
        this.modal.classList.add('active');
        
        this.reportScore();
    }
    
    nextChallenge() {
        this.modal.classList.remove('active');
        this.challengeIndex++;
        this.loadChallenge();
    }
    
    showHint() {
        this.showFeedback(`💡 ${this.currentChallenge.hint}`, 'hint');
    }
    
    clearCanvas() {
        this.elements.forEach(el => el.remove());
        this.elements = [];
        this.selectedElement = null;
        this.propertiesPanel.innerHTML = '<p class="placeholder">Select an element to edit</p>';
    }
    
    showFeedback(message, type) {
        this.feedbackEl.textContent = message;
        this.feedbackEl.className = `feedback ${type}`;
    }
    
    hideFeedback() {
        this.feedbackEl.textContent = '';
        this.feedbackEl.className = 'feedback';
    }
    
    updateStats() {
        this.scoreEl.textContent = this.score;
        this.levelEl.textContent = this.level;
        this.schemasBuiltEl.textContent = this.schemasBuilt;
    }
    
    reportScore() {
        if (window.parent !== window) {
            window.parent.postMessage({
                type: 'GAME_SCORE',
                game: 'schema-builder',
                score: this.score,
                level: this.level,
                schemasBuilt: this.schemasBuilt
            }, '*');
        }
    }
}

let game;
document.addEventListener('DOMContentLoaded', () => {
    game = new SchemaBuilder();
});
