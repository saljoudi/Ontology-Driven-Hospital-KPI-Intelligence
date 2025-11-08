// Hospital KPI Intelligence Dashboard JavaScript

let socket = null;
let networkChart = null;
let currentKPIs = [];
let currentInsights = [];
let isRealtimeActive = false;

// Initialize dashboard
function initializeDashboard() {
    console.log('Initializing Hospital KPI Dashboard...');
    
    // Initialize WebSocket connection
    initializeWebSocket();
    
    // Load initial data
    loadDashboardData();
    
    // Set up event listeners
    setupEventListeners();
    
    // Start periodic updates
    startPeriodicUpdates();
}

// Initialize WebSocket connection for real-time updates
function initializeWebSocket() {
    try {
        socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to real-time updates');
            updateConnectionStatus(true);
        });
        
        socket.on('disconnect', function() {
            console.log('Disconnected from real-time updates');
            updateConnectionStatus(false);
        });
        
        socket.on('kpi_update', function(data) {
            updateKPICards(data.kpis);
        });
        
        socket.on('insights_update', function(data) {
            updateInsightsPanel(data.insights);
        });
        
        socket.on('graph_update', function(data) {
            updateNetworkGraph(data.graph_data);
        });
        
        socket.on('error', function(data) {
            console.error('WebSocket error:', data.message);
            showNotification('Connection error: ' + data.message, 'error');
        });
        
    } catch (error) {
        console.error('Failed to initialize WebSocket:', error);
        updateConnectionStatus(false);
    }
}

// Load initial dashboard data
async function loadDashboardData() {
    try {
        showLoading(true);
        
        // Load KPIs
        const kpiResponse = await fetch('/api/kpis');
        if (kpiResponse.ok) {
            const kpiData = await kpiResponse.json();
            currentKPIs = kpiData.data;
            updateKPICards(currentKPIs);
        }
        
        // Load insights
        const insightsResponse = await fetch('/api/insights');
        if (insightsResponse.ok) {
            const insightsData = await insightsResponse.json();
            currentInsights = insightsData.data.insights;
            updateInsightsPanel(currentInsights);
        }
        
        // Load network graph
        const graphResponse = await fetch('/api/graph');
        if (graphResponse.ok) {
            const graphData = await graphResponse.json();
            updateNetworkGraph(graphData.data);
        }
        
        // Load strategic goals
        const goalsResponse = await fetch('/api/strategic-goals');
        if (goalsResponse.ok) {
            const goalsData = await goalsResponse.json();
            updateStrategicGoals(goalsData.data);
        }
        
        updateLastUpdated();
        showLoading(false);
        
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showNotification('Failed to load dashboard data', 'error');
        showLoading(false);
    }
}

// Set up event listeners
function setupEventListeners() {
    // Real-time controls
    const startRealtimeBtn = document.getElementById('start-realtime');
    const runAnalysisBtn = document.getElementById('run-analysis');
    
    if (startRealtimeBtn) {
        startRealtimeBtn.addEventListener('click', toggleRealtimeUpdates);
    }
    
    if (runAnalysisBtn) {
        runAnalysisBtn.addEventListener('click', runAnalysis);
    }
    
    // Network graph controls
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const centerGraphBtn = document.getElementById('center-graph');
    
    if (zoomInBtn) zoomInBtn.addEventListener('click', () => zoomNetworkGraph(1.2));
    if (zoomOutBtn) zoomOutBtn.addEventListener('click', () => zoomNetworkGraph(0.8));
    if (centerGraphBtn) centerGraphBtn.addEventListener('click', centerNetworkGraph);
}

// Update KPI cards
function updateKPICards(kpis) {
    const container = document.getElementById('kpi-cards');
    if (!container) return;
    
    container.innerHTML = '';
    
    kpis.forEach((kpi, index) => {
        const card = createKPICard(kpi, index);
        container.appendChild(card);
    });
    
    // Animate cards
    anime({
        targets: '.kpi-card',
        translateY: [20, 0],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 500,
        easing: 'easeOutQuart'
    });
}

// Create KPI card element
function createKPICard(kpi, index) {
    const card = document.createElement('div');
    card.className = `kpi-card bg-white rounded-lg shadow-sm border border-gray-200 p-6 status-${kpi.observation.status} fade-in`;
    
    const performanceRatio = (kpi.observation.value / kpi.target) * 100;
    const trendIcon = getTrendIcon(kpi.trend || 'stable');
    const statusColor = getStatusColor(kpi.observation.status);
    
    card.innerHTML = `
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 truncate">${kpi.label}</h3>
            <div class="flex items-center space-x-1">
                <span class="text-xs text-gray-500">${kpi.unit}</span>
                ${trendIcon}
            </div>
        </div>
        
        <div class="mb-4">
            <div class="flex items-baseline space-x-2 mb-2">
                <span class="text-3xl font-bold ${statusColor}">${kpi.observation.value}</span>
                <span class="text-sm text-gray-500">/ ${kpi.target}</span>
            </div>
            <div class="text-sm text-gray-600">
                Performance: <span class="font-medium">${performanceRatio.toFixed(1)}%</span>
            </div>
        </div>
        
        <div class="mb-4">
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="h-2 rounded-full transition-all duration-500" 
                     style="width: ${Math.min(100, performanceRatio)}%; background-color: ${getStatusBackground(kpi.observation.status)}"></div>
            </div>
        </div>
        
        <div class="flex items-center justify-between text-xs text-gray-500">
            <span>Status: <span class="font-medium ${statusColor}">${kpi.observation.status.toUpperCase()}</span></span>
            <span>${new Date(kpi.observation.timestamp).toLocaleTimeString()}</span>
        </div>
    `;
    
    // Add click handler for drill-down
    card.addEventListener('click', () => showKPIDetails(kpi));
    
    return card;
}

// Get trend icon
function getTrendIcon(trend) {
    const icons = {
        improving: '<span class="text-green-500">↗️</span>',
        declining: '<span class="text-red-500">↘️</span>',
        stable: '<span class="text-gray-500">➡️</span>',
        fluctuating: '<span class="text-yellow-500">〰️</span>'
    };
    return icons[trend] || icons.stable;
}

// Get status color
function getStatusColor(status) {
    const colors = {
        excellent: 'text-green-600',
        good: 'text-blue-600',
        warning: 'text-yellow-600',
        critical: 'text-red-600'
    };
    return colors[status] || 'text-gray-600';
}

// Get status background color
function getStatusBackground(status) {
    const colors = {
        excellent: '#059669',
        good: '#0891b2',
        warning: '#f59e0b',
        critical: '#dc2626'
    };
    return colors[status] || '#64748b';
}

// Update insights panel
function updateInsightsPanel(insights) {
    const container = document.getElementById('insights-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!insights || insights.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <div class="text-4xl mb-4">🔍</div>
                <p>No insights available at the moment</p>
            </div>
        `;
        return;
    }
    
    insights.slice(0, 6).forEach((insight, index) => { // Limit to 6 insights
        const card = createInsightCard(insight, index);
        container.appendChild(card);
    });
    
    // Animate insights
    anime({
        targets: '.insight-card',
        translateX: [50, 0],
        opacity: [0, 1],
        delay: anime.stagger(150),
        duration: 600,
        easing: 'easeOutQuart'
    });
}

// Create insight card element
function createInsightCard(insight, index) {
    const card = document.createElement('div');
    card.className = `insight-card bg-white rounded-lg shadow-sm border border-gray-200 p-4 severity-${insight.severity || 'medium'} fade-in`;
    
    const icon = getInsightIcon(insight.type);
    const severityColor = getSeverityColor(insight.severity || 'medium');
    
    card.innerHTML = `
        <div class="flex items-start space-x-3">
            <div class="flex-shrink-0 text-2xl">${icon}</div>
            <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="text-sm font-semibold text-gray-900 truncate">${insight.title}</h3>
                    <span class="text-xs px-2 py-1 rounded-full ${severityColor}">${insight.severity || 'medium'}</span>
                </div>
                <p class="text-sm text-gray-600 mb-3">${insight.message}</p>
                ${insight.recommendation ? `
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                        <p class="text-xs text-blue-800 font-medium mb-1">Recommendation:</p>
                        <p class="text-xs text-blue-700">${insight.recommendation}</p>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    return card;
}

// Get insight icon
function getInsightIcon(type) {
    const icons = {
        performance: '📊',
        causal: '🔗',
        prediction: '🔮',
        optimization: '⚡',
        critical: '🚨',
        warning: '⚠️'
    };
    return icons[type] || '💡';
}

// Get severity color
function getSeverityColor(severity) {
    const colors = {
        high: 'bg-red-100 text-red-800',
        medium: 'bg-yellow-100 text-yellow-800',
        low: 'bg-green-100 text-green-800'
    };
    return colors[severity] || 'bg-gray-100 text-gray-800';
}

// Update network graph
function updateNetworkGraph(graphData) {
    if (!graphData || !graphData.nodes || !graphData.edges) return;
    
    const container = document.getElementById('network-graph');
    if (!container) return;
    
    // Initialize ECharts network graph
    if (!networkChart) {
        networkChart = echarts.init(container);
    }
    
    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'item',
            formatter: function(params) {
                if (params.dataType === 'node') {
                    const node = params.data;
                    return `
                        <div class="text-sm">
                            <strong>${node.label}</strong><br/>
                            Value: ${node.value} ${node.unit}<br/>
                            Target: ${node.target}<br/>
                            Status: ${node.status}<br/>
                            Performance: ${((node.value / node.target) * 100).toFixed(1)}%
                        </div>
                    `;
                } else {
                    return `${params.data.source} → ${params.data.target}<br/>Type: ${params.data.type}`;
                }
            }
        },
        series: [{
            type: 'graph',
            layout: 'force',
            data: graphData.nodes.map(node => ({
                id: node.id,
                name: node.label,
                label: node.label,
                value: node.value,
                symbolSize: node.size || 15,
                itemStyle: {
                    color: node.color || '#2563eb'
                }
            })),
            links: graphData.edges.map(edge => ({
                source: edge.source,
                target: edge.target,
                type: edge.type,
                lineStyle: {
                    color: edge.color || '#2563eb',
                    width: edge.weight || 1
                }
            })),
            roam: true,
            force: {
                repulsion: 100,
                gravity: 0.1,
                edgeLength: 80,
                layoutAnimation: true
            },
            emphasis: {
                focus: 'adjacency',
                lineStyle: {
                    width: 3
                }
            }
        }]
    };
    
    networkChart.setOption(option);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (networkChart) {
            networkChart.resize();
        }
    });
}

// Update strategic goals
function updateStrategicGoals(goals) {
    const container = document.getElementById('strategic-goals');
    if (!container || !goals) return;
    
    container.innerHTML = '';
    
    goals.forEach((goal, index) => {
        const card = createStrategicGoalCard(goal, index);
        container.appendChild(card);
    });
    
    // Animate goals
    anime({
        targets: '.goal-card',
        scale: [0.9, 1],
        opacity: [0, 1],
        delay: anime.stagger(100),
        duration: 500,
        easing: 'easeOutQuart'
    });
}

// Create strategic goal card
function createStrategicGoalCard(goal, index) {
    const card = document.createElement('div');
    card.className = 'goal-card bg-white rounded-lg shadow-sm border border-gray-200 p-4 fade-in';
    
    const progressColor = goal.progress >= 85 ? 'bg-green-500' : 
                         goal.progress >= 70 ? 'bg-yellow-500' : 'bg-red-500';
    
    const statusIcon = goal.status === 'on_track' ? '🎯' : '⚠️';
    
    card.innerHTML = `
        <div class="text-center">
            <div class="text-2xl mb-2">${statusIcon}</div>
            <h3 class="text-sm font-semibold text-gray-900 mb-2">${goal.name}</h3>
            <div class="mb-3">
                <div class="text-2xl font-bold text-gray-900">${goal.progress}%</div>
                <div class="text-xs text-gray-500">Progress</div>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-3">
                <div class="h-2 rounded-full ${progressColor} transition-all duration-500" 
                     style="width: ${goal.progress}%"></div>
            </div>
            <div class="text-xs text-gray-500">
                Risk: <span class="font-medium">${goal.risk_level || 'low'}</span>
            </div>
        </div>
    `;
    
    return card;
}

// Show KPI details modal
function showKPIDetails(kpi) {
    // This would open a detailed view - simplified for demo
    showNotification(`Viewing details for ${kpi.label}`, 'info');
}

// Toggle real-time updates
function toggleRealtimeUpdates() {
    const button = document.getElementById('start-realtime');
    
    if (isRealtimeActive) {
        if (socket) {
            socket.emit('stop_realtime');
        }
        isRealtimeActive = false;
        button.textContent = 'Start Real-Time Updates';
        button.className = 'bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors';
    } else {
        if (socket) {
            socket.emit('start_realtime');
        }
        isRealtimeActive = true;
        button.textContent = 'Stop Real-Time Updates';
        button.className = 'bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 transition-colors';
    }
}

// Run analysis
async function runAnalysis() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/reasoning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ focus_area: 'all' })
        });
        
        if (response.ok) {
            const data = await response.json();
            updateInsightsPanel(data.data.insights);
            showNotification('Analysis completed successfully', 'success');
        } else {
            showNotification('Failed to run analysis', 'error');
        }
        
        showLoading(false);
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Analysis error: ' + error.message, 'error');
        showLoading(false);
    }
}

// Network graph controls
function zoomNetworkGraph(factor) {
    if (networkChart) {
        networkChart.dispatchAction({
            type: 'scale',
            scale: factor
        });
    }
}

function centerNetworkGraph() {
    if (networkChart) {
        networkChart.dispatchAction({
            type: 'restore'
        });
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        if (connected) {
            statusElement.className = 'w-3 h-3 bg-green-400 rounded-full pulse';
        } else {
            statusElement.className = 'w-3 h-3 bg-red-400 rounded-full';
        }
    }
}

// Update last updated timestamp
function updateLastUpdated() {
    const element = document.getElementById('last-updated');
    if (element) {
        element.textContent = new Date().toLocaleTimeString();
    }
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.className = show ? 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50' : 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden';
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg text-white max-w-sm ${getNotificationColor(type)}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    anime({
        targets: notification,
        translateX: [300, 0],
        opacity: [0, 1],
        duration: 300,
        easing: 'easeOutQuart'
    });
    
    // Remove after 3 seconds
    setTimeout(() => {
        anime({
            targets: notification,
            translateX: [0, 300],
            opacity: [1, 0],
            duration: 300,
            easing: 'easeInQuart',
            complete: () => {
                document.body.removeChild(notification);
            }
        });
    }, 3000);
}

// Get notification color
function getNotificationColor(type) {
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        warning: 'bg-yellow-600',
        info: 'bg-blue-600'
    };
    return colors[type] || colors.info;
}

// Start periodic updates
function startPeriodicUpdates() {
    // Update every 30 seconds if not using real-time
    setInterval(() => {
        if (!isRealtimeActive) {
            updateLastUpdated();
        }
    }, 30000);
}

// Initialize insights page
function initializeInsightsPage() {
    console.log('Initializing Insights Page...');
    
    // Initialize WebSocket
    initializeWebSocket();
    
    // Load insights data
    loadInsightsData();
    
    // Set up insights-specific event listeners
    setupInsightsEventListeners();
    
    // Initialize trend chart
    initializeTrendChart();
}

// Load insights data
async function loadInsightsData() {
    try {
        showLoading(true);
        
        // Load insights
        const insightsResponse = await fetch('/api/insights');
        if (insightsResponse.ok) {
            const insightsData = await insightsResponse.json();
            currentInsights = insightsData.data.insights;
            updateInsightsSummary(currentInsights);
            updateInsightsList(currentInsights);
            updateRecommendationsList(currentInsights);
        }
        
        // Load causal analysis
        const reasoningResponse = await fetch('/api/reasoning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ focus_area: 'all' })
        });
        
        if (reasoningResponse.ok) {
            const reasoningData = await reasoningResponse.json();
            updateCausalAnalysis(reasoningData.data.causal_chains);
        }
        
        updateLastUpdated();
        showLoading(false);
    } catch (error) {
        console.error('Failed to load insights data:', error);
        showLoading(false);
    }
}

// Set up insights event listeners
function setupInsightsEventListeners() {
    // Filter buttons
    const filterButtons = ['filter-all', 'filter-critical', 'filter-warning', 'filter-optimization'];
    filterButtons.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', () => filterInsights(id.replace('filter-', '')));
        }
    });
    
    // Refresh button
    const refreshBtn = document.getElementById('refresh-insights');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadInsightsData);
    }
}

// Update insights summary
function updateInsightsSummary(insights) {
    const totalElement = document.getElementById('total-insights');
    const criticalElement = document.getElementById('critical-insights');
    const warningElement = document.getElementById('warning-insights');
    const optimizationElement = document.getElementById('optimization-insights');
    
    if (totalElement) totalElement.textContent = insights.length;
    if (criticalElement) criticalElement.textContent = insights.filter(i => i.severity === 'high').length;
    if (warningElement) warningElement.textContent = insights.filter(i => i.severity === 'medium').length;
    if (optimizationElement) optimizationElement.textContent = insights.filter(i => i.type === 'optimization').length;
}

// Update insights list
function updateInsightsList(insights) {
    const container = document.getElementById('insights-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    insights.forEach((insight, index) => {
        const card = createInsightCard(insight, index);
        container.appendChild(card);
    });
}

// Update recommendations list
function updateRecommendationsList(insights) {
    const container = document.getElementById('recommendations-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    const recommendations = insights.filter(i => i.recommendation).slice(0, 5);
    
    recommendations.forEach((insight, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card rounded-lg p-4 border-l-4';
        card.style.borderLeftColor = getRecommendationColor(insight.severity);
        
        card.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="flex-shrink-0 text-lg">${getInsightIcon(insight.type)}</div>
                <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-semibold text-gray-900 mb-1">${insight.title}</h3>
                    <p class="text-xs text-gray-600 mb-2">${insight.recommendation}</p>
                    <div class="text-xs text-gray-500">
                        Priority: <span class="font-medium">${insight.severity || 'medium'}</span>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}

// Get recommendation color
function getRecommendationColor(severity) {
    const colors = {
        high: '#dc2626',
        medium: '#f59e0b',
        low: '#059669'
    };
    return colors[severity] || '#2563eb';
}

// Filter insights
function filterInsights(filterType) {
    let filteredInsights = currentInsights;
    
    if (filterType !== 'all') {
        filteredInsights = currentInsights.filter(insight => {
            switch (filterType) {
                case 'critical':
                    return insight.severity === 'high';
                case 'warning':
                    return insight.severity === 'medium';
                case 'optimization':
                    return insight.type === 'optimization';
                default:
                    return true;
            }
        });
    }
    
    updateInsightsList(filteredInsights);
    
    // Update filter button states
    document.querySelectorAll('[id^="filter-"]').forEach(btn => {
        btn.className = 'px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200';
    });
    
    const activeBtn = document.getElementById(`filter-${filterType}`);
    if (activeBtn) {
        activeBtn.className = 'px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium';
    }
}

// Initialize trend chart
function initializeTrendChart() {
    const container = document.getElementById('trend-chart');
    if (!container) return;
    
    const chart = echarts.init(container);
    
    // Generate sample trend data
    const dates = [];
    const values = [];
    const now = new Date();
    
    for (let i = 29; i >= 0; i--) {
        const date = new Date(now);
        date.setDate(date.getDate() - i);
        dates.push(date.toISOString().split('T')[0]);
        values.push(75 + Math.random() * 20 + Math.sin(i / 5) * 5);
    }
    
    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
                formatter: function(value) {
                    return new Date(value).toLocaleDateString();
                }
            }
        },
        yAxis: {
            type: 'value',
            min: 60,
            max: 100
        },
        series: [{
            data: values,
            type: 'line',
            smooth: true,
            lineStyle: {
                color: '#2563eb'
            },
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0, color: 'rgba(37, 99, 235, 0.3)'
                    }, {
                        offset: 1, color: 'rgba(37, 99, 235, 0.1)'
                    }]
                }
            }
        }]
    };
    
    chart.setOption(option);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        chart.resize();
    });
}

// Update causal analysis
function updateCausalAnalysis(causalChains) {
    const container = document.getElementById('causal-analysis');
    if (!container || !causalChains) return;
    
    container.innerHTML = '';
    
    // Show top causal chains
    const topChains = causalChains.slice(0, 3);
    
    topChains.forEach((chain, index) => {
        const card = document.createElement('div');
        card.className = 'bg-gray-50 rounded-lg p-4 mb-4';
        
        const chainLabels = chain.chain || [];
        
        card.innerHTML = `
            <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-semibold text-gray-900">Causal Chain ${index + 1}</h3>
                <span class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                    Impact: ${(chain.impact * 100).toFixed(1)}%
                </span>
            </div>
            <div class="flex items-center space-x-2 text-sm text-gray-600">
                ${chainLabels.map((label, i) => `
                    <span>${label}</span>
                    ${i < chainLabels.length - 1 ? '<span>→</span>' : ''}
                `).join('')}
            </div>
        `;
        
        container.appendChild(card);
    });
}