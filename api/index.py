from ui_server import app as flask_app, initialize_swarm

# Initialize agents once at cold start
initialize_swarm()

# Vercel Python runtime looks for a module-level WSGI app
app = flask_app
