import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("entra-id-toolkit-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Entra ID Toolkit API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/policies")
def get_policies():
    return [
        {"id": "ca-mfa-all", "name": "MFA for All Users", "state": "enabled", "mode": "enforced"},
        {"id": "ca-admin-fido2", "name": "Strict FIDO2 for Admins", "state": "enabled", "mode": "enforced"},
        {"id": "ca-guest-review", "name": "Guest Access Review", "state": "enabled", "mode": "report-only"},
        {"id": "ca-legacy-block", "name": "Block Legacy Auth", "state": "enabled", "mode": "enforced"}
    ]

@app.post("/policies/deploy")
def deploy_policy(policy_id: str, tenant_id: str):
    logger.info(f"Deploying policy {policy_id} to tenant {tenant_id}")
    return {"status": "DEPLOYING", "operation_id": f"op_{int(time.time())}", "estimated_duration": "2m"}

@app.post("/policies/simulate")
def simulate_policy(policy_id: str, user_id: str):
    logger.info(f"Simulating policy {policy_id} for user {user_id}")
    return {"impact": "MFA_REQUIRED", "risk_level": "LOW", "device_state": "COMPLIANT"}

@app.get("/risk/summary")
def get_risk_summary():
    return {
        "risky_users": 12,
        "risky_signins_24h": 450,
        "active_remediations": 8,
        "identity_secure_score": 84.5
    }

@app.get("/devices/compliance")
def get_device_compliance():
    return {
        "compliant_devices": 12450,
        "non_compliant_devices": 120,
        "unmanaged_devices": 45,
        "compliance_rate": "98.8%"
    }

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "identity_maturity": 0.88,
        "zero_trust_alignment": 0.92,
        "mfa_coverage": 0.99,
        "break_glass_ready": True
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_tenants": 4,
        "total_users": 150000,
        "total_apps": 1240,
        "toolkit_status": "READY"
    }
