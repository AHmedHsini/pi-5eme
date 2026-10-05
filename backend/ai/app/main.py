"""
MarketSim AI — FastAPI ML service.
Called only by Spring Boot (internal network). Not a public API.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="MarketSim AI",
    description="Internal ML / XAI / NLP worker for MarketSim",
    version="0.1.0",
)


class RiskRequest(BaseModel):
    symbol: str
    qty: float = Field(gt=0)
    side: str
    portfolio_id: str | None = None


class RiskResponse(BaseModel):
    risk_score: float
    suggested_stop_loss: float | None
    suggested_take_profit: float | None
    model_version: str


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    label: str
    score: float
    model_version: str


class ExplainRequest(BaseModel):
    prediction_id: str
    context: dict = Field(default_factory=dict)


class ExplainResponse(BaseModel):
    summary: str
    method: str
    features: list[dict]


@app.get("/health")
def health():
    return {"status": "ok", "service": "marketsim-ai"}


@app.post("/predict/risk", response_model=RiskResponse)
def predict_risk(body: RiskRequest):
    # Placeholder heuristic — replace with trained model
    base = min(1.0, abs(body.qty) / 1000.0)
    return RiskResponse(
        risk_score=round(base, 4),
        suggested_stop_loss=None,
        suggested_take_profit=None,
        model_version="risk-stub-0.1",
    )


@app.post("/sentiment/news", response_model=SentimentResponse)
def sentiment_news(body: SentimentRequest):
    # Placeholder — replace with NLP model
    text = body.text.lower()
    bullish = any(w in text for w in ("rise", "gain", "bull", "surge"))
    bearish = any(w in text for w in ("fall", "loss", "bear", "crash"))
    if bullish and not bearish:
        return SentimentResponse(label="positive", score=0.7, model_version="sent-stub-0.1")
    if bearish and not bullish:
        return SentimentResponse(label="negative", score=0.7, model_version="sent-stub-0.1")
    return SentimentResponse(label="neutral", score=0.5, model_version="sent-stub-0.1")


@app.post("/xai/explain", response_model=ExplainResponse)
def explain(body: ExplainRequest):
    return ExplainResponse(
        summary="Stub explanation — wire SHAP/LIME here.",
        method="stub",
        features=[{"name": "placeholder", "impact": 0.0}],
    )


# Planned routes (see docs/ARCHITECTURE.md):
# POST /predict/trend
# POST /agent/decide
# POST /stress/impact
# POST /actuarial/premium
# POST /learning/recommend
