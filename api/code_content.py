import json, os, urllib.parse

def handler(request):
    """Vercel serverless function for /api/code/content
    Safely reads a file from the repository based on a 'file' query parameter.
    Only files within the project root are allowed.
    """
    # Parse query string
    query = urllib.parse.parse_qs(request.get('queryStringParameters') or '')
    req_file = query.get('file', [''])[0]
    # Normalize and ensure path stays within project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_path = os.path.normpath(os.path.join(base_dir, req_file))
    if not target_path.startswith(base_dir) or not os.path.isfile(target_path):
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "File not found or access denied"}),
        }
    try:
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            code_text = f.read()
        payload = {
            "file": req_file,
            "name": os.path.basename(req_file),
            "lines": len(code_text.splitlines()),
            "size": len(code_text),
            "code": code_text,
        }
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json; charset=utf-8", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(payload),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }
