document.getElementById('analyze-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const textInput = document.getElementById('contract-text').value;
    const btn = document.getElementById('submit-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    // UI state updates
    btn.disabled = true;
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    
    const formData = new FormData();
    formData.append('text', textInput);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Populate Summary
        document.getElementById('summary-text').innerHTML = `<strong>${data.summary}</strong>`;
        
        // Populate Dependency Tree (simple text representation)
        const treeContainer = document.getElementById('dependency-tree');
        treeContainer.innerHTML = data.dependency_tree.map(node => 
            `{ "word": "${node.word}", "dep": "${node.dep}", "head": "${node.head}" }`
        ).join('<br>');
        
        // Populate Clauses
        const clausesList = document.getElementById('clauses-list');
        clausesList.innerHTML = ''; // clear previous
        
        data.clauses.forEach(item => {
            const card = document.createElement('div');
            card.className = `clause-card risk-${item.risk_level}`;
            
            // Build entities HTML
            const entitiesHtml = item.entities.length > 0 
                ? `<div class="meta-info"><strong>NER Entities:</strong><br> ${item.entities.map(e => `<span class="badge">${e}</span>`).join('')}</div>` 
                : '<div class="meta-info">No specific entities detected.</div>';
                
            card.innerHTML = `
                <div class="clause-text">"${item.clause}"</div>
                <div class="meta-info" style="margin-bottom: 10px;">
                    <strong>Risk Classification:</strong> 
                    <span class="risk-badge-${item.risk_level}">${item.risk_level} Risk</span>
                </div>
                ${entitiesHtml}
            `;
            clausesList.appendChild(card);
        });
        
        results.classList.remove('hidden');
        
    } catch (error) {
        console.error("Error during analysis:", error);
        alert("There was an error analyzing the contract. Check console for details.");
    } finally {
        btn.disabled = false;
        loading.classList.add('hidden');
    }
});
