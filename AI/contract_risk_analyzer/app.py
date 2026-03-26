from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from analyzer import ContractAnalyzer
import os

app = FastAPI(title="AI-Based Contract Risk Analyzer")

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the NLP/ML Analyzer
analyzer = ContractAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/analyze")
async def analyze_contract(text: str = Form(...)):
    """
    Endpoint to analyze a contract.
    It expects form data with a 'text' field.
    """
    result = analyzer.analyze(text)
    return result

if __name__ == "__main__":
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
