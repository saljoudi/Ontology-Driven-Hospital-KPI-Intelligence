// What-If Simulation JavaScript

let currentKPIs = [];
let simulationResults = null;
let comparisonChart = null;
let networkImpactChart = null;
let scenarioHistory = [];

// Initialize simulation page
function initializeSimulationPage() {
    console.log('Initializing What-If Simulation Page...');
    
    // Load KPI data
    loadKPIControls();
    
    // Set up event listeners
    setupSimulationEventListeners();
    
    // Initialize charts
    initializeComparisonChart();
    initializeNetworkImpactChart();
    
    // Load scenario history
    loadScenarioHistory();
}

// Load KPI controls
async function loadKPIControls() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/kpis');
        if (response.ok) {
            const data = await response.json();
            currentKPIs = data.data;
            createKPIControls(currentKPIs);
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Failed to load KPI controls:', error);
        showLoading(false);
    }
}

// Create KPI control sliders
function createKPIControls(kpis) {
    const container = document.getElementById('kpi-controls');
    if (!container) return;
    
    container.innerHTML = '';
    
    kpis.forEach((kpi, index) => {
        const control = createKPISlider(kpi, index);
        container.appendChild(control);
    });
}

// Create KPI slider control
function createKPISlider(kpi, index) {
    const control = document.createElement('div');
    control.className = 'bg-white rounded-lg shadow-sm border border-gray-200 p-4';
    
    const currentValue = kpi.observation.value;
    const targetValue = kpi.target;
    const minValue = Math.max(0, currentValue * 0.5);
    const maxValue = currentValue * 1.5;
    
    control.innerHTML = `
        <div class="mb-4">
            <h3 class="text-sm font-semibold text-gray-900 mb-1">${kpi.label}</h3>
            <div class="flex items-center justify-between text-xs text-gray-500">
                <span>Current: ${currentValue}</span>
                <span>Target: ${targetValue}</span>
            </div>
        </div>
        
        <div class="slider-container mb-2">
            <input type="range" 
                   id="slider-${index}" 
                   class="slider" 
                   min="${minValue}" 
                   max="${maxValue}" 
                   value="${currentValue}" 
                   step="${getSliderStep(kpi.unit)}">
        </div>
        
        <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">${kpi.unit}</span>
            <span id="value-${index}" class="text-sm font-medium text-blue-600">${currentValue}</span>
        </div>
    `;
    
    // Add slider event listener
    const slider = control.querySelector(`#slider-${index}`);
    const valueDisplay = control.querySelector(`#value-${index}`);
    
    slider.addEventListener('input', function() {
        valueDisplay.textContent = parseFloat(this.value).toFixed(1);
        updateSliderColor(this, currentValue);
    });
    
    return control;
}

// Get appropriate slider step based on unit
function getSliderStep(unit) {
    switch (unit) {
        case 'percentage':
            return 0.1;
        case 'minutes':
        case 'hours':
            return 1;
        case 'days':
            return 0.1;
        default:
            return 0.1;
    }
}

// Update slider color based on value change
function updateSliderColor(slider, originalValue) {
    const currentValue = parseFloat(slider.value);
    const changePercent = ((currentValue - originalValue) / originalValue) * 100;
    
    if (changePercent > 5) {
        slider.style.background = 'linear-gradient(to right, #e2e8f0 0%, #dcfce7 100%)';
    } else if (changePercent < -5) {
        slider.style.background = 'linear-gradient(to right, #e2e8f0 0%, #fee2e2 100%)';
    } else {
        slider.style.background = '#e2e8f0';
    }
}

// Set up simulation event listeners
function setupSimulationEventListeners() {
    // Run simulation button
    const runBtn = document.getElementById('run-simulation');
    if (runBtn) {
        runBtn.addEventListener('click', runSimulation);
    }
    
    // Reset simulation button
    const resetBtn = document.getElementById('reset-simulation');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetSimulation);
    }
    
    // Save scenario button
    const saveBtn = document.getElementById('save-scenario');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveScenario);
    }
    
    // Chart type buttons
    const chartButtons = ['chart-type-bar', 'chart-type-line', 'chart-type-radar'];
    chartButtons.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', () => changeChartType(id.replace('chart-type-', '')));
        }
    });
    
    // Modal close button
    const closeModalBtn = document.getElementById('close-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', hideSuccessModal);
    }
}

// Run simulation
async function runSimulation() {
    try {
        showLoading(true);
        
        // Collect current slider values
        const changes = {};
        currentKPIs.forEach((kpi, index) => {
            const slider = document.getElementById(`slider-${index}`);
            if (slider) {
                const newValue = parseFloat(slider.value);
                if (Math.abs(newValue - kpi.observation.value) > 0.1) {
                    changes[kpi.uri] = newValue;
                }
            }
        });
        
        if (Object.keys(changes).length === 0) {
            showNotification('Please adjust at least one KPI value', 'warning');
            showLoading(false);
            return;
        }
        
        // Send simulation request
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ changes: changes })
        });
        
        if (response.ok) {
            const data = await response.json();
            simulationResults = data.data;
            
            // Update UI with results
            updateImpactResults(simulationResults);
            updateImpactSummary(simulationResults);
            updateComparisonChart(simulationResults);
            updateNetworkImpactVisualization(simulationResults);
            updateSimulationRecommendations(simulationResults);
            
            // Add to scenario history
            addToScenarioHistory(changes, simulationResults);
            
            showSuccessModal();
            showNotification('Simulation completed successfully', 'success');
        } else {
            showNotification('Failed to run simulation', 'error');
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Simulation error:', error);
        showNotification('Simulation error: ' + error.message, 'error');
        showLoading(false);
    }
}

// Reset simulation
function resetSimulation() {
    currentKPIs.forEach((kpi, index) => {
        const slider = document.getElementById(`slider-${index}`);
        const valueDisplay = document.getElementById(`value-${index}`);
        
        if (slider) {
            slider.value = kpi.observation.value;
            updateSliderColor(slider, kpi.observation.value);
        }
        
        if (valueDisplay) {
            valueDisplay.textContent = kpi.observation.value;
        }
    });
    
    // Clear results
    clearSimulationResults();
    showNotification('Simulation reset to original values', 'info');
}

// Save scenario
function saveScenario() {
    if (!simulationResults) {
        showNotification('No simulation results to save', 'warning');
        return;
    }
    
    const scenarioName = prompt('Enter a name for this scenario:');
    if (!scenarioName) return;
    
    const scenario = {
        name: scenarioName,
        timestamp: new Date().toISOString(),
        changes: simulationResults.changes,
        impact_score: simulationResults.overall_impact_score,
        results: simulationResults
    };
    
    scenarioHistory.unshift(scenario);
    if (scenarioHistory.length > 10) {
        scenarioHistory = scenarioHistory.slice(0, 10);
    }
    
    updateScenarioHistory();
    showNotification(`Scenario "${scenarioName}" saved successfully`, 'success');
}

// Update impact results
function updateImpactResults(results) {
    const container = document.getElementById('impact-results');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Show direct impacts
    Object.entries(results.impacts).forEach(([kpiUri, impact]) => {
        const card = createImpactCard(impact, 'direct');
        container.appendChild(card);
    });
    
    // Show propagated impacts
    if (results.predicted_outcomes && results.predicted_outcomes.length > 0) {
        const propagatedHeader = document.createElement('h3');
        propagatedHeader.className = 'text-lg font-semibold text-gray-900 mt-6 mb-4';
        propagatedHeader.textContent = 'Propagated Impacts';
        container.appendChild(propagatedHeader);
        
        results.predicted_outcomes.forEach(outcome => {
            const card = createPropagatedImpactCard(outcome);
            container.appendChild(card);
        });
    }
    
    // Animate results
    anime({
        targets: '.impact-card',
        translateX: [-50, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 500,
        easing: 'easeOutQuart'
    });
}

// Create impact card
function createImpactCard(impact, type) {
    const card = document.createElement('div');
    card.className = 'impact-card simulation-card rounded-lg p-4 mb-4';
    
    const changePercent = impact.change_percent;
    const impactClass = changePercent > 0 ? 'impact-positive' : 
                       changePercent < 0 ? 'impact-negative' : 'impact-neutral';
    
    card.classList.add(impactClass);
    
    const changeIndicator = changePercent > 0 ? '📈' : 
                           changePercent < 0 ? '📉' : '➡️';
    
    card.innerHTML = `
        <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-gray-900">${impact.kpi.label}</h3>
            <span class="text-lg">${changeIndicator}</span>
        </div>
        
        <div class="before-after mb-3">
            <div class="text-center">
                <div class="text-xs text-gray-500 mb-1">Before</div>
                <div class="text-lg font-bold text-gray-900">${impact.kpi.current_value}</div>
            </div>
            <div class="text-center">
                <div class="text-xs text-gray-500 mb-1">After</div>
                <div class="text-lg font-bold text-blue-600">${impact.new_value}</div>
            </div>
        </div>
        
        <div class="flex items-center justify-between">
            <span class="change-indicator ${getChangeClass(changePercent)}">
                ${changePercent > 0 ? '+' : ''}${changePercent.toFixed(1)}%
            </span>
            <span class="text-xs text-gray-500">${impact.kpi.unit}</span>
        </div>
        
        ${impact.explanation ? `
            <div class="mt-3 p-3 bg-blue-50 rounded-lg">
                <p class="text-xs text-blue-800">${impact.explanation}</p>
            </div>
        ` : ''}
    `;
    
    return card;
}

// Create propagated impact card
function createPropagatedImpactCard(outcome) {
    const card = document.createElement('div');
    card.className = 'impact-card simulation-card rounded-lg p-4 mb-4 impact-propagated';
    
    const changeAmount = outcome.change_amount;
    const impactClass = changeAmount > 0 ? 'impact-positive' : 'impact-negative';
    card.classList.add(impactClass);
    
    card.innerHTML = `
        <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-semibold text-gray-900">${outcome.kpi_label}</h3>
            <span class="text-xs px-2 py-1 bg-purple-100 text-purple-800 rounded">
                ${outcome.relationship_type}
            </span>
        </div>
        
        <div class="before-after mb-3">
            <div class="text-center">
                <div class="text-xs text-gray-500 mb-1">Original</div>
                <div class="text-lg font-bold text-gray-900">${outcome.original_value.toFixed(1)}</div>
            </div>
            <div class="text-center">
                <div class="text-xs text-gray-500 mb-1">Projected</div>
                <div class="text-lg font-bold text-purple-600">${outcome.projected_value.toFixed(1)}</div>
            </div>
        </div>
        
        <div class="text-xs text-gray-500">
            Influenced by: ${outcome.influenced_by.split('#').pop()}
        </div>
    `;
    
    return card;
}

// Get change class
function getChangeClass(changePercent) {
    if (changePercent > 5) return 'change-positive';
    if (changePercent < -5) return 'change-negative';
    return 'change-neutral';
}

// Update impact summary
function updateImpactSummary(results) {
    const container = document.getElementById('impact-summary');
    if (!container) return;
    
    const affectedKPIs = Object.keys(results.impacts).length;
    const propagatedKPIs = results.predicted_outcomes ? results.predicted_outcomes.length : 0;
    const totalImpact = results.overall_impact_score;
    
    container.innerHTML = `
        <div class="text-center mb-4">
            <div class="text-3xl font-bold text-blue-600">${affectedKPIs + propagatedKPIs}</div>
            <div class="text-sm text-gray-600">Total KPIs Affected</div>
        </div>
        
        <div class="space-y-3">
            <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Direct Changes</span>
                <span class="text-sm font-medium">${affectedKPIs}</span>
            </div>
            <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Propagated Effects</span>
                <span class="text-sm font-medium">${propagatedKPIs}</span>
            </div>
            <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Overall Impact</span>
                <span class="text-sm font-medium text-blue-600">${totalImpact.toFixed(2)}</span>
            </div>
        </div>
        
        <div class="mt-4 pt-4 border-t border-gray-200">
            <div class="text-xs text-gray-500 text-center">
                Simulation completed at<br/>${new Date().toLocaleString()}
            </div>
        </div>
    `;
}

// Initialize comparison chart
function initializeComparisonChart() {
    const container = document.getElementById('comparison-chart');
    if (!container) return;
    
    comparisonChart = echarts.init(container);
}

// Update comparison chart
function updateComparisonChart(results) {
    if (!comparisonChart || !results) return;
    
    const kpiNames = [];
    const originalValues = [];
    const newValues = [];
    
    // Add direct changes
    Object.values(results.impacts).forEach(impact => {
        kpiNames.push(impact.kpi.label);
        originalValues.push(impact.kpi.current_value);
        newValues.push(impact.new_value);
    });
    
    // Add propagated changes
    if (results.predicted_outcomes) {
        results.predicted_outcomes.forEach(outcome => {
            kpiNames.push(outcome.kpi_label);
            originalValues.push(outcome.original_value);
            newValues.push(outcome.projected_value);
        });
    }
    
    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: ['Original', 'After Changes']
        },
        xAxis: {
            type: 'category',
            data: kpiNames,
            axisLabel: {
                rotate: 45,
                fontSize: 10
            }
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'Original',
                type: 'bar',
                data: originalValues,
                itemStyle: {
                    color: '#64748b'
                }
            },
            {
                name: 'After Changes',
                type: 'bar',
                data: newValues,
                itemStyle: {
                    color: '#2563eb'
                }
            }
        ]
    };
    
    comparisonChart.setOption(option);
}

// Initialize network impact visualization
function initializeNetworkImpactChart() {
    const container = document.getElementById('network-impact');
    if (!container) return;
    
    networkImpactChart = echarts.init(container);
}

// Update network impact visualization
function updateNetworkImpactVisualization(results) {
    if (!networkImpactChart || !results) return;
    
    // Create network data showing affected KPIs
    const nodes = [];
    const edges = [];
    
    // Add changed KPIs as central nodes
    Object.values(results.impacts).forEach((impact, index) => {
        nodes.push({
            id: impact.kpi.label,
            name: impact.kpi.label,
            symbolSize: 30,
            itemStyle: {
                color: '#dc2626'
            }
        });
    });
    
    // Add affected KPIs
    if (results.predicted_outcomes) {
        results.predicted_outcomes.forEach(outcome => {
            nodes.push({
                id: outcome.kpi_label,
                name: outcome.kpi_label,
                symbolSize: 20,
                itemStyle: {
                    color: '#f59e0b'
                }
            });
            
            edges.push({
                source: outcome.influenced_by.split('#').pop(),
                target: outcome.kpi_label,
                lineStyle: {
                    color: '#f59e0b',
                    width: 2
                }
            });
        });
    }
    
    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'item'
        },
        series: [{
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: edges,
            roam: true,
            force: {
                repulsion: 200,
                gravity: 0.1,
                edgeLength: 100
            }
        }]
    };
    
    networkImpactChart.setOption(option);
}

// Update simulation recommendations
function updateSimulationRecommendations(results) {
    const container = document.getElementById('simulation-recommendations');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Generate recommendations based on results
    const recommendations = generateSimulationRecommendations(results);
    
    recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-sm border border-gray-200 p-4';
        
        card.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="flex-shrink-0 text-2xl">${rec.icon}</div>
                <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-semibold text-gray-900 mb-2">${rec.title}</h3>
                    <p class="text-xs text-gray-600 mb-2">${rec.description}</p>
                    <div class="text-xs text-blue-600 font-medium">
                        Priority: ${rec.priority}
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
    
    // Animate recommendations
    anime({
        targets: '#simulation-recommendations .bg-white',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 500,
        easing: 'easeOutQuart'
    });
}

// Generate simulation recommendations
function generateSimulationRecommendations(results) {
    const recommendations = [];
    
    // Analyze impact patterns
    const highImpactChanges = Object.values(results.impacts).filter(impact => 
        Math.abs(impact.change_percent) > 20
    );
    
    if (highImpactChanges.length > 0) {
        recommendations.push({
            icon: '🚨',
            title: 'High-Impact Changes Detected',
            description: `${highImpactChanges.length} KPIs show significant changes (>20%). Monitor these closely.`,
            priority: 'High'
        });
    }
    
    // Check for negative impacts
    const negativeImpacts = Object.values(results.impacts).filter(impact => 
        impact.change_percent < -10
    );
    
    if (negativeImpacts.length > 0) {
        recommendations.push({
            icon: '⚠️',
            title: 'Negative Performance Impact',
            description: `${negativeImpacts.length} KPIs show negative changes. Consider mitigation strategies.`,
            priority: 'High'
        });
    }
    
    // Check for propagated effects
    if (results.predicted_outcomes && results.predicted_outcomes.length > 0) {
        recommendations.push({
            icon: '🔄',
            title: 'Cascade Effects Identified',
            description: `Changes affect ${results.predicted_outcomes.length} additional KPIs through causal relationships.`,
            priority: 'Medium'
        });
    }
    
    // Add optimization recommendation
    if (results.overall_impact_score < 5) {
        recommendations.push({
            icon: '⚡',
            title: 'Optimization Opportunity',
            description: 'Low overall impact suggests room for more aggressive improvements.',
            priority: 'Medium'
        });
    }
    
    return recommendations;
}

// Change chart type
function changeChartType(type) {
    if (!comparisonChart || !simulationResults) return;
    
    // Update button states
    document.querySelectorAll('[id^="chart-type-"]').forEach(btn => {
        btn.className = 'px-3 py-1 bg-gray-100 text-gray-700 rounded text-sm hover:bg-gray-200';
    });
    
    const activeBtn = document.getElementById(`chart-type-${type}`);
    if (activeBtn) {
        activeBtn.className = 'px-3 py-1 bg-blue-600 text-white rounded text-sm';
    }
    
    // Update chart
    updateComparisonChart(simulationResults, type);
}

// Load scenario history
function loadScenarioHistory() {
    // In a real application, this would load from storage
    updateScenarioHistory();
}

// Update scenario history
function updateScenarioHistory() {
    const container = document.getElementById('scenario-history');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (scenarioHistory.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4 text-gray-500">
                <div class="text-2xl mb-2">📊</div>
                <p class="text-xs">No saved scenarios</p>
            </div>
        `;
        return;
    }
    
    scenarioHistory.forEach((scenario, index) => {
        const item = document.createElement('div');
        item.className = 'bg-gray-50 rounded-lg p-3 cursor-pointer hover:bg-gray-100 transition-colors';
        
        const changeCount = Object.keys(scenario.changes).length;
        
        item.innerHTML = `
            <div class="flex items-center justify-between mb-2">
                <h4 class="text-sm font-medium text-gray-900 truncate">${scenario.name}</h4>
                <button class="text-xs text-red-600 hover:text-red-800" onclick="deleteScenario(${index})">Delete</button>
            </div>
            <div class="text-xs text-gray-600 mb-1">
                ${changeCount} KPI${changeCount !== 1 ? 's' : ''} changed
            </div>
            <div class="text-xs text-gray-500">
                ${new Date(scenario.timestamp).toLocaleString()}
            </div>
        `;
        
        item.addEventListener('click', () => loadScenario(scenario));
        
        container.appendChild(item);
    });
}

// Add to scenario history
function addToScenarioHistory(changes, results) {
    const scenario = {
        name: `Scenario ${scenarioHistory.length + 1}`,
        timestamp: new Date().toISOString(),
        changes: changes,
        impact_score: results.overall_impact_score,
        results: results
    };
    
    scenarioHistory.unshift(scenario);
    if (scenarioHistory.length > 10) {
        scenarioHistory = scenarioHistory.slice(0, 10);
    }
    
    updateScenarioHistory();
}

// Load scenario
function loadScenario(scenario) {
    // Reset all sliders first
    resetSimulation();
    
    // Apply scenario changes
    Object.entries(scenario.changes).forEach(([kpiUri, value]) => {
        const kpiIndex = currentKPIs.findIndex(kpi => kpi.uri === kpiUri);
        if (kpiIndex !== -1) {
            const slider = document.getElementById(`slider-${kpiIndex}`);
            const valueDisplay = document.getElementById(`value-${kpiIndex}`);
            
            if (slider) {
                slider.value = value;
                updateSliderColor(slider, currentKPIs[kpiIndex].observation.value);
            }
            
            if (valueDisplay) {
                valueDisplay.textContent = parseFloat(value).toFixed(1);
            }
        }
    });
    
    showNotification(`Loaded scenario: ${scenario.name}`, 'info');
}

// Delete scenario
function deleteScenario(index) {
    if (confirm('Are you sure you want to delete this scenario?')) {
        scenarioHistory.splice(index, 1);
        updateScenarioHistory();
        showNotification('Scenario deleted', 'info');
    }
}

// Clear simulation results
function clearSimulationResults() {
    simulationResults = null;
    
    const containers = [
        'impact-results',
        'impact-summary', 
        'simulation-recommendations'
    ];
    
    containers.forEach(id => {
        const container = document.getElementById(id);
        if (container) {
            container.innerHTML = '';
        }
    });
    
    if (comparisonChart) {
        comparisonChart.clear();
    }
    
    if (networkImpactChart) {
        networkImpactChart.clear();
    }
}

// Show success modal
function showSuccessModal() {
    const modal = document.getElementById('success-modal');
    if (modal) {
        modal.classList.remove('hidden');
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            hideSuccessModal();
        }, 3000);
    }
}

// Hide success modal
function hideSuccessModal() {
    const modal = document.getElementById('success-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}