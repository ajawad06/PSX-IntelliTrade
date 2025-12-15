## NEWS FILTERING FIX - APPLY THIS TO app.js

Find the `displayStockNews` function (line ~312) and replace it with this:

```javascript
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
                
                newsItem.innerHTML = `
                    <div class="news-title">${cleanTitle}</div>
                    <div class="news-published">📅 ${item.published}</div>
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
```

## WHAT IT FILTERS:
- "This feed is not available"
- "For the latest headlines"
- "This XML file"
- "isPermalink"
- "<item>", "<rss>" tags
- "XML feed is made available"
- "news-webmaster@google.com"
- Titles shorter than 15 characters
- Items with just "false"

## HOW TO APPLY:
1. Open c:\Users\ASUS\Desktop\psx_stock_advisor\frontend\app.js
2. Find function displayStockNews (around line 312)
3. Replace entire function with code above
4. Save file
5. Refresh browser (Ctrl+F5)

Done!
