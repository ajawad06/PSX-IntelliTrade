# ============================================================================
# FILE: app.py
# Description: Flask REST API Server for PSX Stock Advisor (Optimized)
# ============================================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import concurrent.futures
import time
import pandas as pd

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetcher import StockDataFetcher
from indicators import TechnicalIndicators
from rule_engine import RuleEngine
from news_fetcher import NewsFetcher
from portfolio_ai import PortfolioAI

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize components
fetcher = StockDataFetcher()
engine = RuleEngine()
news_fetcher = NewsFetcher()
portfolio_ai = PortfolioAI()

# PSX Stocks List
ALL_PSX_STOCKS = [
    "HBL", "OGDC", "PSO", "ENGRO", "MCB", "UBL", "LUCK", "FFC", "MEBL", "PPL",
    "HUBC", "MARI", "TRG", "SYS", "EFERT", "KAPCO", "NBP", "BAFL", "ABL", "SNGP",
    "POL", "DGKC", "MLCF", "PTC", "KEL", "FCCL", "HASCOL", "APL", "ICI", "DAWH",
    "CHCC", "COLG", "NML", "NESTLE", "FHAM", "PIOC", "PAEL", "BYCO", "SEARL", "SHEL"
]

def analyze_single_stock_safe(ticker):
    """Helper to analyze a single stock safely for parallel execution"""
    try:
        # Fetch data (use shorter period for speed)
        data, error = fetcher.get_stock_data(ticker, '6mo')
        
        if error or data is None or data.empty:
            return None
        
        # Add indicators
        data = TechnicalIndicators.add_all_indicators(data)
        
        # Get decision
        decision, confidence, signals = engine.analyze(data)
        
        # Calculate price change (Last 1 Month / ~22 Trading Days)
        latest_price = float(data['Close'].iloc[-1])
        
        if len(data) > 22:
            first_price = float(data['Close'].iloc[-22])
        else:
            first_price = float(data['Close'].iloc[0])
            
        change_pct = ((latest_price - first_price) / first_price) * 100
        
        return {
            'ticker': ticker,
            'price': latest_price,
            'change_percent': change_pct,
            'signal': decision,
            'confidence': confidence,
            'rsi': float(data['RSI'].iloc[-1]),
            'volume': int(data['Volume'].iloc[-1])
        }
    except Exception as e:
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'PSX Stock Advisor API is running'})


@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Get list of all available PSX stocks"""
    return jsonify({
        'success': True,
        'stocks': ALL_PSX_STOCKS,
        'count': len(ALL_PSX_STOCKS)
    })


@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_analysis(ticker):
    """Get detailed analysis for a specific stock"""
    try:
        # Get period from query params (default: 3mo)
        requested_period = request.args.get('period', '3mo')
        
        # KEY FIX: Always fetch longer history (e.g. 1y) to calculate indicators (MACD/SMA) correctly
        # If we only fetch '1mo', MACD (requires 26+ days) will be empty/NaN!
        fetch_period = '1y' 
        if requested_period in ['2y', '5y', 'max']:
            fetch_period = requested_period
            
        # Fetch stock data
        data, error = fetcher.get_stock_data(ticker, fetch_period)
        
        if error or data is None or data.empty:
            return jsonify({
                'success': False,
                'error': error or 'No data available for this stock'
            }), 404
        
        # Add technical indicators (Now using 1y data, so MACD will be valid)
        data = TechnicalIndicators.add_all_indicators(data)
        
        # Filter data to match the requested period for display
        # Slicing logic based on approximate trading days
        days_map = {'1mo': 22, '3mo': 66, '6mo': 132, '1y': 252, '2y': 504, '5y': 1260}
        display_days = days_map.get(requested_period, 66) # Default to 3mo if unknown
        
        if len(data) > display_days and requested_period != 'max':
            display_data = data.tail(display_days)
        else:
            display_data = data # Use all if requested period is long
            
        # Get trading decision (Analyze the LATEST data point)
        decision, confidence, signals = engine.analyze(data)
        
        # Get latest stats
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        latest_price = float(latest['Close'])
        prev_price = float(prev['Close'])
        price_change = latest_price - prev_price
        price_change_pct = (price_change / prev_price) * 100
        
        # High/Low for the SELECTED period
        period_high = float(display_data['High'].max())
        period_low = float(display_data['Low'].min())
        
        # Prepare chart data
        chart_data = []
        for idx, row in display_data.iterrows():
            # Handle NaN values for JSON (replace with None)
            macd_val = float(row['MACD']) if not pd.isna(row['MACD']) else None
            sig_val = float(row['MACD_Signal']) if not pd.isna(row['MACD_Signal']) else None
            hist_val = float(row['MACD_Hist']) if not pd.isna(row['MACD_Hist']) else None
            sma5_val = float(row['SMA_5']) if not pd.isna(row['SMA_5']) else None
            
            chart_data.append({
                'date': idx.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume']),
                'sma_5': sma5_val,
                'sma_20': float(row['SMA_20']) if not pd.isna(row['SMA_20']) else None,
                'rsi': float(row['RSI']) if not pd.isna(row['RSI']) else None,
                'macd': macd_val,
                'macd_signal': sig_val,
                'macd_hist': hist_val
            })
        
        # Get news
        stock_news = news_fetcher.get_news(ticker, limit=10) # Increased limit
        
        return jsonify({
            'success': True,
            'ticker': ticker,
            'analysis': {
                'decision': decision,
                'confidence': confidence,
                'signals': signals
            },
            'price': {
                'current': latest_price,
                'previous': prev_price,
                'change': price_change,
                'change_percent': price_change_pct,
                'high': period_high, # Period High
                'low': period_low,   # Period Low
                'volume': int(latest['Volume'])
            },
            'indicators': {
                'sma_5': float(latest['SMA_5']) if not pd.isna(latest['SMA_5']) else 0,
                'sma_20': float(latest['SMA_20']) if not pd.isna(latest['SMA_20']) else 0,
                'rsi': float(latest['RSI']) if not pd.isna(latest['RSI']) else 0,
                'macd': float(latest['MACD']) if not pd.isna(latest['MACD']) else 0,
                'macd_signal': float(latest['MACD_Signal']) if not pd.isna(latest['MACD_Signal']) else 0,
                'ema_12': float(latest['EMA_12']) if not pd.isna(latest['EMA_12']) else 0,
                'ema_26': float(latest['EMA_26']) if not pd.isna(latest['EMA_26']) else 0
            },
            'chart_data': chart_data,
            'news': stock_news if stock_news else []
        })
        
    except Exception as e:
        print(f"Error in analysis: {e}") # Debug print
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/portfolio/generate', methods=['POST'])
def generate_portfolio():
    """Generate AI-powered portfolio based on budget and risk level"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'budget' not in data:
            return jsonify({
                'success': False,
                'error': 'Budget is required'
            }), 400
        
        budget = float(data['budget'])
        risk_level = data.get('risk_level', 'moderate').lower()
        
        # Validate budget
        if budget < 1000:
            return jsonify({
                'success': False,
                'error': 'Budget must be at least PKR 1,000'
            }), 400
        
        # Validate risk level
        if risk_level not in ['conservative', 'moderate', 'aggressive']:
            return jsonify({
                'success': False,
                'error': 'Invalid risk level. Must be conservative, moderate, or aggressive'
            }), 400
        
        # Generate portfolio
        portfolio = portfolio_ai.generate_portfolio(budget, risk_level)
        
        return jsonify(portfolio)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/market-scan', methods=['GET'])
def market_scan():
    """Scan market for buy/sell signals (Parallel Execution)"""
    try:
        scan_type = request.args.get('type', 'all')  # all, buy, sell
        
        results = []
        
        # Use ThreadPoolExecutor for parallel processing
        # Significantly speeds up scanning 30+ stocks
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ticker = {executor.submit(analyze_single_stock_safe, ticker): ticker for ticker in ALL_PSX_STOCKS}
            
            for future in concurrent.futures.as_completed(future_to_ticker):
                result = future.result()
                if result:
                    # Filter based on scan type
                    if scan_type == 'buy' and result['signal'] == 'BUY':
                        results.append(result)
                    elif scan_type == 'sell' and result['signal'] == 'SELL':
                        results.append(result)
                    elif scan_type == 'all':
                        results.append(result)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/market-status', methods=['GET'])
def market_status():
    """Get overall market status for dashboard"""
    try:
        # Quick scan of top stocks for dashboard
        quick_list = ALL_PSX_STOCKS[:10]  # Just check top 10 for speed on dashboard load
        
        buy_count = 0
        sell_count = 0
        hold_count = 0
        
        # We can implement a caching mechanism here later if needed
        # For now, let's keep it lightweight or rely on the frontend to call market-scan
        
        return jsonify({
            'success': True,
            'total_stocks': len(ALL_PSX_STOCKS),
            'status': 'Open',
            'message': 'Market data ready'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/news/<ticker>', methods=['GET'])
def get_stock_news(ticker):
    """Get news for a specific stock"""
    try:
        limit = int(request.args.get('limit', 5))
        news = news_fetcher.get_news(ticker, limit=limit)
        
        return jsonify({
            'success': True,
            'ticker': ticker,
            'news': news if news else []
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("PSX Stock Advisor - Flask API Server (Optimized)")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
