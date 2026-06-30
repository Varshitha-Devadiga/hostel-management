from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Import routes to register endpoints
from . import routes
