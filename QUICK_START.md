# PSX Stock Advisor - Quick Start Guide

## 🚀 Quick Start (Just 3 Steps!)

### Step 1: Start Backend Server
Open a terminal in the project folder and run:
```bash
cd backend
python app.py
```

Keep this terminal running! You should see:
```
PSX Stock Advisor - Flask API Server
Server starting on http://localhost:5000
```

### Step 2: Start Frontend Server
Open a **NEW** terminal and run:
```bash
cd frontend
python -m http.server 8080
```

Keep this terminal running too!

### Step 3: Open Your Browser
Navigate to: **http://localhost:8080**

---

## 🎉 Features Ready to Use

### 1. **AI Portfolio Builder** 💼
- Enter budget (e.g., PKR 100,000)
- Select risk level
- Click "Generate Smart Portfolio"
- **AI will show you exactly which stocks to buy and how many shares!**

### 2. **Stock Analysis** 📈
- Select any stock (HBL, OGDC, PSO, etc.)
- View interactive charts
- See **BUY/SELL/HOLD signals** prominently displayed
- Analyze technical indicators

### 3. **Market Scanner** 🔍
- Scan all PSX stocks
- Filter by BUY/SELL signals
- View real-time opportunities

---

## ✅ Recent Improvements

✅ **Charts are now compact** - Fixed height, no more vertical stretching  
✅ **More BUY/SELL signals** - Algorithm adjusted for more decisive signals  
✅ **Lower confidence threshold** - Portfolio builder finds more opportunities (60% instead of 70%)  
✅ **Better signal distribution** - You'll see mix of BUY, SELL, and HOLD signals  

---

## 📊 What Changed?

### Algorithm Improvements:
- **Lower thresholds**: Now requires score of 2 instead of 3 for BUY/SELL (more decisive)
- **Higher weights**: Technical indicators have more impact on decision
- **Wider RSI range**: RSI < 35 = Oversold (was 30), RSI > 65 = Overbought (was 70)
- **Enhanced scoring**: Price direction, trend strength, volume all contribute more

### Chart Improvements:
- **Fixed heights**: Price chart = 350px, RSI/MACD = 250px
- **Cleaner axes**: No rotation, auto-skip labels
- **No point markers**: Cleaner line charts
- **Professional spacing**: Better for trading view

---

## 🐛 Troubleshooting

**Portfolio Builder not finding stocks?**
- Wait 1-2 minutes for AI to scan all stocks
- Try lower budget (PKR 50,000)
- Market conditions may have few BUY signals today

**Market Scanner not working?**
- Refresh the page
- Check both terminal windows are running
- Try clicking "All Stocks" filter first

**Charts extending too much?**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Make sure you're using updated files

---

## 💡 Pro Tips

1. **Test Portfolio Builder** with PKR 100,000 and "Moderate" risk first
2. **Try different stocks** - Some have better signals than others
3. **Use Market Scanner** to find the best opportunities quickly
4. **Check Dashboard** for overall market statistics

---

**Need help? Check the main README.md for full documentation!**
