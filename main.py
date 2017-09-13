import os

from dotenv import load_dotenv

from app import create_app
from app.apis import businesses, vendors, statuses

# load dotenv in the base root
APP_ROOT = os.path.abspath(os.path.dirname(__file__))  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, 'local.env')
load_dotenv(dotenv_path)

config_name = os.getenv('APP_SETTINGS')  # config_name = "development"

app = create_app(config_name)


# API routes
@app.route('/')
def index():
    return "Hello, World!"


@app.route('/businesses/', methods=['POST', 'GET', 'PATCH'])
def business_route():
    return businesses()


@app.route('/vendors/', methods=['POST', 'GET'])
def vendor_route():
    return vendors()


@app.route('/statuses/', methods=['POST', 'GET'])
def status_route():
    return statuses()
