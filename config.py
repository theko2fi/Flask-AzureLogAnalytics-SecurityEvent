"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


TENANT = environ.get("TENANT")
SP_ID = environ.get("SP_ID")
SP_SECRET = environ.get("SP_SECRET")
AZURE_LOG_CUSTOMER_ID = environ.get("AZURE_LOG_CUSTOMER_ID")