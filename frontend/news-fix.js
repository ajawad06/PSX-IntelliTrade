// Improved news display function that filters XML/RSS artifacts
function displayStockNews(ticker, newsData) {
    const newsTickerSpan = document.getElementById('newsStockTicker');
    const newsContainer = document.getElementById('newsContainer');

    newsTickerSpan.textContent = ticker;
    newsContainer.innerHTML = '';

    if (newsData && newsData.length > 0) {
        // Filter out invalid news items
        const validNews = newsData.filter(item => {
            const title = (item.title || '').toLowerCase();
            const summary = (item.summary || '').toLowerCase();

            // Skip XML/RSS artifacts
            if (title.includes('ispermalink') || title.includes('<item>') ||
                title.includes('xml file') || title.includes('this feed') ||
                summary.includes('ispermalink') || summary.includes('<item>') ||
                title.trim() === 'false' || summary.trim() === 'false' ||
                title.length < 10) {
                return false;
            }

            return true;
        });

        if (validNews.length > 0) {
            validNews.forEach((item, index) => {
                const newsItem = document.createElement('div');
                newsItem.className = 'news-item';

                // Deep clean summary
                let cleanSummary = (item.summary || item.title)
                    .replace(/<[^>]+>/g, '')
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&')
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                    .replace(/&quot;/g, '"')
                    .replace(/&#39;/g, "'")
                    .replace(/isPermalink/gi, '')
                    .replace(/\s+/g, ' ')
                    .trim();

                // Clean title
                let cleanTitle = (item.title || '')
                    .replace(/<[^>]+>/g, '')
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&')
                    .replace(/\s+/g, ' ')
                    .trim();

                // Skip if cleaned content is too short
                if (cleanSummary.length < 20) return;

                newsItem.innerHTML = `
                    <div class="news-title">${cleanTitle}</div>
                   <div class="news-published">📅 ${item.published}</div>
                    <div class="news-summary">${cleanSummary.substring(0, 300)}${cleanSummary.length > 300 ? '...' : ''}</div>
                    <a href="${item.link}" target="_blank" class="news-link">
                        Read Full Article →
                    </a>
                `;

                newsContainer.appendChild(newsItem);
            });

            // If no valid items were actually added
            if (newsContainer.children.length === 0) {
                newsContainer.innerHTML = `
                    <p style="color: var(--text-secondary); text-align: center; padding: 2rem;">
                        No news available for ${ticker} at the moment. Check back later!
                    </p>
                `;
            }
        } else {
            newsContainer.innerHTML = `
                <p style="color: var(--text-secondary); text-align: center; padding: 2rem;">
                    No news available for ${ticker} at the moment. Check back later!
                </p>
            `;
        }
    } else {
        newsContainer.innerHTML = `
            <p style="color: var(--text-secondary); text-align: center; padding: 2rem;">
                No news available for ${ticker} at the moment. Check back later!
            </p>
        `;
    }
}

// Copy this function and replace the displayStockNews function in app.js (around line 312-350)
