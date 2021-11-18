from application import db, create_app, app
from application.config import Config
from application.resources import ProfileRecourse, BrandResource

# Call the application factory function to construct a Flask application
# instance using the development configuration
# app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Profile': ProfileRecourse, 'Brand': BrandResource}