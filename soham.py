from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if not GEMINI_API_KEY:
            return jsonify({"result": "Error: GEMINI_API_KEY is not set. Please create a .env file with your key."}), 500

        data = request.get_json()
        user_news = data.get("news", "")

        if not user_news:
            return jsonify({"result": "Please provide some news text."}), 400

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        # --- UPDATED STOCK-FOCUSED PROMPT ---
        prompt = f"""
        You are a highly specialized financial AI assistant, expert in analyzing news impact on publicly traded stocks and their associated companies. Your goal is to provide clear, concise, and actionable insights for stock market participants, suitable for beginners but with accurate financial terminology.
        Do NOT give buy/sell investment advice.

        Analyze the news below and generate a JSON response strictly adhering to the specified format. Ensure all analysis points are directly relevant to stock performance, company valuation, and investor sentiment, and *all fields must be populated*.

        News Content:
        {user_news}

        Provide the output in this specific JSON format:
        {{
          "company_mentioned": "Name of the primary company/stock affected (e.g., 'ITC Ltd.', 'InnovateCo', 'Starbucks'). If multiple, list primary. If none, state 'N/A'.",
          "ticker_symbol": "Likely stock ticker symbol (e.g., 'ITC', 'INNOV', 'SBUX'). If not obvious or applicable, state 'N/A'.",
          "summary": "A brief, stock-market focused summary of the news and its immediate implications for the company's stock.",
          "investor_sentiment": "Overall investor sentiment shift expected (e.g., 'Strongly Negative', 'Negative', 'Neutral', 'Positive', 'Strongly Positive').",
          "stock_impact_magnitude": "Overall expected impact on the stock price (e.g., 'Low Volatility', 'Moderate Movement', 'Significant Movement').",
          "affected_metrics": [
            {{"metric": "Key financial or operational metric directly affected (e.g., 'Revenue', 'Profit Margins', 'Sales Volume', 'Market Share', 'Debt Ratio', 'P/E Ratio')", "direction": "Positive/Neutral/Negative", "reason": "Brief explanation of how the news impacts this metric."}},
            {{"metric": "Another affected metric", "direction": "Positive/Neutral/Negative", "reason": "Brief explanation."}}
          ],
          "short_term_stock_reaction": "Expected immediate stock market reaction (e.g., 'Price Drop', 'Price Surge', 'Increased Volatility', 'Trading Halt').",
          "long_term_outlook_for_stock": "Long-term implications for the company's stock and business strategy (e.g., 'Strategic pivot needed', 'Enhanced growth trajectory', 'Sustained headwind').",
          "risk_factors_highlighted": ["List 2-3 specific risks underscored by this news (e.g., 'Regulatory Risk', 'Supply Chain Disruption', 'Competitive Pressure'). If none, state 'N/A'."],
          "peer_impact": "How might this news indirectly affect competitors or companies in the same industry? (e.g., 'Competitors may face similar challenges', 'Opportunity for peers to gain market share'). If none, state 'N/A'.",
          "jargon_buster": {{
            "Term1": "Simple explanation for Term1 relevant to stocks",
            "Term2": "Simple explanation for Term2 relevant to stocks"
          }}
        }}

        Ensure the response is *only* the JSON object, with no additional text or markdown outside of the JSON.
        """
        # --- END UPDATED STOCK-FOCUSED PROMPT ---

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if "candidates" in response_data:
            ai_raw_text = response_data['candidates'][0]['content']['parts'][0]['text']

            # Strip markdown code block delimiters
            if ai_raw_text.startswith("```json") and ai_raw_text.endswith("```"):
                ai_raw_text = ai_raw_text[7:-3].strip()

            try:
                ai_parsed_json = json.loads(ai_raw_text)
                return jsonify({"result": ai_parsed_json})
            except json.JSONDecodeError:
                return jsonify({"result": f"AI did not return valid JSON even after stripping. Raw output: {ai_raw_text}"}), 500
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown API error")
            return jsonify({"result": f"Google API Error: {error_message}"}), 500

    except requests.exceptions.RequestException as req_e:
        return jsonify({"result": f"Network Error contacting Google API: {str(req_e)}"}), 500
    except Exception as e:
        return jsonify({"result": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    print("Server starting at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)