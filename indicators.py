
# ============================================================================
# FILE: indicators.py
# Description: Calculate technical indicators with robust error handling
# ============================================================================

import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Calculate technical indicators for stock analysis"""
    
    @staticmethod
    def calculate_sma(data, period):
        """Calculate Simple Moving Average"""
        try:
            if len(data) < period:
                return pd.Series([np.nan] * len(data), index=data.index)
            return data['Close'].rolling(window=period, min_periods=1).mean()
        except Exception as e:
            return pd.Series([np.nan] * len(data), index=data.index)
    
    @staticmethod
    def calculate_ema(data, period):
        """Calculate Exponential Moving Average"""
        try:
            if len(data) < period:
                return pd.Series([np.nan] * len(data), index=data.index)
            return data['Close'].ewm(span=period, adjust=False, min_periods=1).mean()
        except Exception as e:
            return pd.Series([np.nan] * len(data), index=data.index)
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """Calculate Relative Strength Index"""
        try:
            if len(data) < period + 1:
                return pd.Series([50] * len(data), index=data.index)  # Neutral RSI
            
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()
            
            # Avoid division by zero
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            
            # Fill NaN values with neutral RSI
            rsi = rsi.fillna(50)
            
            return rsi
        except Exception as e:
            return pd.Series([50] * len(data), index=data.index)
    
    @staticmethod
    def calculate_macd(data):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            if len(data) < 26:
                # Return zeros if insufficient data
                zeros = pd.Series([0] * len(data), index=data.index)
                return zeros, zeros, zeros
            
            ema_12 = data['Close'].ewm(span=12, adjust=False, min_periods=1).mean()
            ema_26 = data['Close'].ewm(span=26, adjust=False, min_periods=1).mean()
            
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9, adjust=False, min_periods=1).mean()
            histogram = macd_line - signal_line
            
            return macd_line, signal_line, histogram
        except Exception as e:
            zeros = pd.Series([0] * len(data), index=data.index)
            return zeros, zeros, zeros
    
    @staticmethod
    def find_support_resistance(data, window=20):
        """Find support and resistance levels"""
        try:
            if len(data) < window:
                # Use available data
                current_support = data['Low'].min() if len(data) > 0 else None
                current_resistance = data['High'].max() if len(data) > 0 else None
                return current_support, current_resistance
            
            # Support: Recent local minima
            support = data['Low'].rolling(window=window, center=True, min_periods=1).min()
            
            # Resistance: Recent local maxima
            resistance = data['High'].rolling(window=window, center=True, min_periods=1).max()
            
            # Get current levels
            current_support = support.dropna().iloc[-1] if not support.dropna().empty else data['Low'].min()
            current_resistance = resistance.dropna().iloc[-1] if not resistance.dropna().empty else data['High'].max()
            
            return current_support, current_resistance
        except Exception as e:
            return None, None
    
    @staticmethod
    def add_all_indicators(data):
        """Add all indicators to the dataframe"""
        try:
            df = data.copy()
            
            # Ensure we have the required columns
            if 'Close' not in df.columns:
                raise ValueError("Data must contain 'Close' column")
            
            # Moving Averages
            df['SMA_5'] = TechnicalIndicators.calculate_sma(df, 5)
            df['SMA_20'] = TechnicalIndicators.calculate_sma(df, 20)
            df['EMA_12'] = TechnicalIndicators.calculate_ema(df, 12)
            df['EMA_26'] = TechnicalIndicators.calculate_ema(df, 26)
            
            # RSI
            df['RSI'] = TechnicalIndicators.calculate_rsi(df, 14)
            
            # MACD
            macd, signal, hist = TechnicalIndicators.calculate_macd(df)
            df['MACD'] = macd
            df['MACD_Signal'] = signal
            df['MACD_Hist'] = hist
            
            # Fill any remaining NaN values with forward fill then backward fill
            df = df.fillna(method='ffill').fillna(method='bfill')
            
            # If still NaN, fill with 0 for indicators
            indicator_cols = ['SMA_5', 'SMA_20', 'EMA_12', 'EMA_26', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist']
            for col in indicator_cols:
                if col in df.columns:
                    df[col] = df[col].fillna(0)
            
            return df
        except Exception as e:
            print(f"Error adding indicators: {e}")
            return data

