import dash
import dash_bootstrap_components as dbc

# Create a new Dash app instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configure the app to interact with the FastAPI backend
app.config.suppress_callback_exceptions = True
app.title = "Neo4j Database Management Dashboard"
