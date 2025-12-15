# ============================================================================
# FILE: rule_engine.py
# Description: Rule-based decision engine for buy/sell/hold signals
# ============================================================================

class RuleEngine:
    """Rule-based decision engine for stock trading signals"""
    
    def __init__(self):
        self.signals = []
        self.decision = "HOLD"
        self.confidence = 0
    
    def analyze(self, data):
        """Analyze stock data and generate signals"""
        self.signals = []
        buy_score = 0
        sell_score = 0
        
        # Get latest values
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        sma_5 = latest['SMA_5']
        sma_20 = latest['SMA_20']
        prev_sma_5 = prev['SMA_5']
        prev_sma_20 = prev['SMA_20']
        rsi = latest['RSI']
        macd = latest['MACD']
        macd_signal = latest['MACD_Signal']
        volume = latest['Volume']
        avg_volume = data['Volume'].tail(20).mean()
        price = latest['Close']
        
        # Rule 1: SMA Crossover with Volume (HIGHER WEIGHT)
        if prev_sma_5 <= prev_sma_20 and sma_5 > sma_20:
            if volume > avg_volume * 1.2:
                buy_score += 4  # Increased from 3
                self.signals.append("✅ BULLISH: SMA(5) crossed above SMA(20) with high volume")
            else:
                buy_score += 2  # Increased from 1
                self.signals.append("⚠️ SMA(5) crossed above SMA(20) but volume is low")
        
        elif prev_sma_5 >= prev_sma_20 and sma_5 < sma_20:
            sell_score += 4  # Increased from 3
            self.signals.append("❌ BEARISH: SMA(5) crossed below SMA(20)")
        
        # Rule 2: Price position relative to SMAs
        if price > sma_5 and sma_5 > sma_20:
            buy_score += 2  # Strong uptrend
            self.signals.append("✅ BULLISH: Price > SMA(5) > SMA(20) - Strong uptrend")
        elif price < sma_5 and sma_5 < sma_20:
            sell_score += 2  # Strong downtrend
            self.signals.append("❌ BEARISH: Price < SMA(5) < SMA(20) - Strong downtrend")
        
        # Rule 3: RSI Oversold/Overbought (MORE DECISIVE)
        if rsi < 35:  # Changed from 30
            buy_score += 3  # Increased from 2
            self.signals.append(f"✅ BULLISH: RSI is oversold ({rsi:.2f})")
        elif rsi > 65:  # Changed from 70
            sell_score += 3  # Increased from 2
            self.signals.append(f"❌ BEARISH: RSI is overbought ({rsi:.2f})")
        elif 45 <= rsi <= 55:
            self.signals.append(f"➖ NEUTRAL: RSI is neutral ({rsi:.2f})")
        elif rsi < 45:
            buy_score += 1  # Slightly oversold
            self.signals.append(f"⚠️ RSI trending lower ({rsi:.2f})")
        else:
            sell_score += 1  # Slightly overbought
            self.signals.append(f"⚠️ RSI trending higher ({rsi:.2f})")
        
        # Rule 4: MACD Signal (HIGHER WEIGHT)
        if macd > macd_signal and prev['MACD'] <= prev['MACD_Signal']:
            buy_score += 3  # Increased from 2
            self.signals.append("✅ BULLISH: MACD crossed above signal line")
        elif macd < macd_signal and prev['MACD'] >= prev['MACD_Signal']:
            sell_score += 3  # Increased from 2
            self.signals.append("❌ BEARISH: MACD crossed below signal line")
        elif macd > macd_signal:
            buy_score += 1
            self.signals.append("✅ MACD above signal line")
        else:
            sell_score += 1
            self.signals.append("❌ MACD below signal line")
        
        # Rule 5: Volume Analysis
        if volume > avg_volume * 1.5:
            self.signals.append("📊 High volume detected - Strong momentum")
            # Add score based on price direction
            if price > prev['Close']:
                buy_score += 1
            else:
                sell_score += 1
        
        # Make decision (LOWER THRESHOLDS FOR MORE DECISIVE SIGNALS)
        if buy_score > sell_score and buy_score >= 2:
            self.decision = "BUY"
            # Boost confidence: Base 60% + (score * 5)
            # Score 2 -> 70%, Score 4 -> 80%, Score 6 -> 90%
            self.confidence = min(60 + (buy_score * 5), 95)
            
        elif sell_score > buy_score and sell_score >= 2:
            self.decision = "SELL"
            self.confidence = min(60 + (sell_score * 5), 95)
            
        else:
            self.decision = "HOLD"
            self.confidence = 50
            
        return self.decision, self.confidence, self.signals
