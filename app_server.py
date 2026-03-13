import secrets
import string
import os
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# Dictionary to store { "slug": "original_url" }
url_db = {}

def generate_slug(length=8):
    """Generates a URL-safe random string."""
    # characters: a-z, A-Z, 0-9
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route('/urls', methods=['POST'])
def create_url():
    print("Received request to create a new short URL")
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400
    
    original_url = data['url']
    
    # Ensure we don't overwrite an existing slug (rare but good practice)
    slug = generate_slug()
    while slug in url_db:
        slug = generate_slug()
        
    url_db[slug] = original_url
    
    return jsonify({
        "status": "success",
        "slug": slug,
        "short_url": f"http://localhost:10000/{slug}"
    }), 201

@app.route('/<slug>', methods=['GET'])
def redirect_to_url(slug):
    print(f"Received request to redirect slug: {slug}")
    target_url = url_db.get(slug)
    
    if target_url:
        # Standard 302 redirect to the encoded destination
        return redirect(target_url)
    
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    # 1. Render provides a 'PORT' variable (usually 10000). 
    # If it doesn't exist (like on your Mac), it defaults to 5001.
    port = int(os.environ.get("PORT", 5001))
    
    print(f"Starting URL Shortener Service on port {port}")
    
    # 2. MUST remove ssl_context='adhoc' for Render/Docker.
    # 3. host='0.0.0.0' is required for Docker to allow external traffic.
    app.run(host='0.0.0.0', port=port)