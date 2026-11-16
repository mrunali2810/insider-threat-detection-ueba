"""
Interactive Local Web Server for Financial Insider Threat SOC Platform.

Serves the interactive SOC dashboard on http://localhost:8989 and provides
REST API endpoints with explicit MIME type enforcement to prevent Windows plain-text rendering.
"""

import os
import sys
import json
import mimetypes
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Explicitly ensure Windows registry does not corrupt HTML MIME type
mimetypes.init()
mimetypes.add_type("text/html", ".html")
mimetypes.add_type("text/html", ".htm")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/json", ".json")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")


class FinancialSOCHandler(SimpleHTTPRequestHandler):
    """Custom request handler serving the SOC dashboard and REST API with strict MIME types."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_GET(self):
        # Force proper HTML rendering for root and dashboard routes
        clean_path = self.path.split("?")[0].strip("/")
        if clean_path in ("", "index.html"):
            filepath = os.path.join(UI_DIR, "index.html")
            try:
                with open(filepath, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"Error loading index: {e}")
                return

        elif clean_path in ("dashboard", "dashboard.html"):
            filepath = os.path.join(UI_DIR, "dashboard.html")
            try:
                with open(filepath, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_error(500, f"Error loading dashboard: {e}")
                return

        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            status_payload = {
                "status": "ONLINE",
                "system": "Meridian Bank Autonomous Cyber SOC",
                "frameworks": ["GLBA 501(b)", "SOX 404", "PCI-DSS 10.2", "SWIFT CSP"],
                "active_agents": ["AlertTriageAgent", "BehavioralProfilerAgent", "ForensicHunterAgent", "AutonomousResponseAgent"],
                "active_threats": 4,
                "containment_latency_ms": 142
            }
            self.wfile.write(json.dumps(status_payload).encode("utf-8"))
            return

        elif self.path == "/api/code/files":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            files_meta = [
                {"name": "pipeline.py", "path": "pipeline.py", "category": "Pipeline", "description": "Master Pipeline: Ingestion, UEBA baseline, Deep Learning, & SOC Agent dispatch"},
                {"name": "soc_agents.py", "path": "agents/soc_agents.py", "category": "Agents", "description": "Autonomous SOC Agents: Alert Triage, Behavioral Profiler, Threat Hunter, & Response"},
                {"name": "base_agent.py", "path": "agents/base_agent.py", "category": "Agents", "description": "OODA Loop (Observe, Orient, Decide, Act) Framework & Agent Messaging Protocol"},
                {"name": "deep_anomaly_detector.py", "path": "models/deep_anomaly_detector.py", "category": "Models", "description": "Bi-LSTM Sequence Autoencoder for 30-day temporal reconstruction loss"},
                {"name": "hybrid_scorer.py", "path": "models/hybrid_scorer.py", "category": "Models", "description": "Multi-model Risk Fusion & Regulatory Impact Compliance Scorer"},
                {"name": "engine.py", "path": "ueba/engine.py", "category": "UEBA", "description": "UEBA Engine: Peer group cohort baseline & multivariate Z-score computation"},
                {"name": "features.py", "path": "ueba/features.py", "category": "UEBA", "description": "12-Dimensional Behavioral Feature Extractor from daily multi-modal logs"},
                {"name": "banking_cert_generator.py", "path": "data/banking_cert_generator.py", "category": "Data", "description": "Enterprise CERT Multi-Modal Log Generator with planted ground-truth threats"},
                {"name": "cert_schema.py", "path": "data/cert_schema.py", "category": "Data", "description": "Standard CERT Log Event Schemas & CSV dataset exporter"},
                {"name": "server.py", "path": "server.py", "category": "Server", "description": "Interactive Local Financial SOC Web Server with strict MIME controls"},
                {"name": "test_system.py", "path": "tests/test_system.py", "category": "Tests", "description": "Comprehensive Automated Verification & Detection Test Suite"}
            ]
            self.wfile.write(json.dumps(files_meta).encode("utf-8"))
            return

        elif self.path.startswith("/api/code/content"):
            from urllib.parse import parse_qs, urlparse
            query = parse_qs(urlparse(self.path).query)
            req_file = query.get("file", [""])[0].replace("\\", "/").strip("/")
            target_path = os.path.normpath(os.path.join(BASE_DIR, req_file))
            if not target_path.startswith(BASE_DIR) or not os.path.isfile(target_path):
                self.send_error(404, "File not found or access denied")
                return
            try:
                with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                    code_text = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                payload = {
                    "file": req_file,
                    "name": os.path.basename(req_file),
                    "lines": len(code_text.splitlines()),
                    "size": len(code_text),
                    "code": code_text
                }
                self.wfile.write(json.dumps(payload).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
                return

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/action"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            payload = json.loads(post_data) if post_data else {}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = {
                "status": "SUCCESS",
                "action": payload.get("action", "POLICY_ENFORCEMENT"),
                "target": payload.get("target", "ALL_ENDPOINTS"),
                "timestamp": "2025-05-26 14:02:11",
                "latency_ms": 138,
                "message": f"Successfully executed {payload.get('action', 'containment')} across banking infrastructure."
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def start_server(preferred_ports=(8989, 9050, 5555, 7890, 8765)):
    env_port = os.environ.get("PORT")
    ports_to_try = [int(env_port)] if env_port else list(preferred_ports)
    for port in ports_to_try:
        try:
            server_address = ("0.0.0.0", port)
            httpd = HTTPServer(server_address, FinancialSOCHandler)
            url = f"http://localhost:{port}/"
            print("=" * 70, flush=True)
            print(f"  MERIDIAN BANK FINANCIAL SOC PLATFORM SERVER", flush=True)
            print(f"  URL: {url}", flush=True)
            print(f"  Serving dashboard from: {UI_DIR}", flush=True)
            print("=" * 70, flush=True)
            httpd.serve_forever()
            return
        except (PermissionError, OSError) as e:
            print(f"[!] Port {port} unavailable ({e}), trying next...", flush=True)
            continue
    raise RuntimeError("Could not bind to any available port.")


if __name__ == "__main__":
    start_server()
