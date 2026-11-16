import json

def handler(request):
    """Vercel serverless function for /api/code/files
    Returns metadata about project files similar to original implementation.
    """
    files_meta = [
        {"name": "pipeline.py", "path": "pipeline.py", "category": "Pipeline", "description": "Master Pipeline: Ingestion, UEBA baseline, Deep Learning & SOC Agent dispatch"},
        {"name": "soc_agents.py", "path": "agents/soc_agents.py", "category": "Agents", "description": "Autonomous SOC Agents: Alert Triage, Behavioral Profiler, Threat Hunter & Response"},
        {"name": "base_agent.py", "path": "agents/base_agent.py", "category": "Agents", "description": "OODA Loop (Observe, Orient, Decide, Act) Framework & Agent Messaging Protocol"},
        {"name": "deep_anomaly_detector.py", "path": "models/deep_anomaly_detector.py", "category": "Models", "description": "Bi-LSTM Sequence Autoencoder for 30-day temporal reconstruction loss"},
        {"name": "hybrid_scorer.py", "path": "models/hybrid_scorer.py", "category": "Models", "description": "Multi-model Risk Fusion & Regulatory Impact Compliance Scorer"},
        {"name": "engine.py", "path": "ueba/engine.py", "category": "UEBA", "description": "UEBA Engine: Peer group cohort baseline & multivariate Z-score computation"},
        {"name": "features.py", "path": "ueba/features.py", "category": "UEBA", "description": "12-Dimensional Behavioral Feature Extractor from daily multi-modal logs"},
        {"name": "banking_cert_generator.py", "path": "data/banking_cert_generator.py", "category": "Data", "description": "Enterprise CERT Multi-Modal Log Generator with planted ground-truth threats"},
        {"name": "cert_schema.py", "path": "data/cert_schema.py", "category": "Data", "description": "Standard CERT Log Event Schemas & CSV dataset exporter"},
        {"name": "server.py", "path": "server.py", "category": "Server", "description": "Interactive Local Financial SOC Web Server with strict MIME controls"},
        {"name": "test_system.py", "path": "tests/test_system.py", "category": "Tests", "description": "Comprehensive Automated Verification & Detection Test Suite"},
    ]
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(files_meta),
    }
