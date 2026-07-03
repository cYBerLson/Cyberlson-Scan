import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from config import config

csrf = CSRFProtect()
talisman = Talisman()

def create_app(config_name=None):
    """Application factory for Cyberlson-Scan."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(__name__,
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))

    app.config.from_object(config[config_name])

    csrf.init_app(app)

    csp = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            'https://cdn.jsdelivr.net',
            'https://cdn.tailwindcss.com'
        ],
        'style-src': [
            "'self'",
            'https://cdn.jsdelivr.net',
            'https://fonts.googleapis.com',
            'https://cdn.tailwindcss.com'
        ],
        'font-src': [
            "'self'",
            'https://fonts.gstatic.com'
        ],
        'img-src': ["'self'"]
    }

    if app.debug:
        talisman.init_app(
            app,
            content_security_policy={
                **csp,
                "style-src": [
                    "'self'",
                    "'unsafe-inline'",
                    "https://fonts.googleapis.com",
                    "https://cdn.tailwindcss.com"
                ]
            },
            force_https=False
        )
    else:
        talisman.init_app(
            app,
            content_security_policy=csp,
            force_https=True,
            strict_transport_security=True
        )

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app