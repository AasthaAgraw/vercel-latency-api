from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/latency")
async def latency_metrics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    # Load sample telemetry data (replace with your telemetry bundle)
    with open("telemetry.json") as f:
        telemetry = json.load(f)

    result = {}
    for region in regions:
        entries = telemetry.get(region, [])
        if not entries:
            continue
        latencies = np.array([r["latency_ms"] for r in entries])
        uptimes = np.array([r["uptime"] for r in entries])

        result[region] = {
            "avg_latency": float(latencies.mean()),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(uptimes.mean()),
            "breaches": int((latencies > threshold).sum())
        }

    return result
