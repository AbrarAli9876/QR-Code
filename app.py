import io
import os
from flask import Flask, render_template, send_file, request
import qrcode

app = Flask(__name__)

# Set APP_BASE_URL to your HTTPS tunnel URL when you want to scan the QR
# from a phone. Example: https://your-subdomain.trycloudflare.com
APP_BASE_URL = os.getenv("APP_BASE_URL", "").rstrip("/")


def public_base_url():
    return APP_BASE_URL or request.host_url.rstrip("/")


@app.get("/")
def index():
    target_url = f"{public_base_url()}/location"
    return render_template("index.html", target_url=target_url)


@app.get("/qr.png")
def qr_png():
    target_url = f"{public_base_url()}/location"
    img = qrcode.make(target_url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png", download_name="location-qr.png")


@app.get("/location")
def location():
    return render_template("location.html")


if __name__ == "__main__":
    # Local development server. Do not expose Flask's debug server publicly.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
