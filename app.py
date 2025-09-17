import os
import requests
import pandas as pd
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in environment")

app = FastAPI()

CSV_FILE = "call_analysis.csv"

def query_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Groq API request failed: {str(e)}")
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Unexpected response from Groq API")

@app.post("/analyze")
async def analyze_transcript(transcript: str = Form(...)):
    if not transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    summary_prompt = f"Summarize this customer service transcript in 2-3 sentences:\n\n{transcript}"
    sentiment_prompt = f"Classify the customer sentiment (positive, neutral, or negative) in this transcript:\n\n{transcript}"

    summary = query_groq(summary_prompt)
    sentiment = query_groq(sentiment_prompt)

    row = {"Transcript": transcript, "Summary": summary, "Sentiment": sentiment}
    df = pd.DataFrame([row])

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)
        
    print("Original Transcript:")
    print(transcript)
    print("\nSummary:")
    print(summary)
    print("\nSentiment:")
    print(sentiment)

    return JSONResponse({
        "Transcript": transcript,
        "Summary": summary,
        "Sentiment": sentiment
    })

@app.get("/")
async def root():
    return JSONResponse({"message": "Welcome to the Customer Call Analysis API. Use POST /analyze"})

