# 📈 Market Pulse — Stock Impact AI Analyst

> Paste any financial news article and get an instant, AI-powered breakdown of how it affects a company's stock — powered by Google Gemini.

---

## 🚀 What It Does

**Market Pulse** analyzes raw news text and returns a structured, investor-friendly report that includes:

| Output Field | Description |
|---|---|
| 🏢 Company & Ticker | Primary company and stock symbol affected |
| 📊 Market Summary | Stock-focused summary of the news |
| 🎭 Investor Sentiment | Positive / Neutral / Negative sentiment shift |
| 📉 Financial Metrics | Revenue, margins, P/E ratio impacts with direction |
| ⚡ Short-Term Reaction | Immediate expected stock movement |
| 🔭 Long-Term Outlook | Strategic implications for the company |
| ⚠️ Risk Factors | Key risks highlighted by the news |
| 🏭 Peer Impact | How competitors might be affected |
| 📖 Jargon Buster | Plain-English explanations of financial terms used |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3 · Flask · Flask-CORS |
| **AI Engine** | Google Gemini 2.5 Flash API |
| **Frontend** | Vanilla HTML · CSS · JavaScript |
| **Config** | python-dotenv (`.env` file) |

---

## 📁 Project Structure

```
market_pulse/
├── soham.py        # Flask backend — API routes & Gemini integration
├── soham.html      # Frontend UI — news input & results dashboard
├── .env            # Your API key (never committed to git)
├── .gitignore      # Excludes .env and other sensitive files
└── README.md       # This file
```

---

## ⚙️ Setup & Run

### 1. Clone the Repository

```bash
git clone https://github.com/Sohamm-afk/Market_pulse.git
cd Market_pulse
```

### 2. Install Python Dependencies

```bash
pip install flask flask-cors python-dotenv requests
```

### 3. Add Your Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

> Get your free API key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Start the Backend Server

```bash
python soham.py
```

Server will start at: **http://localhost:8080**

### 5. Open the Frontend

Open `soham.html` directly in your browser (double-click the file), then paste any financial news and click **Analyze Financial Data**.

---

## 💡 How It Works

```
User pastes news
       │
       ▼
soham.html (frontend)
  → POST /analyze with { news: "..." }
       │
       ▼
soham.py (Flask backend)
  → Builds structured prompt with financial analysis instructions
  → Calls Gemini 2.5 Flash API
  → Parses JSON response
  → Returns structured data to frontend
       │
       ▼
soham.html renders:
  Company Card · Sentiment Badge · Metrics Table
  Short/Long-Term Outlook · Jargon Buster
```

---

## 📸 Sample Analysis Output

When you analyze a news article like *"Apple announces record-breaking AI chip sales..."*, you'll see:

- **Company:** Apple Inc. | **Ticker:** AAPL
- **Sentiment:** 🟢 Strongly Positive
- **Metrics:** Revenue ↑, Profit Margins ↑, Market Share ↑
- **Short-Term:** Price Surge
- **Long-Term:** Enhanced growth trajectory

---

## ⚠️ Disclaimer

> This tool is for **educational purposes only**. It does **not** provide investment advice or buy/sell recommendations. Always consult a qualified financial advisor before making investment decisions.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ using Google Gemini AI*
