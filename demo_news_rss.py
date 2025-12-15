"""
Quick Demo: Fetching Google News RSS and Converting to JSON
This script shows exactly how your project handles news feeds
"""

import feedparser
import json
from datetime import datetime

def fetch_google_news_rss(ticker):
    """Fetch and parse Google News RSS - Returns clean data (not raw XML!)"""
    print(f"\n{'='*60}")
    print(f"📰 Fetching News for: {ticker}")
    print(f"{'='*60}\n")
    
    # Step 1: Build Google News RSS URL
    search_query = f"{ticker} Pakistan stock"
    google_news_url = f"https://news.google.com/rss/search?q={search_query.replace(' ', '+')}&hl=en-PK&gl=PK&ceid=PK:en"
    
    print(f"🔗 RSS URL: {google_news_url}\n")
    
    # Step 2: Fetch and Parse RSS (feedparser handles all XML)
    print("⏳ Fetching RSS feed...")
    feed = feedparser.parse(google_news_url)
    
    print(f"✅ Fetched {len(feed.entries)} entries from RSS\n")
    
    # Step 3: Convert to clean JSON format
    news_items = []
    for entry in feed.entries[:5]:  # Get top 5
        # Filter out Google error messages
        if 'this feed is not available' in entry.title.lower():
            print(f"⚠️  Skipped error entry: {entry.title}")
            continue
        
        news_item = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', 'N/A'),
            'summary': entry.get('summary', entry.title)[:200] + '...'
        }
        news_items.append(news_item)
    
    print(f"✅ Filtered to {len(news_items)} valid news items\n")
    
    # Step 4: Display as formatted JSON
    print(f"{'='*60}")
    print("📋 CLEAN JSON OUTPUT (No Raw XML!)")
    print(f"{'='*60}\n")
    
    json_output = {
        'success': True,
        'ticker': ticker,
        'count': len(news_items),
        'news': news_items
    }
    
    print(json.dumps(json_output, indent=2, ensure_ascii=False))
    
    # Step 5: Show what the UI would display
    print(f"\n{'='*60}")
    print("🎨 HOW IT LOOKS IN THE UI")
    print(f"{'='*60}\n")
    
    for i, item in enumerate(news_items, 1):
        print(f"📰 News Item #{i}")
        print(f"   Title: {item['title']}")
        print(f"   Date:  {item['published']}")
        print(f"   Link:  {item['link']}")
        print(f"   Summary: {item['summary'][:100]}...")
        print()
    
    return json_output


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 PSX STOCK ADVISOR - NEWS RSS DEMO")
    print("="*60)
    print("\nThis demonstrates how RSS (XML) is converted to clean JSON")
    print("No raw XML will be shown - only beautiful, structured data!\n")
    
    # Test with different stocks
    test_stocks = ['HBL', 'OGDC', 'PSO']
    
    for ticker in test_stocks:
        try:
            result = fetch_google_news_rss(ticker)
            print(f"\n✅ Successfully fetched {result['count']} news items for {ticker}!\n")
        except Exception as e:
            print(f"❌ Error fetching news for {ticker}: {e}\n")
        
        print("\n" + "-"*60 + "\n")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)
    print("\n💡 Key Takeaway:")
    print("   - RSS XML is fetched on the backend (Python)")
    print("   - feedparser converts XML → Python dictionaries")
    print("   - Flask converts Python → JSON")
    print("   - Frontend displays beautiful news cards")
    print("   - Users NEVER see raw XML!")
    print("\n🌐 Try it in the app: http://localhost:8080")
    print("   Go to Stock Analysis → Select HBL → See clean news!\n")
