
# ============================================================================
# FILE: data_fetcher.py
# Description: Fetches stock data with CURRENT DAY priority from PSX
# ============================================================================

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup

class StockDataFetcher:
    """Fetch stock data for Pakistan Stock Exchange with current day priority"""
    
    def __init__(self):
        self.psx_suffixes = [".KA", ".KARACHI", ""]
        self.max_retries = 3
        self.retry_delay = 1
    
    def _try_multiple_formats(self, ticker, period="1y"):
        """Try fetching data with different ticker formats - ALWAYS include today"""
        base_ticker = ticker.split('.')[0].upper()
        
        # Calculate date range to FORCE today's data
        end_date = datetime.now() + timedelta(days=1)  # Tomorrow to ensure today is included
        
        period_days = {
            '1mo': 35, '3mo': 95, '6mo': 185,
            '1y': 370, '2y': 735, '5y': 1830
        }
        days = period_days.get(period, 370)
        start_date = end_date - timedelta(days=days)
        
        # Try each suffix
        for suffix in self.psx_suffixes:
            try:
                full_ticker = f"{base_ticker}{suffix}"
                stock = yf.Ticker(full_ticker)
                
                # Force download with explicit dates and auto_adjust
                df = stock.history(
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d'),
                    auto_adjust=True,
                    actions=False
                )
                
                # If empty, try with period
                if df.empty:
                    df = stock.history(period=period, auto_adjust=True)
                
                # Check if we got valid data
                if not df.empty and len(df) > 0:
                    # Ensure timezone-naive datetime index
                    if df.index.tz is not None:
                        df.index = df.index.tz_localize(None)
                    
                    return df, None, full_ticker
            except Exception as e:
                continue
        
        return None, "No data found for this ticker with any format", None
    
    def _validate_data(self, df, min_rows=20):
        """Validate that data has sufficient rows for analysis"""
        if df is None or df.empty:
            return False, "No data available"
        
        if len(df) < min_rows:
            return False, f"Insufficient data (only {len(df)} rows, need at least {min_rows})"
        
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {missing_cols}"
        
        nan_percentage = (df[required_cols].isna().sum().sum() / (len(df) * len(required_cols))) * 100
        if nan_percentage > 50:
            return False, f"Too many missing values ({nan_percentage:.1f}%)"
        
        return True, None
    
    def get_stock_data(self, ticker, period="1y"):
        """Fetch historical stock data with retry logic - INCLUDES TODAY"""
        for attempt in range(self.max_retries):
            try:
                # Try multiple ticker formats
                df, error, successful_ticker = self._try_multiple_formats(ticker, period)
                
                if df is not None:
                    # Validate data quality
                    is_valid, validation_error = self._validate_data(df)
                    
                    if is_valid:
                        # Clean the data
                        df = self._clean_data(df)
                        
                        # Force refresh - download latest data again
                        if attempt == 0:
                            # On first attempt, try to get absolute latest
                            try:
                                stock = yf.Ticker(successful_ticker)
                                latest_df = stock.history(period='5d', auto_adjust=True)
                                
                                if not latest_df.empty:
                                    # Merge with existing data, prioritizing latest
                                    if latest_df.index.tz is not None:
                                        latest_df.index = latest_df.index.tz_localize(None)
                                    
                                    # Combine and remove duplicates, keeping latest
                                    df = pd.concat([df, latest_df])
                                    df = df[~df.index.duplicated(keep='last')]
                                    df = df.sort_index()
                            except:
                                pass
                        
                        return df, None
                    else:
                        return None, validation_error
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    return None, error
                    
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    return None, f"Error fetching data: {str(e)}"
        
        return None, "Failed to fetch data after multiple attempts"
    
    def _clean_data(self, df):
        """Clean and prepare data for analysis"""
        df = df.dropna(how='all')
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # Remove timezone if present
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        
        df = df.sort_index()
        return df
    
    def get_company_info(self, ticker):
        """Fetch company profile and fundamentals"""
        try:
            base_ticker = ticker.split('.')[0].upper()
            
            for suffix in self.psx_suffixes:
                try:
                    full_ticker = f"{base_ticker}{suffix}"
                    stock = yf.Ticker(full_ticker)
                    info = stock.info
                    
                    if info and len(info) > 1:
                        company_data = {
                            'name': info.get('longName', info.get('shortName', ticker)),
                            'sector': info.get('sector', 'N/A'),
                            'industry': info.get('industry', 'N/A'),
                            'market_cap': info.get('marketCap', 'N/A'),
                            'pe_ratio': info.get('trailingPE', 'N/A'),
                            'dividend_yield': info.get('dividendYield', 'N/A'),
                            'website': info.get('website', 'N/A'),
                            'description': info.get('longBusinessSummary', 'N/A')
                        }
                        return company_data, None
                except:
                    continue
            
            return None, "Company information not available"
        except Exception as e:
            return None, str(e)
    
    def get_recent_dividends(self, ticker):
        """Fetch dividend history"""
        try:
            base_ticker = ticker.split('.')[0].upper()
            
            for suffix in self.psx_suffixes:
                try:
                    full_ticker = f"{base_ticker}{suffix}"
                    stock = yf.Ticker(full_ticker)
                    dividends = stock.dividends
                    
                    if dividends is not None and len(dividends) > 0:
                        return dividends, None
                except:
                    continue
            
            return None, "No dividend data available"
        except Exception as e:
            return None, str(e)
    
    def get_stock_splits(self, ticker):
        """Fetch stock split history"""
        try:
            base_ticker = ticker.split('.')[0].upper()
            
            for suffix in self.psx_suffixes:
                try:
                    full_ticker = f"{base_ticker}{suffix}"
                    stock = yf.Ticker(full_ticker)
                    splits = stock.splits
                    
                    if splits is not None and len(splits) > 0:
                        return splits, None
                except:
                    continue
            
            return None, "No stock split data available"
        except Exception as e:
            return None, str(e)
