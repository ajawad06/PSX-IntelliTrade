

# ============================================================================
# FILE: app.py
# Description: Interactive Streamlit application with Auto-refresh & Portfolio
# ============================================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Import our modules
from data_fetcher import StockDataFetcher
from indicators import TechnicalIndicators
from rule_engine import RuleEngine
from news_fetcher import NewsFetcher
from teaching_mode import TeachingMode

# Page config
st.set_page_config(page_title="PSX AI Stock Advisor", page_icon="📈", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .buy-signal {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    .sell-signal {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
    }
    .hold-signal {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    .info-box {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .stock-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stock-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-3px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache(allow_output_mutation=True)
def init_components():
    return {
        'fetcher': StockDataFetcher(),
        'engine': RuleEngine(),
        'news': NewsFetcher(),
        'teacher': TeachingMode()
    }

components = init_components()

# Initialize session state
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "HBL"
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["HBL", "OGDC", "PSO"]

# All PSX stocks (expanded list)
all_psx_stocks = [
    "HBL", "OGDC", "PSO", "ENGRO", "MCB", "UBL", "LUCK", "FFC", "MEBL", "PPL",
    "HUBC", "MARI", "TRG", "SYS", "EFERT", "KAPCO", "NBP", "BAFL", "ABL", "SNGP",
    "POL", "DGKC", "MLCF", "PTC", "KEL", "FCCL", "HASCOL", "APL", "ICI", "DAWH",
    "CHCC", "COLG", "NML", "NESTLE", "FHAM", "PIOC", "PAEL", "BYCO", "SEARL", "SHEL"
]

# Sidebar
st.sidebar.markdown("# PSX Stock Advisor")
st.sidebar.markdown("---")

# Auto-refresh toggle
st.sidebar.markdown("### Live Mode")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=st.session_state.auto_refresh)
st.session_state.auto_refresh = auto_refresh

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio("", ["Stock Analysis", "Portfolio Builder", "Learning Center", "Market Scanner"])

# Watchlist
st.sidebar.markdown("---")
st.sidebar.markdown("### Your Watchlist")
for stock in st.session_state.watchlist:
    if st.sidebar.button(f"{stock}"):
        st.session_state.current_ticker = stock

# Add to watchlist
new_watch = st.sidebar.text_input("Add stock to watchlist", "").upper()
if st.sidebar.button("Add") and new_watch and new_watch not in st.session_state.watchlist:
    st.session_state.watchlist.append(new_watch)
    st.sidebar.success(f"Added {new_watch}!")

if page == "Stock Analysis":
    # Header
    st.markdown('<div class="main-header">Pakistan Stock Exchange - Stock Advisor</div>', unsafe_allow_html=True)
    st.markdown("### Technical Analysis & Trading Signals")
    st.markdown("---")
    
    # Search with autocomplete effect
    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    
    with col1:
        ticker = st.selectbox("Select PSX Stock Ticker", all_psx_stocks, 
                             index=all_psx_stocks.index(st.session_state.current_ticker) if st.session_state.current_ticker in all_psx_stocks else 0)
        st.session_state.current_ticker = ticker
    
    with col2:
        period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    with col3:
        if st.button("Analyze"):
            pass
    
    with col4:
        if st.button("Add to Watchlist"):
            if ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(ticker)
                st.success(f"Added to watchlist!")
    
    st.markdown("---")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        placeholder = st.empty()
        with placeholder.container():
            st.info("Auto-refresh enabled. Data refreshes every 30 seconds...")
    
    with st.spinner("Fetching and analyzing data... Please wait..."):
        # Fetch data
        data, error = components['fetcher'].get_stock_data(ticker, period)
        
        if error:
            st.error(f"Error: {error}")
            st.info("**Troubleshooting Tips:**")
            st.markdown("""
            - Try selecting a different stock from the dropdown
            - Check your internet connection
            - Some stocks may have limited historical data
            - Try a shorter time period (e.g., 1mo instead of 1y)
            """)
            st.warning(f"Unable to fetch data for **{ticker}**. Please try another stock.")
        else:
            # Get latest data date
            from datetime import datetime
            latest_data_date = data.index[-1]
            latest_date_str = latest_data_date.strftime('%B %d, %Y') if hasattr(latest_data_date, 'strftime') else str(latest_data_date)
            current_date = datetime.now().date()
            data_date = latest_data_date.date() if hasattr(latest_data_date, 'date') else latest_data_date
            
            # Success message
            st.success(f"Successfully loaded data for **{ticker}** ({len(data)} data points)")
            
            # Show data date with warning if not current
            if data_date < current_date:
                days_old = (current_date - data_date).days
                st.warning(f"**Latest Available Data:** {latest_date_str} ({days_old} day(s) old)")
                st.info("**Note:** Data for PSX stocks may have a 1-day delay. This is normal for international data providers.")
            else:
                st.info(f"**Latest Data:** {latest_date_str} (Current)")
            
            # Add indicators
            data = TechnicalIndicators.add_all_indicators(data)
            
            # Get decision
            decision, confidence, signals = components['engine'].analyze(data)
            
            # Latest data
            latest = data.iloc[-1]
            prev = data.iloc[-2]
            latest_price = latest['Close']
            prev_price = prev['Close']
            price_change = latest_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            # Trading Decision
            st.markdown("## TRADING RECOMMENDATION")
            
            if decision == "BUY":
                st.markdown(f'<div class="buy-signal">STRONG BUY SIGNAL</div>', unsafe_allow_html=True)
            elif decision == "SELL":
                st.markdown(f'<div class="sell-signal">STRONG SELL SIGNAL</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hold-signal">HOLD POSITION</div>', unsafe_allow_html=True)
            
            st.markdown("")
            
            # Key metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Current Price", f"PKR {latest_price:.2f}", f"{price_change:.2f} PKR ({price_change_pct:+.2f}%)")
            with col2:
                st.metric("Confidence", f"{confidence}%")
            with col3:
                st.metric("Volume", f"{int(latest['Volume']):,}")
            with col4:
                st.metric("Day High", f"PKR {latest['High']:.2f}")
            with col5:
                st.metric("Day Low", f"PKR {latest['Low']:.2f}")
            
            st.markdown("---")
            
            # Analysis Signals
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Trading Signals")
                for signal in signals:
                    if "BULLISH" in signal or "✅" in signal:
                        st.success(signal)
                    elif "BEARISH" in signal or "❌" in signal:
                        st.error(signal)
                    else:
                        st.info(signal)
            
            with col2:
                st.markdown("### 📈 Key Indicators")
                st.markdown(f"**SMA (5):** {latest['SMA_5']:.2f} PKR")
                st.markdown(f"**SMA (20):** {latest['SMA_20']:.2f} PKR")
                st.markdown(f"**RSI (14):** {latest['RSI']:.2f}")
                st.markdown(f"**MACD:** {latest['MACD']:.2f}")
                st.markdown(f"**EMA (12):** {latest['EMA_12']:.2f} PKR")
            
            st.markdown("---")
            
            # Interactive Charts
            st.markdown("## 📈 INTERACTIVE CHARTS")
            
            # Tabs for different chart views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Price & Volume", "⚡ RSI", "📉 MACD", "📋 Data Table"])
            
            with tab1:
                fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                    vertical_spacing=0.03, row_heights=[0.7, 0.3])
                
                fig1.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                             low=data['Low'], close=data['Close'], name='OHLC'), row=1, col=1)
                fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_5'], name='SMA 5', 
                                         line=dict(color='orange', width=2)), row=1, col=1)
                fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', 
                                         line=dict(color='blue', width=2)), row=1, col=1)
                
                colors = ['red' if data['Close'].iloc[i] < data['Open'].iloc[i] else 'green' 
                         for i in range(len(data))]
                fig1.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', 
                                     marker_color=colors), row=2, col=1)
                
                fig1.update_layout(height=700, showlegend=True, xaxis_rangeslider_visible=False)
                st.plotly_chart(fig1, use_container_width=True)
            
            with tab2:
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', 
                                         line=dict(color='purple', width=2)))
                fig2.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                fig2.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                fig2.update_layout(height=400, yaxis_range=[0, 100])
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab3:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', 
                                         line=dict(color='blue', width=2)))
                fig3.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal', 
                                         line=dict(color='red', width=2)))
                fig3.add_trace(go.Bar(x=data.index, y=data['MACD_Hist'], name='Histogram'))
                fig3.update_layout(height=400)
                st.plotly_chart(fig3, use_container_width=True)
            
            with tab4:
                st.dataframe(data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_5', 
                                  'SMA_20', 'RSI', 'MACD']].tail(30))
            
            st.markdown("---")
            
            # Stock-specific News
            st.markdown(f"## 📰 LATEST NEWS FOR {ticker}")
            news = components['news'].get_news(ticker, limit=5)
            
            if news:
                for idx, item in enumerate(news, 1):
                    # Clean HTML tags from summary
                    import re
                    clean_summary = re.sub(r'<[^>]+>', '', item['summary'])
                    clean_summary = clean_summary.replace('&nbsp;', ' ').replace('&amp;', '&')
                    
                    with st.expander(f"📌 {item['title']}"):
                        st.markdown(f"**Published:** {item['published']}")
                        st.markdown(clean_summary)
                        st.markdown(f"[🔗 Read Full Article]({item['link']})")
            else:
                st.warning(f"No specific news for {ticker}. Showing general PSX news...")
                general_news = components['news'].get_news(None, limit=5)
                for idx, item in enumerate(general_news, 1):
                    # Clean HTML tags from summary
                    import re
                    clean_summary = re.sub(r'<[^>]+>', '', item['summary'])
                    clean_summary = clean_summary.replace('&nbsp;', ' ').replace('&amp;', '&')
                    
                    with st.expander(f"📌 {item['title']}"):
                        st.markdown(f"**Published:** {item['published']}")
                        st.markdown(clean_summary)
                        st.markdown(f"[🔗 Read Full Article]({item['link']})")

elif page == "💰 Portfolio Builder":
    st.markdown('<div class="main-header">💰 Smart Portfolio Builder</div>', unsafe_allow_html=True)
    st.markdown("### Tell us your budget and get personalized stock recommendations!")
    st.markdown("---")
    
    # User input
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.number_input("💵 Enter your investment budget (PKR)", min_value=1000, 
                                max_value=10000000, value=100000, step=1000)
    
    with col2:
        risk_level = st.selectbox("⚠️ Risk Tolerance", ["Conservative (Low Risk)", 
                                                        "Moderate (Medium Risk)", 
                                                        "Aggressive (High Risk)"])
    
    if st.button("🎯 Generate Portfolio Recommendation"):
        with st.spinner("🔄 Analyzing stocks and building your portfolio..."):
            st.markdown("## 📊 Your Personalized Portfolio")
            
            # Analyze top stocks
            recommendations = []
            
            for stock in all_psx_stocks[:15]:  # Analyze top 15 stocks
                try:
                    data, error = components['fetcher'].get_stock_data(stock, "3mo")
                    if data is not None and not data.empty:
                        data = TechnicalIndicators.add_all_indicators(data)
                        decision, confidence, signals = components['engine'].analyze(data)
                        
                        latest_price = data['Close'].iloc[-1]
                        
                        if decision == "BUY" and confidence >= 60:
                            recommendations.append({
                                'stock': stock,
                                'price': latest_price,
                                'confidence': confidence,
                                'decision': decision
                            })
                except:
                    continue
            
            # Sort by confidence
            recommendations.sort(key=lambda x: x['confidence'], reverse=True)
            
            if recommendations:
                st.success(f"✅ Found {len(recommendations)} recommended stocks based on technical analysis!")
                
                # Calculate allocation based on risk level
                num_stocks = min(3, len(recommendations))  # Diversify into 3 stocks
                
                st.markdown("### 🎯 Recommended Stock Allocation")
                st.markdown(f"**Your Budget:** PKR {budget:,}")
                st.markdown(f"**Risk Level:** {risk_level}")
                st.markdown("---")
                
                portfolio_items = []
                total_invested = 0
                
                for i, rec in enumerate(recommendations[:num_stocks]):
                    # Equal allocation across stocks
                    allocation = budget / num_stocks
                    shares = int(allocation / rec['price'])
                    investment = shares * rec['price']
                    total_invested += investment
                    
                    portfolio_items.append({
                        'stock': rec['stock'],
                        'price': rec['price'],
                        'shares': shares,
                        'investment': investment,
                        'confidence': rec['confidence']
                    })
                    
                    # Display each stock
                    st.markdown(f"### 📌 Stock {i+1}: {rec['stock']}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"**Signal:** 🟢 {rec['decision']}")
                        st.markdown(f"**Confidence:** {rec['confidence']}%")
                    
                    with col2:
                        st.metric("Price per Share", f"PKR {rec['price']:.2f}")
                    
                    with col3:
                        st.metric("Shares to Buy", f"{shares}")
                    
                    with col4:
                        st.metric("Total Cost", f"PKR {investment:,.2f}")
                        percentage = (investment / budget) * 100
                        st.markdown(f"*{percentage:.1f}% of portfolio*")
                    
                    st.markdown("---")
                
                # Portfolio Summary
                remaining = budget - total_invested
                
                st.markdown("### 💼 Portfolio Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💰 Total Budget", f"PKR {budget:,}")
                with col2:
                    st.metric("📊 Total Invested", f"PKR {total_invested:,.2f}")
                with col3:
                    st.metric("💵 Cash Remaining", f"PKR {remaining:,.2f}")
                with col4:
                    invested_pct = (total_invested / budget) * 100
                    st.metric("% Invested", f"{invested_pct:.1f}%")
                
                # Detailed breakdown table
                st.markdown("### 📋 Detailed Breakdown")
                import pandas as pd
                df_portfolio = pd.DataFrame(portfolio_items)
                df_portfolio.columns = ['Stock', 'Price (PKR)', 'Shares', 'Investment (PKR)', 'Confidence (%)']
                st.dataframe(df_portfolio, use_container_width=True)
                
                st.markdown("---")
                st.info("💡 **Note:** This is an AI-generated recommendation based on technical analysis. Always do your own research and consult a financial advisor before investing!")
            else:
                st.warning("⚠️ No BUY recommendations found at the moment. Market conditions may not be favorable. Try again later!")

elif page == "📚 Learning Center":
    st.markdown('<div class="main-header">📚 Stock Market Learning Center</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Interactive learning mode
    st.markdown("### 🎓 Choose Your Learning Path")
    
    learning_mode = st.radio("", ["📖 Basic Concepts", "📊 Technical Analysis", "💰 Investment Strategy"])
    
    if learning_mode == "📖 Basic Concepts":
        lessons = components['teacher'].get_basics()
        
        for title, content in lessons.items():
            with st.expander(f"📖 {title}"):
                st.markdown(content)
        
        # Interactive Quiz
        st.markdown("---")
        st.markdown("### 🎯 Test Your Knowledge!")
        
        q1 = st.radio("What does RSI below 30 indicate?", 
                     ["Overbought", "Oversold", "Neutral", "Bullish Trend"])
        
        if st.button("Check Answer"):
            if q1 == "Oversold":
                st.success("✅ Correct! RSI below 30 means the stock is oversold and might be a good buy.")
            else:
                st.error("❌ Wrong! RSI below 30 indicates the stock is oversold.")
    
    elif learning_mode == "📊 Technical Analysis":
        st.markdown("### 📊 Understanding Technical Indicators")
        
        indicator = st.selectbox("Choose an indicator to learn about:", 
                                ["SMA", "RSI", "MACD", "Volume", "Support & Resistance"])
        
        if indicator == "SMA":
            st.markdown("""
            ### Simple Moving Average (SMA)
            
            **What is it?**  
            SMA calculates the average price over a specific period.
            
            **How to use it?**
            - **Golden Cross:** When SMA(5) crosses above SMA(20) = BUY signal
            - **Death Cross:** When SMA(5) crosses below SMA(20) = SELL signal
            
            **Example:**
            If a stock's SMA(5) = 150 and SMA(20) = 145, and yesterday SMA(5) was 143,
            this is a bullish crossover!
            """)
        
        elif indicator == "RSI":
            st.markdown("""
            ### Relative Strength Index (RSI)
            
            **What is it?**  
            RSI measures momentum on a scale of 0-100.
            
            **Trading Rules:**
            - **RSI < 30:** Stock is oversold → Consider BUYING
            - **RSI > 70:** Stock is overbought → Consider SELLING
            - **RSI 30-70:** Neutral zone
            
            **Pro Tip:**  
            Combine RSI with other indicators for better accuracy!
            """)
    
    elif learning_mode == "💰 Investment Strategy":
        st.markdown("### 💰 Building Your Investment Strategy")
        
        st.markdown("""
        #### Step 1: Set Your Goals
        - Short-term (< 1 year)
        - Medium-term (1-3 years)
        - Long-term (> 3 years)
        
        #### Step 2: Assess Risk Tolerance
        - Conservative: Focus on stable, dividend-paying stocks
        - Moderate: Mix of growth and stable stocks
        - Aggressive: Growth stocks with higher volatility
        
        #### Step 3: Diversification
        - Don't put all money in one stock
        - Spread across different sectors
        - Keep some cash reserves
        
        #### Step 4: Regular Monitoring
        - Review portfolio monthly
        - Rebalance when needed
        - Stay informed about market news
        """)

elif page == "📊 Market Scanner":
    st.markdown('<div class="main-header">📊 Real-time Market Scanner</div>', unsafe_allow_html=True)
    st.markdown("### Scan all PSX stocks for trading opportunities")
    st.markdown("---")
    
    scan_type = st.radio("🔍 Scan for:", ["🟢 BUY Signals", "🔴 SELL Signals", "📊 All Stocks"])
    
    if st.button("🚀 Start Scanning"):
        progress_bar = st.progress(0)
        results = []
        
        for idx, stock in enumerate(all_psx_stocks):
            try:
                data, error = components['fetcher'].get_stock_data(stock, "1mo")
                if data is not None and not data.empty:
                    data = TechnicalIndicators.add_all_indicators(data)
                    decision, confidence, signals = components['engine'].analyze(data)
                    
                    latest_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[0]
                    change_pct = ((latest_price - prev_price) / prev_price) * 100
                    
                    results.append({
                        'Stock': stock,
                        'Price': f"PKR {latest_price:.2f}",
                        'Change': f"{change_pct:+.2f}%",
                        'Signal': decision,
                        'Confidence': f"{confidence}%",
                        'RSI': f"{data['RSI'].iloc[-1]:.2f}"
                    })
                
                progress_bar.progress((idx + 1) / len(all_psx_stocks))
                time.sleep(0.1)  # Small delay to show progress
            except:
                continue
        
        # Filter results
        if scan_type == "🟢 BUY Signals":
            results = [r for r in results if r['Signal'] == 'BUY']
        elif scan_type == "🔴 SELL Signals":
            results = [r for r in results if r['Signal'] == 'SELL']
        
        if results:
            st.success(f"✅ Found {len(results)} stocks!")
            
            # Display as interactive table
            df = pd.DataFrame(results)
            st.dataframe(df)
            
            # Download option
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Results", csv, "psx_scan.csv", "text/csv")
        else:
            st.warning("⚠️ No stocks found matching your criteria.")

# Auto-refresh implementation
if st.session_state.auto_refresh and page == "🏠 Stock Analysis":
    time.sleep(30)
    st.rerun()

# Enhanced Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.info(f"""
**Total Stocks:** {len(all_psx_stocks)}  
**Watchlist:** {len(st.session_state.watchlist)}  
**Last Update:** {datetime.now().strftime('%H:%M:%S')}
""")

st.sidebar.markdown("---")
st.sidebar.warning("""
**⚠️ Disclaimer**

This app is for educational purposes only. Not financial advice. Always consult professionals before trading.
""")
