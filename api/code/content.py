from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

BASE_DIR = os.path.realpath(os.getcwd())

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        req_file = query.get("file", [""])[0].replace("\\", "/")
        target = os.path.realpath(os.path.join(BASE_DIR, req_file))

        try:
            if os.path.commonpath([BASE_DIR, target]) != BASE_DIR:
                self.send_error(404, "Access denied")
                return
        except ValueError:
            self.send_error(404, "Access denied")
            return

        if not os.path.isfile(target) or os.path.basename(target).startswith("."):
            self.send_error(404, "File not found")
            return

        try:
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                code = f.read()

            payload = {
                "file": req_file,
                "name": os.path.basename(target),
                "lines": len(code.splitlines()),
                "size": len(code),
                "code": code
            }

            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception:
            self.send_error(500, "Unable to read file")
