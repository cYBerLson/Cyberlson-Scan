import os
from app import create_app

# Set the configuration based on environment or default to development
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    # When running locally, use these settings
    # In production, use Gunicorn as specified in DEPLOYMENT.md
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
