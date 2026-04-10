from flask import Flask, redirect, request, jsonify
from spotify.auth import auth_manager

from routes.ingest import ingest_bp
from routes.stats import stats_bp

from db.database import init_db

def create_app():
    app = Flask(__name__)

    # --- CONFIG ---
    app.config["AUTH_MANAGER"] = auth_manager

    # --- INIT DB ---
    init_db()

    # --- BASIC ROUTES ---
    @app.route("/")
    def health_check():
        return {"status": "Jamz backend running"}

    @app.route("/login")
    def login():
        return redirect(auth_manager.get_authorize_url())

    @app.route("/callback")
    def callback():
        code = request.args.get("code")

        if not code:
            return jsonify({"error": "Missing Authentication code"}), 400

        auth_manager.get_access_token(code)
        return {"message": "Authentication successful"}
    
    @app.route("/me")
    def me():
        import spotipy
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp.current_user()

    # --- REGISTER BLUEPRINTS ---
    app.register_blueprint(ingest_bp)
    app.register_blueprint(stats_bp)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)