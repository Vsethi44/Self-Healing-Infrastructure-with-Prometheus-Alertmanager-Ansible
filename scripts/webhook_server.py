from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess, datetime

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        with open("/opt/webhook.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] Webhook triggered\n")
        subprocess.run(["ansible-playbook", "/opt/heal.yml"], check=False)
        with open("/opt/webhook.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] heal.yml executed\n")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5001), WebhookHandler)
    with open("/opt/webhook.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Webhook server started\n")
    server.serve_forever()
