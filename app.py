import os
import logging
import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.timezone import utc_to_ist

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_database_uri():
    """Get database URI - PostgreSQL primary, with SQL Server and MySQL support"""
    
    # PostgreSQL (primary database)
    postgres_url = os.environ.get("DATABASE_URL")
    if postgres_url:
        return postgres_url

    # Direct PostgreSQL configuration for local development
    return "postgresql://gtn_user:gtn_password_2024@localhost:5432/gtn_helpdesk"


# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "dev-secret-key-change-in-production"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database - PostgreSQL primary database
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

@app.template_filter('to_ist')
def to_ist_filter(dt):
    return utc_to_ist(dt).strftime('%Y-%m-%d %H:%M:%S') if dt else ''

# Add custom Jinja2 filter for line breaks
@app.template_filter('nl2br')
def nl2br_filter(s):
    """Convert newlines to <br> tags"""
    return s.replace('\n', '<br>\n') if s else s


with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()
    logging.info("Database tables created")
