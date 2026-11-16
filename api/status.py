from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status_payload = {
            "status": "ONLINE",
            "system": "Meridian Bank Autonomous Cyber SOC",
            "frameworks": ["GLBA 501(b)", "SOX 404", "PCI-DSS 10.2", "SWIFT CSP"],
            "active_agents": [
                "AlertTriageAgent",
                "BehavioralProfilerAgent",
                "ForensicHunterAgent",
                "AutonomousResponseAgent"
            ],
            "active_threats": 4,
            "containment_latency_ms": 142
        }

        body = json.dumps(status_payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
