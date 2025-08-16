#!/usr/bin/env python3
"""
Simple web server for Railway health checks
"""
import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Check if bot is running
            bot_status = "running" if hasattr(self.server, 'bot_running') else "starting"
            
            response = {
                "status": "healthy",
                "bot_status": bot_status,
                "timestamp": time.time()
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Audify Music Bot</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .status { color: green; font-weight: bold; }
                </style>
            </head>
            <body>
                <h1>🎵 Audify Music Bot</h1>
                <p class="status">✅ Bot is running successfully!</p>
                <p>Developed with ❤️ by @devforgekush</p>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        # Suppress access logs
        pass

def start_web_server(port=8000):
    """Start the web server in a separate thread"""
    def run_server():
        try:
            server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
            server.bot_running = True
            print(f"🌐 Web server started on port {port}")
            server.serve_forever()
        except Exception as e:
            print(f"❌ Web server failed to start: {e}")
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    start_web_server(port)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Web server stopped")
