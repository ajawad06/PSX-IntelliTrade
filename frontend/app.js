// ============================================================================
// PSX Stock Advisor - JavaScript Application
// ============================================================================

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
const state = {
    currentPage: 'dashboard',
    selectedStock: null,
    selectedPeriod: '3mo',
    currentFilter: 'all',
    selectedRisk: 'moderate',
    charts: {
        price: null,
        rsi: null,
        macd: null
    }
};

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    setupNavigation();
    setupEventListeners();
    await loadStocksList();
    loadDashboard();
}

// ============================================================================
// Navigation
// ============================================================================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            switchPage(page);
        });
    });
}

function switchPage(pageName) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });

    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    document.getElementById(`${pageName}-page`).classList.add('active');
    state.currentPage = pageName;

    // Load page data
    if (pageName === 'dashboard') {
        loadDashboard();
    }
}

// ============================================================================
// Event Listeners
// ============================================================================

function setupEventListeners() {
    // Analyze button
    document.getElementById('analyzeBtn').addEventListener('click', analyzeStock);

    // Generate portfolio button
    document.getElementById('generatePortfolioBtn').addEventListener('click', generatePortfolio);

    // Risk selector
    document.querySelectorAll('.risk-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.risk-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.selectedRisk = btn.dataset.risk;
        });
    });

    // Scan button
    document.getElementById('scanBtn').addEventListener('click', scanMarket);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentFilter = btn.dataset.filter;
        });
    });

    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', () => {
        if (state.currentPage === 'dashboard') {
            loadDashboard();
        } else if (state.currentPage === 'analysis' && state.selectedStock) {
            analyzeStock();
        }
    });
}

// ============================================================================
// API Functions
// ============================================================================

async function apiCall(endpoint, options = {}) {
    try {
        const response = await axios({
            url: `${API_BASE_URL}${endpoint}`,
            ...options
        });
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        showToast(`Error: ${error.response?.data?.error || error.message}`, 'error');
        throw error;
    }
}

async function loadStocksList() {
    try {
        const data = await apiCall('/stocks');
        const select = document.getElementById('stockSelect');

        data.stocks.forEach(stock => {
            const option = document.createElement('option');
            option.value = stock;
            option.textContent = stock;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load stocks list');
    }
}

// ============================================================================
// Dashboard
// ============================================================================

async function loadDashboard() {
    showLoading('marketOverviewLoading');
    hideElement('marketOverviewContent');

    try {
        // Quick scan to get signals
        const scanData = await apiCall('/market-scan?type=all');

        if (scanData.success) {
            const buySignals = scanData.results.filter(r => r.signal === 'BUY').length;
            const sellSignals = scanData.results.filter(r => r.signal === 'SELL').length;
            const holdSignals = scanData.results.filter(r => r.signal === 'HOLD').length;

            document.getElementById('buySignals').textContent = buySignals;
            document.getElementById('sellSignals').textContent = sellSignals;
            document.getElementById('holdSignals').textContent = holdSignals;

            // Show top movers
            displayTopMovers(scanData.results);
        }

        hideLoading('marketOverviewLoading');
        showElement('marketOverviewContent');
    } catch (error) {
        hideLoading('marketOverviewLoading');
        showElement('marketOverviewContent');
        document.getElementById('topMoversContainer').innerHTML = '<p style="color: var(--text-secondary); text-align: center;">Failed to load market data</p>';
    }
}

function displayTopMovers(stocks) {
    const sorted = stocks.sort((a, b) => Math.abs(b.change_percent) - Math.abs(a.change_percent));
    const top5 = sorted.slice(0, 5);

    const container = document.getElementById('topMoversContainer');
    container.innerHTML = '<h3 style="margin-bottom: 1rem;">Top Movers</h3>';

    top5.forEach(stock => {
        const card = document.createElement('div');
        card.className = 'stock-allocation-card';
        card.style.marginBottom = '1rem';
        card.style.cursor = 'pointer';
        card.onclick = () => analyzeStockByTicker(stock.ticker);

        card.innerHTML = `
            <div class="allocation-header">
                <span class="allocation-ticker">${stock.ticker}</span>
                <span class="signal-badge signal-badge-${stock.signal.toLowerCase()}">${stock.signal}</span>
            </div>
            <div class="allocation-details">
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Price</span>
                    <span class="allocation-detail-value">PKR ${stock.price.toFixed(2)}</span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Change</span>
                    <span class="allocation-detail-value" style="color: ${stock.change_percent >= 0 ? 'var(--color-success)' : 'var(--color-danger)'}">
                        ${stock.change_percent >= 0 ? '+' : ''}${stock.change_percent.toFixed(2)}%
                    </span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Confidence</span>
                    <span class="allocation-detail-value">${stock.confidence}%</span>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

// ============================================================================
// Stock Analysis
// ============================================================================

async function analyzeStock() {
    const ticker = document.getElementById('stockSelect').value;
    const period = document.getElementById('periodSelect').value;

    if (!ticker) {
        showToast('Please select a stock', 'warning');
        return;
    }

    state.selectedStock = ticker;
    state.selectedPeriod = period;

    showLoading('analysisLoading');
    hideElement('analysisContent');

    try {
        const data = await apiCall(`/stock/${ticker}?period=${period}`);

        if (data.success) {
            displayAnalysis(data);
            hideLoading('analysisLoading');
            showElement('analysisContent');
        }
    } catch (error) {
        hideLoading('analysisLoading');
    }
}

async function analyzeStockByTicker(ticker) {
    document.getElementById('stockSelect').value = ticker;
    switchPage('analysis');
    await analyzeStock();
}

function displayAnalysis(data) {
    // Trading Signal
    const signalDiv = document.getElementById('tradingSignal');
    const decision = data.analysis.decision;
    signalDiv.className = `trading-signal signal-${decision.toLowerCase()}`;
    signalDiv.textContent = `${decision === 'BUY' ? '🟢' : decision === 'SELL' ? '🔴' : '⏸️'} STRONG ${decision} SIGNAL`;

    // Metrics
    document.getElementById('metricPrice').textContent = `PKR ${data.price.current.toFixed(2)}`;

    const changeSpan = document.getElementById('metricChange');
    changeSpan.textContent = `${data.price.change >= 0 ? '+' : ''}${data.price.change.toFixed(2)} (${data.price.change_percent >= 0 ? '+' : ''}${data.price.change_percent.toFixed(2)}%)`;
    changeSpan.className = `metric-change ${data.price.change >= 0 ? 'positive' : 'negative'}`;

    document.getElementById('metricConfidence').textContent = `${data.analysis.confidence}%`;
    document.getElementById('metricRSI').textContent = data.indicators.rsi.toFixed(2);
    document.getElementById('metricVolume').textContent = new Intl.NumberFormat().format(data.price.volume);

    // Signals
    const signalsList = document.getElementById('signalsList');
    signalsList.innerHTML = '';

    data.analysis.signals.forEach(signal => {
        const div = document.createElement('div');
        div.className = 'signal-item';

        if (signal.includes('BULLISH') || signal.includes('✅')) {
            div.classList.add('signal-bullish');
        } else if (signal.includes('BEARISH') || signal.includes('❌')) {
            div.classList.add('signal-bearish');
        } else {
            div.classList.add('signal-neutral');
        }

        div.textContent = signal;
        signalsList.appendChild(div);
    });

    // Charts
    createPriceChart(data.chart_data);
    createRSIChart(data.chart_data);
    createMACDChart(data.chart_data);

    // Display News
    displayStockNews(data.ticker, data.news);
}

function displayStockNews(ticker, newsData) {
    const newsTickerSpan = document.getElementById('newsStockTicker');
    const newsContainer = document.getElementById('newsContainer');

    newsTickerSpan.textContent = ticker;
    newsContainer.innerHTML = '';

    if (newsData && newsData.length > 0) {
        // Filter valid news
        const validNews = newsData.filter(item => {
            const title = (item.title || '').toLowerCase();
            const summary = (item.summary || '').toLowerCase();

            // Filter out Google News errors and XML artifacts
            const invalidPatterns = [
                'this feed is not available',
                'for the latest headlines',
                'this xml file',
                'ispermalink',
                '<item>',
                '<rss>',
                'xml feed is made available',
                'news-webmaster@google.com',
                'copyright',
                'all rights reserved'
            ];

            for (let pattern of invalidPatterns) {
                if (title.includes(pattern) || summary.includes(pattern)) {
                    return false;
                }
            }

            // Skip if title is too short or just 'false'
            if (title.trim() === 'false' || title.length < 15) {
                return false;
            }

            return true;
        });

        if (validNews.length > 0) {
            validNews.forEach(item => {
                const newsItem = document.createElement('div');
                newsItem.className = 'news-item';

                // Clean summary
                const cleanSummary = (item.summary || item.title)
                    .replace(/<[^>]+>/g, '')
                    .replace(/&[a-z]+;/gi, ' ')
                    .replace(/\s+/g, ' ')
                    .trim();

                const cleanTitle = (item.title || '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/&[a-z]+;/gi, ' ')
                    .replace(/\s+/g, ' ')
                    .trim();

                if (cleanSummary.length < 20) return;

                // Add source badge styling
                const isPSXGeneral = item.source === 'PSX Market News';
                const sourceLabel = isPSXGeneral ?
                    '<span style="background: rgba(255,179,0,0.2); color: #FFB300; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">📊 PSX Market</span>' :
                    `<span style="background: rgba(108,99,255,0.2); color: #6C63FF; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">${item.source || 'Stock News'}</span>`;

                newsItem.innerHTML = `
                    <div class="news-title">${cleanTitle}</div>
                    <div class="news-published">📅 ${item.published} | ${sourceLabel}</div>
                    <div class="news-summary">${cleanSummary.substring(0, 300)}${cleanSummary.length > 300 ? '...' : ''}</div>
                    <a href="${item.link}" target="_blank" class="news-link">Read Full Article →</a>
                `;

                newsContainer.appendChild(newsItem);
            });
        } else {
            newsContainer.innerHTML = `<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No news available for ${ticker}</p>`;
        }
    } else {
        newsContainer.innerHTML = `<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No news available for ${ticker}</p>`;
    }
}

function createPriceChart(chartData) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    // Destroy existing chart
    if (state.charts.price) {
        state.charts.price.destroy();
    }

    const dates = chartData.map(d => d.date);
    const closes = chartData.map(d => d.close);
    const sma5 = chartData.map(d => d.sma_5);
    const sma20 = chartData.map(d => d.sma_20);
    const volumes = chartData.map(d => d.volume);

    state.charts.price = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Close Price',
                    data: closes,
                    borderColor: '#6C63FF',
                    backgroundColor: 'rgba(108, 99, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'SMA 5',
                    data: sma5,
                    borderColor: '#FFB300',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'SMA 20',
                    data: sma20,
                    borderColor: '#2196F3',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#E8EAED'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#9AA0A6',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 10
                    },
                    grid: {
                        color: '#2d3548',
                        drawBorder: false
                    }
                },
                y: {
                    ticks: {
                        color: '#9AA0A6'
                    },
                    grid: {
                        color: '#2d3548'
                    }
                }
            }
        }
    });
}

function createRSIChart(chartData) {
    const ctx = document.getElementById('rsiChart').getContext('2d');

    if (state.charts.rsi) {
        state.charts.rsi.destroy();
    }

    const dates = chartData.map(d => d.date);
    const rsiValues = chartData.map(d => d.rsi);

    state.charts.rsi = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'RSI',
                data: rsiValues,
                borderColor: '#8B5CF6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#E8EAED'
                    }
                },
                annotation: {
                    annotations: {
                        overbought: {
                            type: 'line',
                            yMin: 70,
                            yMax: 70,
                            borderColor: '#FF1744',
                            borderWidth: 2,
                            borderDash: [5, 5]
                        },
                        oversold: {
                            type: 'line',
                            yMin: 30,
                            yMax: 30,
                            borderColor: '#00C853',
                            borderWidth: 2,
                            borderDash: [5, 5]
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#9AA0A6',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 8
                    },
                    grid: {
                        color: '#2d3548',
                        drawBorder: false
                    }
                },
                y: {
                    min: 0,
                    max: 100,
                    ticks: {
                        color: '#9AA0A6'
                    },
                    grid: {
                        color: '#2d3548'
                    }
                }
            }
        }
    });
}

function createMACDChart(chartData) {
    const ctx = document.getElementById('macdChart').getContext('2d');

    if (state.charts.macd) {
        state.charts.macd.destroy();
    }

    const dates = chartData.map(d => d.date);
    const macd = chartData.map(d => d.macd);
    const signal = chartData.map(d => d.macd_signal);
    const hist = chartData.map(d => d.macd_hist);

    state.charts.macd = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    type: 'line',
                    label: 'MACD',
                    data: macd,
                    borderColor: '#2196F3',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    type: 'line',
                    label: 'Signal',
                    data: signal,
                    borderColor: '#FF5722',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    type: 'bar',
                    label: 'Histogram',
                    data: hist,
                    backgroundColor: hist.map(v => v >= 0 ? 'rgba(0, 200, 83, 0.5)' : 'rgba(255, 23, 68, 0.5)')
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#E8EAED'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#9AA0A6',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 10
                    },
                    grid: {
                        color: '#2d3548',
                        drawBorder: false
                    }
                },
                y: {
                    ticks: {
                        color: '#9AA0A6'
                    },
                    grid: {
                        color: '#2d3548'
                    }
                }
            }
        }
    });
}

// ============================================================================
// Portfolio Builder
// ============================================================================

async function generatePortfolio() {
    const budget = parseFloat(document.getElementById('budgetInput').value);

    if (!budget || budget < 1000) {
        showToast('Please enter a valid budget (minimum PKR 1,000)', 'warning');
        return;
    }

    showLoading('portfolioLoading');
    hideElement('portfolioResult');

    try {
        const data = await apiCall('/portfolio/generate', {
            method: 'POST',
            data: {
                budget: budget,
                risk_level: state.selectedRisk
            }
        });

        if (data.success) {
            displayPortfolio(data);
            hideLoading('portfolioLoading');
            showElement('portfolioResult');
        } else {
            hideLoading('portfolioLoading');
            showToast(data.message, 'warning');
        }
    } catch (error) {
        hideLoading('portfolioLoading');
    }
}

function displayPortfolio(data) {
    // Summary
    document.getElementById('summaryBudget').textContent = `PKR ${new Intl.NumberFormat().format(data.summary.total_budget)}`;
    document.getElementById('summaryInvested').textContent = `PKR ${new Intl.NumberFormat().format(Math.round(data.summary.total_invested))}`;
    document.getElementById('summaryRemaining').textContent = `PKR ${new Intl.NumberFormat().format(Math.round(data.summary.cash_remaining))}`;
    document.getElementById('summaryStocks').textContent = data.summary.num_stocks;

    // Stock allocations
    const container = document.getElementById('stockAllocations');
    container.innerHTML = '';

    data.stocks.forEach((stock, index) => {
        const card = document.createElement('div');
        card.className = 'stock-allocation-card';

        card.innerHTML = `
            <div class="allocation-header">
                <span class="allocation-ticker">${stock.ticker}</span>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <span class="allocation-signal">BUY ${stock.confidence}%</span>
                </div>
            </div>
            <div class="allocation-details">
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Price per Share</span>
                    <span class="allocation-detail-value">PKR ${stock.price.toFixed(2)}</span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Shares to Buy</span>
                    <span class="allocation-detail-value">${stock.shares}</span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Total Investment</span>
                    <span class="allocation-detail-value">PKR ${new Intl.NumberFormat().format(Math.round(stock.investment))}</span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">Portfolio %</span>
                    <span class="allocation-detail-value">${stock.allocation_percent.toFixed(1)}%</span>
                </div>
                <div class="allocation-detail">
                    <span class="allocation-detail-label">RSI</span>
                    <span class="allocation-detail-value">${stock.rsi.toFixed(2)}</span>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

// ============================================================================
// Market Scanner
// ============================================================================

async function scanMarket() {
    showElement('scanProgress');
    hideElement('scanResults');

    document.getElementById('progressFill').style.width = '0%';
    document.getElementById('progressText').textContent = 'Scanning market...';

    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 5;
            document.getElementById('progressFill').style.width = `${progress}%`;
            if (progress >= 95) {
                clearInterval(progressInterval);
            }
        }, 100);

        const data = await apiCall(`/market-scan?type=${state.currentFilter}`);

        clearInterval(progressInterval);
        document.getElementById('progressFill').style.width = '100%';

        if (data.success) {
            displayScanResults(data.results);
            hideElement('scanProgress');
            showElement('scanResults');
        }
    } catch (error) {
        hideElement('scanProgress');
    }
}

function displayScanResults(results) {
    document.getElementById('resultsCount').textContent = results.length;

    // Clear lists
    const buyList = document.getElementById('buyList');
    const sellList = document.getElementById('sellList');
    const holdList = document.getElementById('holdList');

    buyList.innerHTML = '';
    sellList.innerHTML = '';
    holdList.innerHTML = '';

    let buyCount = 0;
    let sellCount = 0;
    let holdCount = 0;

    results.forEach(stock => {
        const card = createScannerCard(stock);

        if (stock.signal === 'BUY') {
            buyList.appendChild(card);
            buyCount++;
        } else if (stock.signal === 'SELL') {
            sellList.appendChild(card);
            sellCount++;
        } else {
            holdList.appendChild(card);
            holdCount++;
        }
    });

    // Update counts
    document.getElementById('buyCount').textContent = buyCount;
    document.getElementById('sellCount').textContent = sellCount;
    document.getElementById('holdCount').textContent = holdCount;
}

function createScannerCard(stock) {
    const card = document.createElement('div');
    card.className = 'scanner-card';
    card.onclick = () => analyzeStockByTicker(stock.ticker);

    const changeClass = stock.change_percent >= 0 ? 'change-positive' : 'change-negative';
    const changeSign = stock.change_percent >= 0 ? '+' : '';

    card.innerHTML = `
        <div class="scanner-card-header">
            <span class="scanner-ticker">${stock.ticker}</span>
            <span class="scanner-price">PKR ${stock.price.toFixed(2)}</span>
        </div>
        <div class="scanner-details">
            <span class="${changeClass}">${changeSign}${stock.change_percent.toFixed(2)}%</span>
            <span>RSI: ${stock.rsi.toFixed(1)}</span>
            <span>Conf: ${stock.confidence}%</span>
        </div>
    `;

    return card;
}

// ============================================================================
// Utility Functions
// ============================================================================

function showLoading(elementId) {
    document.getElementById(elementId).style.display = 'flex';
}

function hideLoading(elementId) {
    document.getElementById(elementId).style.display = 'none';
}

function showElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }
}

function hideElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Make functions globally available
window.switchPage = switchPage;
window.analyzeStockByTicker = analyzeStockByTicker;
