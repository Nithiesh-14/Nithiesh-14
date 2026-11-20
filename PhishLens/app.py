"""PhishLens web app. Standard library only; never fetches submitted URLs."""
import json, os
from pathlib import Path
from wsgiref.simple_server import make_server
from src.detector import analyze_url
ROOT=Path(__file__).resolve().parent
MIME={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"application/javascript; charset=utf-8"}
def _file(path,start):
    if not path.is_file():
        body=b"Not found"; start("404 Not Found",[("Content-Type","text/plain"),("Content-Length",str(len(body)))]); return [body]
    body=path.read_bytes(); start("200 OK",[("Content-Type",MIME.get(path.suffix,"application/octet-stream")),("Content-Length",str(len(body)))]); return [body]
def application(env,start):
    method,path=env.get("REQUEST_METHOD","GET"),env.get("PATH_INFO","/")
    if method=="GET" and path in ("/","/index.html"): return _file(ROOT/"static"/"index.html",start)
    if method=="GET" and path in ("/style.css","/app.js"): return _file(ROOT/"static"/path.lstrip("/"),start)
    if method=="GET" and path=="/health":
        body=b'{"status":"ok","service":"PhishLens"}'; start("200 OK",[("Content-Type","application/json"),("Content-Length",str(len(body)))]); return [body]
    if method=="POST" and path=="/api/analyze":
        try:
            length=int(env.get("CONTENT_LENGTH") or "0")
            if length>8192: raise ValueError("Request body is too large.")
            payload=json.loads(env["wsgi.input"].read(length) or b"{}"); result=analyze_url(payload.get("url","")); body,status=json.dumps(result).encode(),"200 OK"
        except (ValueError,TypeError,json.JSONDecodeError) as exc: body,status=json.dumps({"error":str(exc) or "Invalid request."}).encode(),"400 Bad Request"
        start(status,[("Content-Type","application/json; charset=utf-8"),("Content-Length",str(len(body))),("Cache-Control","no-store")]); return [body]
    body=b'{"error":"Not found"}'; start("404 Not Found",[("Content-Type","application/json"),("Content-Length",str(len(body)))]); return [body]
if __name__=="__main__":
    port=int(os.environ.get("PORT","5000")); print("PhishLens running on port",port); make_server("0.0.0.0",port,application).serve_forever()
