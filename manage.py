from app.api.app import create_app
from app.infrastructure.db import db
from app.infrastructure.models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {"db": db}