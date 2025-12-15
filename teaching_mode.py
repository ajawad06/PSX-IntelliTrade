# ============================================================================
# FILE: teaching_mode.py
# Description: Educational content for beginners
# ============================================================================

class TeachingMode:
    """Educational content for stock market beginners"""
    
    @staticmethod
    def get_basics():
        return {
            "What is a Stock?": """
            A stock represents ownership in a company. When you buy a stock, 
            you become a shareholder and own a small piece of that company.
            Stocks can increase or decrease in value based on company performance 
            and market conditions.
            """,
            
            "What is PSX?": """
            Pakistan Stock Exchange (PSX) is the main stock exchange in Pakistan.
            It was formed in 2016 by merging Karachi, Lahore, and Islamabad 
            stock exchanges. Major companies like HBL, OGDC, PSO trade on PSX.
            """,
            
            "What is SMA?": """
            Simple Moving Average (SMA) smooths price data by creating an average 
            price over a specific period. SMA(5) is 5-day average, SMA(20) is 20-day.
            When SMA(5) crosses above SMA(20), it's often a bullish signal.
            """,
            
            "What is RSI?": """
            Relative Strength Index (RSI) measures if a stock is overbought or oversold.
            - RSI < 30: Oversold (might be a good time to buy)
            - RSI > 70: Overbought (might be a good time to sell)
            - RSI 30-70: Neutral zone
            """,
            
            "What is Volume?": """
            Volume is the number of shares traded in a period. High volume with 
            price increase shows strong buying interest. High volume with price 
            decrease shows strong selling pressure.
            """,
            
            "What is MACD?": """
            Moving Average Convergence Divergence (MACD) shows the relationship 
            between two moving averages. When MACD crosses above the signal line, 
            it's bullish. When it crosses below, it's bearish.
            """,
            
            "How Decisions Are Made?": """
            This app uses rule-based analysis:
            1. Calculates technical indicators (SMA, RSI, MACD)
            2. Checks for bullish/bearish patterns
            3. Assigns scores based on signals
            4. Recommends BUY/SELL/HOLD based on total score
            
            Remember: This is for educational purposes. Always do your own research!
            """
        }
