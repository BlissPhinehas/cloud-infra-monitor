from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    multiprocess,
)
import time
import os

app = FastAPI(title="Cloud Infra Monitor")

# ── Metrics ────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["path"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total number of HTTP errors",
    ["path", "status"],
)

# ── Middleware ──────────────────────────────────────────────
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(path=request.url.path).observe(duration)

    if response.status_code >= 400:
        ERROR_COUNT.labels(
            path=request.url.path,
            status=response.status_code,
        ).inc()

    return response

# ── Routes ─────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Cloud Infra Monitor is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        ERROR_COUNT.labels(path="/items", status=400).inc()
        return Response(status_code=400)
    return {"item_id": item_id, "name": f"Item {item_id}"}