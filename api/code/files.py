from http.server import BaseHTTPRequestHandler
import json

FILES_META = [
    {"name": "pipeline.py", "path": "pipeline.py", "category": "Pipeline", "description": "Master Pipeline"},
    {"name": "soc_agents.py", "path": "agents/soc_agents.py", "category": "Agents", "description": "SOC Agents"},
    {"name": "base_agent.py", "path": "agents/base_agent.py", "category": "Agents", "description": "OODA Agent Framework"},
    {"name": "deep_anomaly_detector.py", "path": "models/deep_anomaly_detector.py", "category": "Models", "description": "Bi-LSTM Anomaly Detector"},
    {"name": "hybrid_scorer.py", "path": "models/hybrid_scorer.py", "category": "Models", "description": "Hybrid Risk Scorer"},
    {"name": "engine.py", "path": "ueba/engine.py", "category": "UEBA", "description": "UEBA Engine"},
    {"name": "features.py", "path": "ueba/features.py", "category": "UEBA", "description": "Behavioral Feature Extractor"},
    {"name": "banking_cert_generator.py", "path": "data/banking_cert_generator.py", "category": "Data", "description": "CERT Data Generator"},
    {"name": "cert_schema.py", "path": "data/cert_schema.py", "category": "Data", "description": "CERT Log Schemas"},
    {"name": "server.py", "path": "server.py", "category": "Server", "description": "Local SOC Server"},
    {"name": "test_system.py", "path": "tests/test_system.py", "category": "Tests", "description": "System Tests"}
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(FILES_META).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
