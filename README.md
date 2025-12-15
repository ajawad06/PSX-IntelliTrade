# PSX Stock Advisor - AI-Powered Trading Platform

A professional, AI-powered stock analysis and portfolio building platform for Pakistan Stock Exchange (PSX) with modern trading-style UI.

![PSX Stock Advisor](https://img.shields.io/badge/PSX-Stock%20Advisor-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### 1. **AI-Powered Portfolio Builder** 💼
- Automatically scans all PSX stocks for strong BUY signals
- Filters stocks with confidence ≥ 70%
- Intelligent budget allocation based on risk tolerance:
  - **Conservative**: 5-7 stocks, equal weighting
  - **Moderate**: 4-5 stocks, confidence-weighted
  - **Aggressive**: 3-4 stocks, top performer weighted
- Exact share calculations ensuring budget compliance
- Real-time portfolio summary with cash remaining

### 2. **Professional Trading UI** 📈
- **Modern Dark Theme** with trading-specific colors
- **Interactive Charts**:
  - Candlestick charts with SMA overlays
  - RSI indicator with overbought/oversold zones
  - MACD with histogram visualization
- **Real-time Market Scanner** for opportunities
- **Stock Analysis** with AI-powered buy/sell/hold signals
- **Glassmorphism effects** and smooth animations
- **Fully responsive** design

### 3. **Technical Analysis** 📊
- Multiple technical indicators:
  - SMA (5, 20 period)
  - RSI (14 period)
  - MACD with signal line
  - EMA (12, 26 period)
- Rule-based decision engine
- Confidence scoring for all signals
- Volume analysis

### 4. **Market Scanner** 🔍
- Real-time scanning of all PSX stocks
- Filter by BUY/SELL/HOLD signals
- Sortable results table
- Quick analyze action

### 5. **News Integration** 📰
- Stock-specific news from major sources
- Latest PSX market news
- Clean, formatted news display

## 🏗️ Architecture

```
psx_stock_advisor/
├── backend/                    # Flask REST API
│   ├── app.py                 # Main API server
│   ├── portfolio_ai.py        # AI Portfolio Builder
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Trading UI
│   ├── index.html             # Main HTML
│   ├── styles.css             # Professional trading CSS
│   └── app.js                 # JavaScript application
├── data_fetcher.py            # Stock data fetching
├── indicators.py              # Technical indicators
├── rule_engine.py             # Trading signals
├── news_fetcher.py            # News scraping
└── app.py                     # Streamlit app (legacy)
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for fetching stock data)

## 🔧 Installation & Setup

### Step 1: Clone or Download the Project

```bash
cd psx_stock_advisor
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Start the Flask API Server

```bash
python app.py
```

The API server will start on `http://localhost:5000`

You should see:
```
============================================================
PSX Stock Advisor - Flask API Server
============================================================
Server starting on http://localhost:5000
API Documentation: http://localhost:5000/api/health
============================================================
```

### Step 4: Open the Frontend

In a new terminal/command prompt:

```bash
cd frontend
```

**Option 1: Using Python's built-in HTTP server**
```bash
python -m http.server 8080
```

**Option 2: Using any local web server**
- Simply open `index.html` in a modern browser
- Or use Live Server extension in VS Code

### Step 5: Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:8080`
- API Health Check: `http://localhost:5000/api/health`

## 🎯 Usage Guide

### Dashboard
- View market statistics (buy/sell/hold signals count)
- See top movers with price changes
- Quick access to all features

### Stock Analysis
1. Select a stock from the dropdown
2. Choose time period (1mo, 3mo, 6mo, 1y)
3. Click "Analyze"
4. View:
   - **Large BUY/SELL/HOLD signal** (animated, prominent)
   - Price metrics and changes
   - Interactive candlestick chart
   - RSI and MACD indicators
   - Technical signals breakdown

### AI Portfolio Builder
1. Enter your investment budget (PKR)
2. Select risk tolerance:
   - Conservative: More diversified, lower risk
   - Moderate: Balanced approach
   - Aggressive: Concentrated, higher returns potential
3. Click "Generate Smart Portfolio"
4. Wait for AI to analyze all stocks
5. Review recommended portfolio:
   - Exact number of shares to buy
   - Investment amount per stock
   - Portfolio allocation percentages
   - Cash remaining

### Market Scanner
1. Choose filter: All Stocks / Buy Signals / Sell Signals
2. Click "Start Scan"
3. View results in sortable table
4. Click "Analyze" on any stock for detailed view

## 🌐 API Endpoints

### `GET /api/health`
Health check endpoint

### `GET /api/stocks`
Get list of all available PSX stocks

**Response:**
```json
{
  "success": true,
  "stocks": ["HBL", "OGDC", "PSO", ...],
  "count": 40
}
```

### `GET /api/stock/:ticker?period=3mo`
Get detailed analysis for specific stock

**Parameters:**
- `ticker`: Stock symbol (e.g., "HBL")
- `period`: Time period (1mo, 3mo, 6mo, 1y)

**Response:**
```json
{
  "success": true,
  "ticker": "HBL",
  "analysis": {
    "decision": "BUY",
    "confidence": 85,
    "signals": [...]
  },
  "price": {
    "current": 150.5,
    "change": 2.5,
    "change_percent": 1.69,
    ...
  },
  "indicators": {...},
  "chart_data": [...],
  "news": [...]
}
```

### `POST /api/portfolio/generate`
Generate AI-powered portfolio

**Request Body:**
```json
{
  "budget": 100000,
  "risk_level": "moderate"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully generated portfolio with 4 stocks",
  "stocks": [
    {
      "ticker": "HBL",
      "price": 150.5,
      "shares": 220,
      "investment": 33110,
      "allocation_percent": 33.1,
      "confidence": 85,
      ...
    },
    ...
  ],
  "summary": {
    "total_budget": 100000,
    "total_invested": 98500,
    "cash_remaining": 1500,
    "num_stocks": 4,
    "percent_invested": 98.5
  }
}
```

### `GET /api/market-scan?type=all`
Scan market for trading opportunities

**Parameters:**
- `type`: Filter type (all, buy, sell)

### `GET /api/news/:ticker?limit=5`
Get stock-specific news

## 🎨 UI Features

### Professional Trading Theme
- **Dark charcoal background** (#0a0e27)
- **Trading colors**: Green (#00C853) for BUY, Red (#FF1744) for SELL
- **Glassmorphism cards** with backdrop blur
- **Smooth animations** on hover and interactions
- **Gradient accents** for CTAs and important elements

### Interactive Elements
- **Animated signal badges** with pulse effect
- **Hover states** on all interactive components
- **Progress bars** for scanning operations
- **Toast notifications** for user feedback
- **Loading spinners** during API calls

### Responsive Design
- Mobile-optimized layouts
- Flexible grid systems
- Touch-friendly controls
- Adaptive typography

## ⚙️ Configuration

### Changing API URL
Edit `frontend/app.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Modifying Stock List
Edit `backend/app.py` or `backend/portfolio_ai.py`:
```python
ALL_PSX_STOCKS = [
    "HBL", "OGDC", "PSO", ...
]
```

### Adjusting Portfolio AI Parameters
Edit `backend/portfolio_ai.py`:
```python
def scan_market_for_opportunities(self, min_confidence=70):
    # Change min_confidence to adjust filtering threshold
```

## 🧪 Testing

### Test Portfolio AI
```bash
cd backend
python portfolio_ai.py
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get stocks
curl http://localhost:5000/api/stocks

# Analyze stock
curl http://localhost:5000/api/stock/HBL?period=3mo

# Generate portfolio
curl -X POST http://localhost:5000/api/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{"budget": 100000, "risk_level": "moderate"}'
```

## 📊 Technical Indicators Explained

### SMA (Simple Moving Average)
- **SMA(5)**: Short-term trend (5 days)
- **SMA(20)**: Long-term trend (20 days)
- **Golden Cross**: SMA(5) crosses above SMA(20) = BUY signal
- **Death Cross**: SMA(5) crosses below SMA(20) = SELL signal

### RSI (Relative Strength Index)
- **Range**: 0-100
- **< 30**: Oversold (potential BUY)
- **> 70**: Overbought (potential SELL)
- **30-70**: Neutral zone

### MACD (Moving Average Convergence Divergence)
- **MACD Line**: Difference between EMA(12) and EMA(26)
- **Signal Line**: EMA(9) of MACD
- **Histogram**: MACD - Signal
- **Crossover above signal**: BUY
- **Crossover below signal**: SELL

## ⚠️ Disclaimer

**IMPORTANT**: This application is for **educational and informational purposes only**. 

- NOT financial advice
- NOT a recommendation to buy or sell securities
- Past performance does not guarantee future results
- Always conduct your own research
- Consult with qualified financial advisors before investing
- The developers are not responsible for any financial losses

## 🐛 Troubleshooting

### CORS Errors
- Ensure Flask backend is running on port 5000
- Check that Flask-CORS is installed
- Verify API_BASE_URL in app.js

### No Data for Stock
- Some stocks may have limited historical data
- Try different time periods (1mo instead of 1y)
- Check internet connection
- Verify stock ticker is correct

### Portfolio Not Generating
- Ensure budget is >= 1000 PKR
- Check that backend is running
- Look for error messages in browser console
- May indicate no strong BUY signals in current market

### Charts Not Displaying
- Check browser console for errors
- Ensure Chart.js is loaded (check CDN)
- Try refreshing the page
- Clear browser cache

## 📝 Future Enhancements

- [ ] Real-time price updates via WebSocket
- [ ] User authentication and saved portfolios
- [ ] Backtesting capabilities
- [ ] Email alerts for signals
- [ ] More technical indicators (Bollinger Bands, Fibonacci)
- [ ] Sector-based analysis
- [ ] Fundamental analysis integration
- [ ] Mobile app version

## 📜 License

MIT License - feel free to use for personal and educational purposes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Built with ❤️ for PSX traders and investors**
