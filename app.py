from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone
from mangum import Mangum

app = FastAPI(title="Failures API")

# مدل داده‌ها
class FailureItem(BaseModel):
    label: str
    failure_type: str  # بهتره type رو تغییر بدیم تا با builtin تداخل نکنه
    color: str
    timestamp: datetime

class FailuresResponse(BaseModel):
    items: List[FailureItem]

# Endpoint
@app.get("/api/failures", response_model=FailuresResponse)
def get_failures():
    now = datetime.now(timezone.utc)  # زمان UTC با timezone-aware
    items = [
        {"label": "Flow Instability", "failure_type": "AI", "color": "#ff3b30", "timestamp": now - timedelta(minutes=30)},
        {"label": "Pressure Anomaly", "failure_type": "AI", "color": "#ff3b30", "timestamp": now - timedelta(hours=1)},
        {"label": "Chemical Composition", "failure_type": "AI", "color": "#ffcc00", "timestamp": now - timedelta(minutes=10)},
        {"label": "Temperature Anomaly", "failure_type": "AI", "color": "#34c759", "timestamp": now - timedelta(minutes=45)},
        {"label": "Fluid Level Anomaly", "failure_type": "AI", "color": "#34c759", "timestamp": now - timedelta(hours=2)},
        {"label": "Viscosity Anomaly", "failure_type": "AI", "color": "#34c759", "timestamp": now - timedelta(minutes=5)}
    ]
    # مرتب‌سازی از جدیدترین به قدیمی
    items = sorted(items, key=lambda x: x["timestamp"], reverse=True)
    return {"items": items}

# Adapter برای Vercel Serverless
handler = Mangum(app)
