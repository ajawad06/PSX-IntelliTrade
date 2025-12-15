# ============================================================================
# FILE: news_fetcher.py
# Description: Fetch 2025 stock-specific news (Stable Version)
# ============================================================================

import feedparser
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re

class NewsFetcher:
    """Fetch 2025 stock-specific news"""
    
    def __init__(self):
        # ONLY Dawn News
        self.general_feeds = [
            "https://www.dawn.com/feeds/business",
        ]
        # Only 2025 news
        self.cutoff_date = datetime(2025, 1, 1)
    
    def get_news(self, keyword=None, limit=5):
        """Fetch news - ONLY stock-specific if keyword provided"""
        if keyword:
            return self._get_stock_specific_news(keyword, limit)
        else:
            return self._get_general_news(limit)
    
    def _parse_date(self, date_string):
        """Parse date from various formats"""
        if not date_string or date_string == 'N/A':
            return None
            
        try:
            # Remove timezone info
            date_string = str(date_string).split('+')[0].split('-', 3)[-1] if '+' in str(date_string) else str(date_string)
            date_string = date_string.strip()
            
            # Try multiple date formats
            for fmt in [
                '%a, %d %b %Y %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%d %b %Y %H:%M:%S',
                '%Y-%m-%d',
                '%d %b %Y'
            ]:
                try:
                    parsed = datetime.strptime(date_string.split('.')[0].strip(), fmt)
                    return parsed
                except:
                    continue
            
            # Try to extract year at least
            year_match = re.search(r'202[45]', date_string)
            if year_match:
                year = int(year_match.group())
                return datetime(year, 1, 1)
                
            return None
        except:
            return None
    
    def _is_from_2025(self, date_string):
        """Check if news is from 2025"""
        if not date_string or date_string == 'N/A':
            return True
        
        parsed_date = self._parse_date(date_string)
        if parsed_date:
            return parsed_date >= self.cutoff_date
        
        if '2025' in str(date_string):
            return True
            
        return True
    
    def _get_stock_specific_news(self, stock_ticker, limit=8):
        """Return only general PSX market news (no stock-specific filtering)"""
        
        print(f"\n{'='*60}")
        print(f"📰 Fetching general PSX market news for {stock_ticker}")
        print(f"{'='*60}\n")
        
        # Just return general PSX market news for all stocks
        general_news = self._get_general_psx_news(limit=limit)
        
        print(f"\n{'='*60}")
        print(f"✅ Returning {len(general_news)} general PSX market news items")
        print(f"{'='*60}\n")
        
        return general_news if general_news else None
    
    def _get_general_psx_news(self, limit=5):
        """Fetch general PSX/business news from Dawn.com"""
        all_news = []
        try:
            dawn_rss = "https://www.dawn.com/feeds/business"
            feed = feedparser.parse(dawn_rss)
            
            psx_keywords = ['psx', 'pakistan stock exchange', 'karachi stock exchange', 
                          'stock market', 'stocks', 'shares', 'trading']
            
            for entry in feed.entries[:20]:
                title_lower = entry.title.lower()
                summary_lower = entry.get('summary', '').lower()
                
                # Check if it's PSX-related
                is_psx_news = any(keyword in title_lower or keyword in summary_lower 
                                 for keyword in psx_keywords)
                
                if is_psx_news:
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', 'Recent'),
                        'summary': entry.get('summary', entry.title)[:250],
                        'source': 'PSX Market News'
                    }
                    all_news.append(news_item)
                    
                    if len(all_news) >= limit:
                        break
        except Exception as e:
            print(f"General news error: {e}")
            
        return all_news
    
    def _get_general_news(self, limit=5):
        """Fetch general business news from Dawn.com"""
        return self._get_general_psx_news(limit)
    
    def _get_company_keywords(self, ticker):
        """Get company name keywords for news matching"""
        company_map = {
            'HBL': ['Habib Bank', 'HBL Bank', 'HBL Limited'],
            'OGDC': ['Oil and Gas Development', 'OGDC', 'Oil Gas Development'],
            'PSO': ['Pakistan State Oil', 'PSO'],
            'LUCK': ['Lucky Cement', 'Lucky'],
            'ENGRO': ['Engro Corporation', 'Engro'],
            'MCB': ['MCB Bank', 'Muslim Commercial Bank'],
            'UBL': ['United Bank', 'UBL'],
            'FFC': ['Fauji Fertilizer', 'FFC'],
            'MEBL': ['Meezan Bank', 'MEBL'],
            'PPL': ['Pakistan Petroleum', 'PPL'],
            'HUBC': ['Hub Power', 'HUBC'],
            'MARI': ['Mari Petroleum', 'MARI'],
            'TRG': ['TRG Pakistan', 'TRG'],
            'SYS': ['Systems Limited', 'Systems'],
            'EFERT': ['Engro Fertilizer', 'Efert'],
            'KAPCO': ['Kot Addu', 'KAPCO'],
            'NBP': ['National Bank', 'NBP'],
            'BAFL': ['Bank Alfalah', 'Alfalah'],
            'ABL': ['Allied Bank', 'ABL'],
            'SNGP': ['Sui Northern Gas', 'SNGP'],
            'POL': ['Pakistan Oilfields', 'POL'],
            'DGKC': ['DG Khan Cement', 'DGKC'],
            'MLCF': ['Maple Leaf', 'MLCF'],
            'PTC': ['Pakistan Tobacco', 'PTC'],
            'KEL': ['K-Electric', 'KEL', 'KE'],
            'FCCL': ['Fauji Cement', 'FCCL'],
            'HASCOL': ['Hascol Petroleum', 'Hascol'],
            'APL': ['Attock Petroleum', 'APL'],
            'ICI': ['ICI Pakistan', 'ICI'],
            'NESTLE': ['Nestle Pakistan', 'Nestle'],
            'COLG': ['Colgate Palmolive', 'Colgate'],
            'NML': ['Nishat Mills', 'NML'],
        }
        return company_map.get(ticker, [ticker])