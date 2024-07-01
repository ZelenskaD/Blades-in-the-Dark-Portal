from flask import Flask


def register_blueprints(blades_app: Flask) -> Flask:
    # Import Blueprints using absolute imports
    from blueprints.homepage_routes import homepage_bp
    from blueprints.auth_routes import auth_bp
    from blueprints.user_routes import users_bp
    from blueprints.campaign_routes import campaigns_bp
    from blueprints.session_routes import sessions_bp
    from blueprints.character_routes import characters_bp

    # Register Blueprints
    blades_app.register_blueprint(homepage_bp, url_prefix='/')
    blades_app.register_blueprint(auth_bp, url_prefix='/auth')
    blades_app.register_blueprint(users_bp, url_prefix='/users')
    blades_app.register_blueprint(campaigns_bp, url_prefix='/campaigns')
    blades_app.register_blueprint(sessions_bp, url_prefix='/sessions')
    blades_app.register_blueprint(characters_bp, url_prefix='/characters')

    return blades_app



